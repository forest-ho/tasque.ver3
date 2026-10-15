from pathlib import Path

import streamlit as st

import database
from components.menu import open_menu, show_menu_if_open
from components.monster import render_monster
from components.navigation import CALENDAR, navigate_to
from components.task_list import render_sub_tasks


def render_home(root: Path) -> None:
    user_id = st.session_state.user_id
    profile = database.get_user_profile(user_id)
    tasks = database.list_main_tasks(user_id)
    tasks_by_id = {task["id"]: task for task in tasks}
    st.title("ホーム")
    st.button("☰ メニューを開く", on_click=open_menu, key="home_menu_button")
    if st.session_state.selected_main_task_id not in tasks_by_id:
        st.session_state.selected_main_task_id = tasks[0]["id"] if tasks else None
    if tasks:
        selected_index = list(tasks_by_id).index(
            st.session_state.selected_main_task_id
        )
        st.selectbox(
            "メインタスクを選択",
            options=list(tasks_by_id),
            index=selected_index,
            format_func=lambda task_id: tasks_by_id[task_id]["name"],
            key="selected_main_task_id",
        )
    current_task = tasks_by_id.get(st.session_state.selected_main_task_id)
    if current_task:
        st.session_state.active_main_task_id = current_task["id"]
    st.metric("プレイヤーレベル", f"Lv. {profile['level']}")
    st.button("📅 カレンダー", on_click=navigate_to, args=(CALENDAR,))
    subtasks = (
        database.list_sub_tasks(user_id, current_task["id"])
        if current_task
        else []
    )
    if not tasks:
        st.info("メインタスクをつくってモンスター狩りをはじめよう！")
    elif current_task:
        st.caption("メインタスクのHP")
        render_monster(
            root,
            subtasks,
            st.session_state.pop("monster_notice", None),
        )
    render_sub_tasks(
        subtasks,
        user_id,
        current_task["id"] if current_task else None,
    )
    notice = st.session_state.pop("form_notice", None)
    if notice:
        st.success(notice)
    show_menu_if_open()