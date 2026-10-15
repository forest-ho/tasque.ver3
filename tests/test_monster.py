import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

from components.monster import (
    calculate_current_hp,
    calculate_max_hp,
    render_monster,
)


ROOT = Path(__file__).resolve().parents[1]


class MonsterTests(unittest.TestCase):
    def test_max_hp_is_the_sum_of_subtask_priorities(self):
        self.assertEqual(
            calculate_max_hp(
                [
                    {"priority": "高"},
                    {"priority": "中"},
                    {"priority": "低"},
                    {"priority": "高"},
                ]
            ),
            130,
        )

    def test_max_hp_is_zero_without_subtasks(self):
        self.assertEqual(calculate_max_hp([]), 0)

    def test_completed_subtasks_reduce_current_hp_by_priority(self):
        self.assertEqual(
            calculate_current_hp(
                [
                    {"priority": "高", "completed": True},
                    {"priority": "中", "completed": False},
                    {"priority": "低", "completed": False},
                ]
            ),
            30,
        )

    def test_render_displays_hp_progress_and_current_over_max(self):
        with (
            patch(
                "components.monster.st.columns",
                return_value=[nullcontext(), nullcontext(), nullcontext()],
            ),
            patch("components.monster.st.container", return_value=nullcontext()),
            patch("components.monster.st.markdown") as markdown,
            patch("components.monster.st.progress") as progress,
            patch("components.monster.st.image") as image,
            patch("components.monster.st.caption") as caption,
        ):
            render_monster(
                ROOT,
                [
                    {"priority": "中", "completed": False},
                    {"priority": "低", "completed": False},
                ],
                "モンスターは回復した！",
            )

        progress.assert_called_once_with(1, text="HP 30 / 30")
        markdown.assert_called_once_with(
            '<p style="text-align:center;font-weight:700">'
            "モンスターがあらわれた！</p>",
            unsafe_allow_html=True,
        )
        image.assert_called_once_with(
            str(ROOT / "assets" / "monsters" / "defolt" / "デフォルトドラゴン.png"),
            width=250,
        )
        caption.assert_called_once_with("モンスターは回復した！")

    def test_render_shows_empty_hp_for_monster_without_subtasks(self):
        with (
            patch(
                "components.monster.st.columns",
                return_value=[nullcontext(), nullcontext(), nullcontext()],
            ),
            patch("components.monster.st.container", return_value=nullcontext()),
            patch("components.monster.st.markdown") as markdown,
            patch("components.monster.st.progress") as progress,
            patch("components.monster.st.image") as image,
        ):
            render_monster(ROOT, [])

        progress.assert_called_once_with(0, text="HP 0 / 0")
        markdown.assert_called_once_with(
            '<p style="text-align:center;font-weight:700">'
            "モンスターをやっつけた！</p>",
            unsafe_allow_html=True,
        )
        image.assert_called_once_with(
            str(
                ROOT
                / "assets"
                / "monsters"
                / "defolt"
                / "デフォルトドラゴン_敗北.png"
            ),
            width=250,
        )

    def test_render_aggregates_all_subtask_batches_as_one_monster(self):
        with (
            patch(
                "components.monster.st.columns",
                return_value=[nullcontext(), nullcontext(), nullcontext()],
            ),
            patch("components.monster.st.container", return_value=nullcontext()),
            patch("components.monster.st.markdown") as markdown,
            patch("components.monster.st.progress") as progress,
            patch("components.monster.st.image") as image,
        ):
            render_monster(
                ROOT,
                [
                    {"priority": "低", "completed": False},
                    {"priority": "高", "completed": True},
                ],
            )

        progress.assert_called_once_with(10 / 60, text="HP 10 / 60")
        markdown.assert_not_called()
        image.assert_called_once_with(
            str(ROOT / "assets" / "monsters" / "defolt" / "デフォルトドラゴン.png"),
            width=250,
        )


if __name__ == "__main__":
    unittest.main()
