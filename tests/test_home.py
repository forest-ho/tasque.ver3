import unittest
from pathlib import Path
from unittest.mock import patch

from pages.home import render_home


class SessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __setattr__(self, name, value):
        self[name] = value


class HomePageTests(unittest.TestCase):
    def test_home_selects_first_task_and_renders_aggregate_monster_hp(self):
        tasks = [
            {"id": 4, "name": "First quest", "due_date": "2026-10-20"},
            {"id": 7, "name": "Second quest", "due_date": "2026-10-21"},
        ]
        subtasks = [
            {"id": 3, "priority": "高", "completed": False},
            {"id": 4, "priority": "低", "completed": True},
        ]
        state = SessionState(
            user_id="user",
            selected_main_task_id=None,
            monster_notice="モンスターは回復した！",
        )

        with (
            patch("pages.home.st.session_state", state),
            patch("pages.home.st.title"),
            patch("pages.home.st.button", return_value=False),
            patch("pages.home.st.selectbox") as selectbox,
            patch("pages.home.st.metric"),
            patch("pages.home.st.success"),
            patch(
                "pages.home.database.get_user_profile",
                return_value={"level": 1},
            ),
            patch("pages.home.database.list_main_tasks", return_value=tasks),
            patch("pages.home.database.list_sub_tasks", return_value=subtasks),
            patch("pages.home.render_monster") as render_monster,
            patch("pages.home.render_sub_tasks"),
            patch("pages.home.show_menu_if_open"),
        ):
            render_home(Path("/project"))

        self.assertEqual(state.selected_main_task_id, 4)
        self.assertEqual(state.active_main_task_id, 4)
        self.assertEqual(selectbox.call_args.kwargs["index"], 0)
        render_monster.assert_called_once_with(
            Path("/project"),
            subtasks,
            "モンスターは回復した！",
        )
        self.assertNotIn("monster_notice", state)


if __name__ == "__main__":
    unittest.main()
