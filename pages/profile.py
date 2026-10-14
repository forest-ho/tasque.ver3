from pathlib import Path

import streamlit as st

import database
from components.navigation import back_button
from components.ui import show_asset


def render_profile(root: Path) -> None:
    profile = database.get_user_profile(st.session_state.user_id)
    st.title("プロフィール")
    st.metric("プレイヤーレベル", f"Lv. {profile['level']}")
    st.markdown(
        '<div class="quest-panel"><strong>冒険者</strong>'
        '<br><span class="quest-muted">プロフィール・アイコンは仮表示です。</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("#### アイコン")
    show_asset(root / "assets" / "ui" / "プロフィール.png")
    st.button("アイコンを変更（準備中）", disabled=True)
    back_button()