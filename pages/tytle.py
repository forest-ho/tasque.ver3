from pathlib import Path

import streamlit as st

from components.navigation import HOME, navigate_to
from components.ui import show_asset


def render_title() -> None:
    st.write("")
    show_asset(Path(__file__).resolve().parents[1] / "assets" / "ui" / "ロゴ.png")
    st.title("たすくえ")
    st.markdown(
        '<div class="quest-panel">毎日のタスクを、冒険に変えよう。</div>',
        unsafe_allow_html=True,
    )
    st.button("冒険をはじめる", on_click=navigate_to, args=(HOME,), type="primary")