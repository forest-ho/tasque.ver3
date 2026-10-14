import unittest
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

    def test_render_displays_hp_frame_and_current_over_max(self):
        with (
            patch("components.monster.st.markdown") as markdown,
            patch(
                "components.monster._image_data_url",
                side_effect=["data:image/png;base64,frame", "data:image/png;base64,monster"],
            ) as image_data_url,
        ):
            render_monster(ROOT, [
                {"priority": "中", "completed": False},
                {"priority": "低", "completed": False},
            ])

        html = markdown.call_args.args[0]
        self.assertIn('aria-label="HP 30/30"', html)
        self.assertIn(">30 / 30</span>", html)
        self.assertIn("mask-image:url('data:image/png;base64,frame')", html)
        self.assertNotIn('class="monster-hp-frame"', html)
        self.assertIn('class="monster-art"', html)
        self.assertIn("background:#38c76b", html)
        self.assertEqual(
            image_data_url.call_args_list[1].args[0],
            ROOT / "assets" / "monsters" / "defolt" / "デフォルトドラゴン.png",
        )

    def test_render_shows_empty_hp_for_monster_without_subtasks(self):
        with (
            patch("components.monster.st.markdown") as markdown,
            patch(
                "components.monster._image_data_url",
                side_effect=["data:image/png;base64,frame", "data:image/png;base64,monster"],
            ) as image_data_url,
        ):
            render_monster(ROOT, [])

        html = markdown.call_args.args[0]
        self.assertIn('aria-label="HP 0/0"', html)
        self.assertIn(">0 / 0</span>", html)
        self.assertIn("background:#e34848", html)
        self.assertEqual(
            image_data_url.call_args_list[1].args[0],
            ROOT / "assets" / "monsters" / "defolt" / "デフォルトドラゴン_敗北.png",
        )


if __name__ == "__main__":
    unittest.main()
