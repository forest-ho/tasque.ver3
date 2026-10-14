from pathlib import Path

import streamlit as st

import database
from components.navigation import (
    CALENDAR,
    HOME,
    MAIN_TASK,
    PROFILE,
    SUB_TASK,
    TITLE,
    initialize_navigation,
)
from components.user_identity import ensure_browser_user_id
from components.ui import inject_styles, show_loading_overlay
from pages.calender import render_calendar
from pages.home import render_home
from pages.profile import render_profile
from pages.quest_forms import render_main_task_form, render_sub_task_form
from pages.tytle import render_title

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="たすくえ",
    page_icon="🐉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

initialize_navigation(st.session_state)
inject_styles()
user_id = ensure_browser_user_id()
database.ensure_user(user_id)
loading_overlay = st.empty()
with loading_overlay.container():
    show_loading_overlay(ROOT / "assets" / "ui" / "ローディング.png")

try:
    screen = st.session_state.screen
    if screen == TITLE:
        render_title()
    elif screen == HOME:
        render_home(ROOT)
    elif screen == CALENDAR:
        render_calendar()
    elif screen == MAIN_TASK:
        render_main_task_form()
    elif screen == SUB_TASK:
        render_sub_task_form()
    elif screen == PROFILE:
        render_profile(ROOT)
    else:
        st.session_state.screen = TITLE
        render_title()
finally:
    loading_overlay.empty()