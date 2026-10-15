from datetime import date

import streamlit as st

TITLE = "title"
HOME = "home"
CALENDAR = "calendar"
MAIN_TASK = "main_task"
SUB_TASK = "sub_task"
PROFILE = "profile"
VALID_SCREENS = {TITLE, HOME, CALENDAR, MAIN_TASK, SUB_TASK, PROFILE}


def initialize_navigation(state) -> None:
    state.setdefault("screen", TITLE)
    state.setdefault("screen_history", [])
    state.setdefault("menu_open", False)
    state.setdefault("main_task_mode", "add")
    state.setdefault("selected_main_task_id", None)
    state.setdefault("selected_date", date.today())
    state.setdefault("calendar_picker", state["selected_date"])
    state.setdefault(
        "calendar_month",
        date(state["selected_date"].year, state["selected_date"].month, 1),
    )


def change_calendar_month(offset: int) -> None:
    current = st.session_state.calendar_month
    month_index = current.year * 12 + current.month - 1 + offset
    year, month = divmod(month_index, 12)
    st.session_state.calendar_month = date(year, month + 1, 1)


def select_calendar_date(selected: date) -> None:
    st.session_state.selected_date = selected
    st.session_state.calendar_picker = selected
    st.session_state.calendar_month = date(selected.year, selected.month, 1)


def set_calendar_picker_month() -> None:
    selected = st.session_state.calendar_picker
    st.session_state.selected_date = selected
    st.session_state.calendar_month = date(selected.year, selected.month, 1)


def navigate_to(screen: str) -> None:
    if screen not in VALID_SCREENS:
        raise ValueError(f"Unknown screen: {screen}")

    current = st.session_state.screen
    if current != screen:
        st.session_state.screen_history.append(current)
        st.session_state.screen = screen
    st.session_state.menu_open = False


def open_main_task(mode: str) -> None:
    if mode not in {"add", "edit"}:
        raise ValueError(f"Unknown main task mode: {mode}")
    st.session_state.main_task_mode = mode
    navigate_to(MAIN_TASK)


def go_back() -> None:
    history = st.session_state.screen_history
    if history:
        st.session_state.screen = history.pop()
    else:
        st.session_state.screen = HOME
    st.session_state.menu_open = False


def go_home() -> None:
    st.session_state.screen = HOME
    st.session_state.screen_history.clear()
    st.session_state.menu_open = False


def back_button(label: str = "← 戻る") -> None:
    st.button(label, on_click=go_back, key=f"back_{st.session_state.screen}")