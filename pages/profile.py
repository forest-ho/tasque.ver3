import streamlit as st

from components.navigation import go_home


def render_profile() -> None:
    st.title("プロフィール")
    st.info("プロフィール画面は現在開発中です。")
    st.button("⌂ ホームに戻る", on_click=go_home)
