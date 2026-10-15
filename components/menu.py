from collections.abc import Callable

import streamlit as st

from components.navigation import (
    CALENDAR,
    PROFILE,
    SUB_TASK,
    navigate_to,
    open_main_task,
)


def _menu_button(
    label: str,
    action: Callable[..., None],
    *args: object,
) -> None:
    if st.button(label):
        action(*args)
        st.rerun(scope="app")


@st.dialog("メニュー")
def _menu_dialog() -> None:
    _menu_button("メインタスク追加", open_main_task, "add")
    _menu_button("サブタスク追加", navigate_to, SUB_TASK)
    _menu_button("プロフィール", navigate_to, PROFILE)
    _menu_button("カレンダー", navigate_to, CALENDAR)
    _menu_button("閉じる", _close_menu)


def _close_menu() -> None:
    st.session_state.menu_open = False


def open_menu() -> None:
    st.session_state.menu_open = True


def show_menu_if_open() -> None:
    if st.session_state.menu_open:
        _menu_dialog()