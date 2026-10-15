import unittest
from datetime import date
from unittest.mock import Mock, patch

from components.menu import _menu_button
from components.navigation import (
    CALENDAR,
    HOME,
    MAIN_TASK,
    TITLE,
    change_calendar_month,
    go_back,
    go_home,
    initialize_navigation,
    navigate_to,
    open_main_task,
    select_calendar_date,
    set_calendar_picker_month,
)


class SessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __setattr__(self, name, value):
        self[name] = value


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.state = SessionState()
        initialize_navigation(self.state)
        session_patch = patch("components.navigation.st.session_state", self.state)
        session_patch.start()
        self.addCleanup(session_patch.stop)

    def test_navigation_and_back_restore_origin(self):
        navigate_to(HOME)
        navigate_to(MAIN_TASK)

        go_back()

        self.assertEqual(self.state["screen"], HOME)
        self.assertEqual(self.state["screen_history"], [TITLE])

    def test_go_home_clears_navigation_history_and_menu(self):
        navigate_to(HOME)
        navigate_to(CALENDAR)
        self.state["menu_open"] = True

        go_home()

        self.assertEqual(self.state["screen"], HOME)
        self.assertEqual(self.state["screen_history"], [])
        self.assertFalse(self.state["menu_open"])

    def test_unknown_screen_is_rejected(self):
        with self.assertRaises(ValueError):
            navigate_to("unknown")

    def test_open_main_task_adds_screen_and_sets_add_mode(self):
        navigate_to(HOME)
        self.state["menu_open"] = True

        open_main_task("add")

        self.assertEqual(self.state["screen"], MAIN_TASK)
        self.assertEqual(self.state["main_task_mode"], "add")
        self.assertFalse(self.state["menu_open"])
        self.assertEqual(self.state["screen_history"], [TITLE, HOME])

    def test_menu_button_action_reruns_the_app(self):
        action = Mock()
        with (
            patch("components.menu.st.button", return_value=True),
            patch("components.menu.st.rerun") as rerun,
        ):
            _menu_button("メインタスク追加", action, "add")

        action.assert_called_once_with("add")
        rerun.assert_called_once_with(scope="app")

    def test_calendar_month_navigation_handles_year_boundaries(self):
        self.state["calendar_month"] = date(2026, 12, 1)

        change_calendar_month(1)
        self.assertEqual(self.state["calendar_month"], date(2027, 1, 1))

        change_calendar_month(-1)
        change_calendar_month(-1)
        self.assertEqual(self.state["calendar_month"], date(2026, 11, 1))

    def test_selecting_calendar_day_updates_selected_date_and_month(self):
        selected = date(2027, 2, 14)

        select_calendar_date(selected)

        self.assertEqual(self.state["selected_date"], selected)
        self.assertEqual(self.state["calendar_picker"], selected)
        self.assertEqual(self.state["calendar_month"], date(2027, 2, 1))

    def test_calendar_picker_change_updates_displayed_month(self):
        selected = date(2027, 4, 9)
        self.state["calendar_picker"] = selected

        set_calendar_picker_month()

        self.assertEqual(self.state["selected_date"], selected)
        self.assertEqual(self.state["calendar_month"], date(2027, 4, 1))


if __name__ == "__main__":
    unittest.main()
