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


def render_monster(
    root: Path,
    subtasks: list[dict],
    recovery_message: str | None = None,
) -> None:
    max_hp = calculate_max_hp(subtasks)
    current_hp = calculate_current_hp(subtasks)
    hp_ratio = current_hp / max_hp if max_hp else 0
    monster_name = (
        "デフォルトドラゴン.png"
        if current_hp > 0
        else "デフォルトドラゴン_敗北.png"
    )
    monster_path = root / "assets" / "monsters" / "defolt" / monster_name
    if max_hp == 0:
        status_message = "モンスターをやっつけた！"
    elif current_hp == max_hp:
        status_message = "モンスターがあらわれた！"
    elif current_hp == 0:
        status_message = "モンスターをやっつけた！"
    else:
        status_message = None

    with st.container():
        centered_column = st.columns([1, 2, 1])[1]
        with centered_column:
            st.progress(hp_ratio, text=f"HP {current_hp} / {max_hp}")
            st.image(str(monster_path), width=250)
    if status_message:
        st.markdown(
            f'<p style="text-align:center;font-weight:700">{status_message}</p>',
            unsafe_allow_html=True,
        )
    if recovery_message:
        st.caption(recovery_message)