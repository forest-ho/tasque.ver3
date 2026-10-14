import streamlit as st

from components.navigation import go_home


def render_calendar() -> None:
    st.title("カレンダー")
    selected = st.date_input("日付を選択", key="calendar_picker")
    st.session_state.selected_date = selected
    st.markdown(
        f'<div class="quest-panel"><strong>{selected:%Y年%m月%d日} のクエスト</strong>'
        '<br><span class="quest-muted">この日のクエスト情報はまだありません。</span></div>',
        unsafe_allow_html=True,
    )
    st.button("⌂ ホームに戻る", on_click=go_home)