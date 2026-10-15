import unittest
from unittest.mock import patch

from components.navigation import go_home
from pages.profile import render_profile


class ProfilePageTests(unittest.TestCase):
    def test_profile_page_shows_development_notice_and_home_button(self):
        with (
            patch("pages.profile.st.title") as title,
            patch("pages.profile.st.info") as info,
            patch("pages.profile.st.button") as button,
        ):
            render_profile()

        title.assert_called_once_with("プロフィール")
        info.assert_called_once_with("プロフィール画面は現在開発中です。")
        button.assert_called_once_with("⌂ ホームに戻る", on_click=go_home)


if __name__ == "__main__":
    unittest.main()
