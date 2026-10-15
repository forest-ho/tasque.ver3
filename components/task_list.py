from html import escape

import streamlit as st

import database


def render_sub_tasks(
    tasks: list[dict],
    user_id: str | None = None,
    main_task_id: int | None = None,
) -> None:
    st.markdown("#### 🧭 サブタスク")
    if not tasks:
        st.markdown(
            '<div class="quest-panel"><span class="quest-muted">'
            "サブタスクはここに表示されます。</span></div>",
            unsafe_allow_html=True,
        )
        return
    for task in tasks:
        if task["completed"]:
            st.markdown(
                f'<span style="color:#9ca3af;text-decoration:line-through">'
                f"✓ {escape(task['name'])} · 優先度 {task['priority']} · "
                f"期限 {task['due_date']}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.button(
                task["name"],
                key=f"complete_sub_task_{task['id']}",
                on_click=database.complete_sub_task,
                args=(user_id, main_task_id, task["id"]),
            )
            st.caption(f"優先度 {task['priority']} · 期限 {task['due_date']}")