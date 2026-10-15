import unittest
from datetime import date
from unittest.mock import ANY, patch

from pages.quest_forms import (
    _create_main_task,
    _register_sub_tasks,
    render_sub_task_form,
)


class SessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __setattr__(self, name, value):
        self[name] = value


class SubTaskFormTests(unittest.TestCase):
    def test_initial_main_task_and_pending_subtasks_are_created_together(self):
        pending_tasks = [
            {"name": "Step one", "priority": "高", "due_date": "2026-10-20"},
            {"name": "Step two", "priority": "低", "due_date": "2026-10-21"},
        ]
        state = SessionState(
            user_id="user",
            main_task_name=" Main quest ",
            main_task_due_date=date(2026, 10, 22),
            main_task_pending_sub_tasks=pending_tasks,
        )
        with (
            patch("pages.quest_forms.st.session_state", state),
            patch(
                "pages.quest_forms.database.create_main_task_with_subtasks",
                return_value=9,
            ) as create_task,
            patch("pages.quest_forms.go_home") as go_home,
        ):
            _create_main_task()

        create_task.assert_called_once_with(
            "user",
            "Main quest",
            "2026-10-22",
            pending_tasks,
        )
        self.assertEqual(state.active_main_task_id, 9)
        self.assertEqual(state.selected_main_task_id, 9)
        self.assertEqual(state.main_task_pending_sub_tasks, [])
        self.assertEqual(
            state.form_notice,
            "メインタスクとサブタスク2件を登録しました。",
        )
        go_home.assert_called_once_with()

    def test_initial_main_task_without_subtasks_continues_to_subtask_screen(self):
        state = SessionState(
            user_id="user",
            main_task_name="Main quest",
            main_task_due_date=date(2026, 10, 22),
            main_task_pending_sub_tasks=[],
        )
        with (
            patch("pages.quest_forms.st.session_state", state),
            patch(
                "pages.quest_forms.database.create_main_task_with_subtasks",
                return_value=9,
            ) as create_task,
            patch("pages.quest_forms.navigate_to") as navigate_to,
        ):
            _create_main_task()

        create_task.assert_called_once_with(
            "user",
            "Main quest",
            "2026-10-22",
            [],
        )
        navigate_to.assert_called_once_with("sub_task")

    def test_subtask_addition_screen_does_not_render_monster_images(self):
        state = SessionState(
            user_id="user",
            active_main_task_id=4,
            pending_sub_task_main_id=4,
            pending_sub_tasks=[
                {"name": "New step", "priority": "高", "due_date": "2026-10-20"}
            ],
        )
        with (
            patch("pages.quest_forms.st.session_state", state),
            patch(
                "pages.quest_forms.database.list_main_tasks",
                return_value=[{"id": 4, "name": "Main quest"}],
            ),
            patch("pages.quest_forms.st.title"),
            patch("pages.quest_forms.st.write"),
            patch("pages.quest_forms.st.text_input"),
            patch("pages.quest_forms.st.selectbox"),
            patch("pages.quest_forms.st.date_input"),
            patch("pages.quest_forms.st.button"),
            patch("pages.quest_forms.st.markdown"),
            patch("pages.quest_forms.st.image") as image,
        ):
            render_sub_task_form()

        image.assert_not_called()

    def test_registration_saves_pending_tasks_as_one_batch(self):
        pending_tasks = [
            {"name": "Step one", "priority": "高", "due_date": "2026-10-20"},
            {"name": "Step two", "priority": "低", "due_date": "2026-10-21"},
        ]
        state = SessionState(
            user_id="user",
            active_main_task_id=4,
            pending_sub_tasks=pending_tasks.copy(),
        )
        with (
            patch("pages.quest_forms.st.session_state", state),
            patch("pages.quest_forms.database.create_sub_tasks") as create_sub_tasks,
            patch("pages.quest_forms.go_home") as go_home,
        ):
            _register_sub_tasks()

        create_sub_tasks.assert_called_once_with("user", 4, pending_tasks)
        go_home.assert_called_once_with()
        self.assertEqual(state.pending_sub_tasks, [])
        self.assertEqual(state.monster_notice, "モンスターは回復した！")
        self.assertEqual(state.form_notice, "2件のサブタスクを登録しました。")

    def test_home_button_has_home_navigation_label(self):
        state = SessionState(
            user_id="user",
            active_main_task_id=4,
            pending_sub_task_main_id=4,
            pending_sub_tasks=[],
        )
        with (
            patch("pages.quest_forms.st.session_state", state),
            patch(
                "pages.quest_forms.database.list_main_tasks",
                return_value=[{"id": 4, "name": "Main quest"}],
            ),
            patch("pages.quest_forms.database.list_monster_batches", return_value=[]),
            patch("pages.quest_forms.st.title"),
            patch("pages.quest_forms.st.write"),
            patch("pages.quest_forms.st.text_input"),
            patch("pages.quest_forms.st.selectbox"),
            patch("pages.quest_forms.st.date_input"),
            patch("pages.quest_forms.st.markdown"),
            patch("pages.quest_forms.st.button") as button,
        ):
            render_sub_task_form()

        button.assert_any_call("ホームに戻る", on_click=ANY)


if __name__ == "__main__":
    unittest.main()
