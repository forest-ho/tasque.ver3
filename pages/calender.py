import calendar
from datetime import date
from html import escape

import jpholiday
import streamlit as st

import database
from components.navigation import (
    change_calendar_month,
    go_home,
    select_calendar_date,
    set_calendar_picker_month,
)


def _calendar_day_class(displayed_date: date) -> str:
    if jpholiday.is_holiday(displayed_date):
        return "holiday"
    if displayed_date.weekday() == 5:
        return "saturday"
    if displayed_date.weekday() == 6:
        return "sunday"
    return "weekday"


def render_daily_quests(selected: date, tasks: list[dict]) -> None:
    if tasks:
        quest_items = "".join(
            f'<li class="{"calendar-quest-completed" if task["completed"] else ""}">'
            f"{escape(task['name'])}</li>"
            for task in tasks
        )
        content = f"<ul class=\"calendar-quest-list\">{quest_items}</ul>"
    else:
        content = '<span class="quest-muted">この日のクエストはありません。</span>'
    st.markdown(
        f'<div class="quest-panel"><strong>'
        f"{selected:%Y年%m月%d日} のクエスト</strong>{content}</div>",
        unsafe_allow_html=True,
    )


def render_calendar() -> None:
    shown_month = st.session_state.calendar_month
    previous, month_heading, following = st.columns([1, 4, 1])
    with previous:
        st.button(
            "‹",
            key="calendar_previous_month",
            help="前の月",
            on_click=change_calendar_month,
            args=(-1,),
        )
    with month_heading:
        st.markdown(
            f'<div class="calendar-month-heading">'
            f"{shown_month.year}年{shown_month.month}月</div>",
            unsafe_allow_html=True,
        )
    with following:
        st.button(
            "›",
            key="calendar_next_month",
            help="次の月",
            on_click=change_calendar_month,
            args=(1,),
        )

    with st.container(key="calendar_grid"):
        weekday_columns = st.columns(7)
        for column, weekday in zip(
            weekday_columns,
            ("月", "火", "水", "木", "金", "土", "日"),
        ):
            with column:
                st.markdown(
                    f'<div class="calendar-weekday">{weekday}</div>',
                    unsafe_allow_html=True,
                )

        today = date.today()
        for week in calendar.monthcalendar(shown_month.year, shown_month.month):
            day_columns = st.columns(7)
            for column, day_number in zip(day_columns, week):
                with column:
                    if day_number == 0:
                        st.markdown(
                            '<div class="calendar-empty-day">&nbsp;</div>',
                            unsafe_allow_html=True,
                        )
                        continue
                    displayed_date = date(
                        shown_month.year,
                        shown_month.month,
                        day_number,
                    )
                    today_marker = "_today" if displayed_date == today else ""
                    cell_key = (
                        f"calendar_day_{_calendar_day_class(displayed_date)}"
                        f"{today_marker}_{displayed_date:%Y%m%d}"
                    )
                    with st.container(key=cell_key):
                        st.button(
                            str(day_number),
                            key=f"calendar_select_{displayed_date:%Y%m%d}",
                            on_click=select_calendar_date,
                            args=(displayed_date,),
                        )

    selected = st.date_input(
        "日付を選択",
        key="calendar_picker",
        on_change=set_calendar_picker_month,
    )
    st.session_state.selected_date = selected
    tasks = database.list_main_tasks_due_on(
        st.session_state.user_id,
        selected.isoformat(),
    )
    render_daily_quests(selected, tasks)
    st.button("⌂ ホームに戻る", on_click=go_home)