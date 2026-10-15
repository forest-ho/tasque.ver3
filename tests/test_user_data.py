import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import database
from components.user_identity import ensure_browser_user_id, parse_user_id


class UserDataIsolationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.sqlite3"
        self.user_a = str(uuid.uuid4())
        self.user_b = str(uuid.uuid4())

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_tasks_and_profiles_are_scoped_to_browser_user(self):
        database.ensure_user(self.user_a, self.db_path)
        database.ensure_user(self.user_b, self.db_path)
        task_id = database.create_main_task(
            self.user_a, "User A task", "2026-11-01", self.db_path
        )
        database.create_sub_task(
            self.user_a, task_id, "User A subtask", "高", "2026-10-20", self.db_path
        )

        self.assertEqual(
            database.get_user_profile(self.user_a, self.db_path)["level"], 1
        )
        self.assertEqual(database.list_main_tasks(self.user_b, self.db_path), [])
        self.assertEqual(database.list_sub_tasks(self.user_b, task_id, self.db_path), [])

    def test_user_cannot_attach_subtask_to_another_users_main_task(self):
        task_id = database.create_main_task(
            self.user_a, "User A task", "2026-11-01", self.db_path
        )

        with self.assertRaisesRegex(ValueError, "does not belong"):
            database.create_sub_task(
                self.user_b,
                task_id,
                "Cross-user subtask",
                "中",
                "2026-10-20",
                self.db_path,
            )

        self.assertEqual(database.list_sub_tasks(self.user_a, task_id, self.db_path), [])

    def test_create_multiple_subtasks_and_complete_each_only_once(self):
        task_id = database.create_main_task(
            self.user_a, "User A task", "2026-11-01", self.db_path
        )

        sub_task_ids = database.create_sub_tasks(
            self.user_a,
            task_id,
            [
                {
                    "name": "First subtask",
                    "priority": "高",
                    "due_date": "2026-10-20",
                },
                {
                    "name": "Second subtask",
                    "priority": "低",
                    "due_date": "2026-10-21",
                },
            ],
            self.db_path,
        )

        self.assertEqual(len(sub_task_ids), 2)
        self.assertEqual(
            [task["completed"] for task in database.list_sub_tasks(
                self.user_a, task_id, self.db_path
            )],
            [False, False],
        )
        self.assertTrue(
            database.complete_sub_task(
                self.user_a, task_id, sub_task_ids[0], self.db_path
            )
        )
        self.assertFalse(
            database.complete_sub_task(
                self.user_a, task_id, sub_task_ids[0], self.db_path
            )
        )
        self.assertEqual(
            [task["completed"] for task in database.list_sub_tasks(
                self.user_a, task_id, self.db_path
            )],
            [True, False],
        )

    def test_initialize_database_migrates_existing_subtask_table(self):
        with sqlite3.connect(self.db_path) as connection:
            connection.executescript(
                """
                CREATE TABLE users (user_id TEXT PRIMARY KEY);
                CREATE TABLE user_profiles (
                    user_id TEXT PRIMARY KEY REFERENCES users(user_id),
                    display_name TEXT NOT NULL DEFAULT '冒険者',
                    level INTEGER NOT NULL DEFAULT 1,
                    icon TEXT
                );
                CREATE TABLE main_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL REFERENCES users(user_id),
                    name TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, id)
                );
                CREATE TABLE sub_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    main_task_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

        database.initialize_database(self.db_path)
        with sqlite3.connect(self.db_path) as connection:
            columns = {
                row[1] for row in connection.execute("PRAGMA table_info(sub_tasks)")
            }

        self.assertIn("completed", columns)

    def test_cookie_identity_must_be_a_canonical_uuid(self):
        user_id = str(uuid.uuid4())
        self.assertEqual(parse_user_id(user_id), user_id)
        self.assertIsNone(parse_user_id("not-a-user-id"))
        self.assertIsNone(parse_user_id(None))

    def test_missing_cookie_sets_identity_in_the_main_document(self):
        streamlit = Mock(
            context=SimpleNamespace(cookies={}),
            session_state={},
        )
        streamlit.stop.side_effect = RuntimeError("stopped")

        with patch("components.user_identity.st", streamlit):
            with self.assertRaisesRegex(RuntimeError, "stopped"):
                ensure_browser_user_id()

        html = streamlit.html.call_args.args[0]
        self.assertIn("document.cookie =", html)
        self.assertIn("window.location.reload()", html)
        self.assertNotIn("window.parent.location.reload()", html)
        self.assertTrue(streamlit.html.call_args.kwargs["unsafe_allow_javascript"])


if __name__ == "__main__":
    unittest.main()
