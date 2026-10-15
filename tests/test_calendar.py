import unittest
from datetime import date
from unittest.mock import patch

from pages.calender import render_daily_quests


class CalendarQuestTests(unittest.TestCase):
    def test_daily_quests_are_listed_with_completed_style_and_escaped_names(self):
        tasks = [
            {"name": "Active quest", "completed": False},
            {"name": "<Finished & safe>", "completed": True},
        ]

        with patch("pages.calender.st.markdown") as markdown:
            render_daily_quests(date(2026, 10, 15), tasks)

        html = markdown.call_args.args[0]
        self.assertIn("<ul class=\"calendar-quest-list\">", html)
        self.assertIn("<li class=\"\">Active quest</li>", html)
        self.assertIn(
            '<li class="calendar-quest-completed">'
            "&lt;Finished &amp; safe&gt;</li>",
            html,
        )

    def test_empty_day_shows_no_quests_message(self):
        with patch("pages.calender.st.markdown") as markdown:
            render_daily_quests(date(2026, 10, 15), [])

        self.assertIn("この日のクエストはありません。", markdown.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
