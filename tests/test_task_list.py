import unittest
from unittest.mock import patch

from components.task_list import _complete_sub_task, render_sub_tasks


class SessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __setattr__(self, name, value):
        self[name] = value


class TaskListTests(unittest.TestCase):
    def test_completed_subtask_sets_damage_message_using_priority_hp(self):
        state = SessionState()
        with (
            patch("components.task_list.st.session_state", state),
            patch(
                "components.task_list.database.complete_sub_task",
                return_value=True,
            ) as complete_sub_task,
        ):
            _complete_sub_task("user", 8, 12, "高")

        complete_sub_task.assert_called_once_with("user", 8, 12)
        self.assertEqual(state.monster_notice, "モンスターに50のダメージ！")

    def test_already_completed_subtask_does_not_set_damage_message(self):
        state = SessionState()
        with (
            patch("components.task_list.st.session_state", state),
            patch(
                "components.task_list.database.complete_sub_task",
                return_value=False,
            ),
        ):
            _complete_sub_task("user", 8, 12, "低")

        self.assertNotIn("monster_notice", state)

    def test_active_subtask_button_passes_priority_to_callback(self):
        with (
            patch("components.task_list.st.markdown"),
            patch("components.task_list.st.button") as button,
            patch("components.task_list.st.caption"),
        ):
            render_sub_tasks(
                [
                    {
                        "id": 12,
                        "name": "Read a chapter",
                        "priority": "中",
                        "due_date": "2026-10-20",
                        "completed": False,
                    }
                ],
                "user",
                8,
            )

        button.assert_called_once_with(
            "Read a chapter",
            key="complete_sub_task_12",
            on_click=_complete_sub_task,
            args=("user", 8, 12, "中"),
        )


if __name__ == "__main__":
    unittest.main()
