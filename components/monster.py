import base64
from pathlib import Path

import streamlit as st


HP_BY_PRIORITY = {"高": 50, "中": 20, "低": 10}


def calculate_max_hp(subtasks: list[dict]) -> int:
    return sum(HP_BY_PRIORITY[task["priority"]] for task in subtasks)


def calculate_current_hp(subtasks: list[dict]) -> int:
    return sum(
        HP_BY_PRIORITY[task["priority"]]
        for task in subtasks
        if not task["completed"]
    )


def _image_data_url(path: Path) -> str:
    image_data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{image_data}"


def render_monster(root: Path, subtasks: list[dict]) -> None:
    max_hp = calculate_max_hp(subtasks)
    current_hp = calculate_current_hp(subtasks)
    hp_ratio = current_hp / max_hp if max_hp else 0
    hp_color = "#38c76b" if hp_ratio > 0.4 else "#e34848"
    hp_bar = _image_data_url(root / "assets" / "ui" / "HPバー.png")
    monster = _image_data_url(
        root
        / "assets"
        / "monsters"
        / "defolt"
        / (
            "デフォルトドラゴン.png"
            if current_hp > 0
            else "デフォルトドラゴン_敗北.png"
        )
    )

    st.markdown(
        f"""
        <div class="monster-display">
            <div class="monster-hp-bar" role="img"
                 aria-label="HP {current_hp}/{max_hp}">
                <div class="monster-hp-track"
                     style="-webkit-mask-image:url('{hp_bar}');mask-image:url('{hp_bar}')">
                    <div class="monster-hp-fill"
                         style="width:{hp_ratio * 100}%;background:{hp_color}"></div>
                </div>
                <span class="monster-hp-label">{current_hp} / {max_hp}</span>
            </div>
            <img class="monster-art" src="{monster}" alt="モンスター">
        </div>
        """,
        unsafe_allow_html=True,
    )