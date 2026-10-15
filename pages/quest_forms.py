import streamlit as st

import database
from components.navigation import MAIN_TASK, SUB_TASK, go_home, navigate_to


def _create_main_task() -> None:
    name = st.session_state.main_task_name.strip()
    if not name:
        st.session_state.form_error = "メインタスク名を入力してください。"
        return

    pending_tasks = st.session_state.main_task_pending_sub_tasks
    task_id = database.create_main_task_with_subtasks(
        st.session_state.user_id,
        name,
        st.session_state.main_task_due_date.isoformat(),
        pending_tasks,
    )
    st.session_state.active_main_task_id = task_id
    st.session_state.selected_main_task_id = task_id
    st.session_state.main_task_pending_sub_tasks = []
    st.session_state.form_error = None
    if pending_tasks:
        st.session_state.form_notice = (
            f"メインタスクとサブタスク{len(pending_tasks)}件を登録しました。"
        )
        go_home()
    else:
        navigate_to(SUB_TASK)


def _stage_main_task_sub_task() -> None:
    name = st.session_state.main_task_sub_task_name.strip()
    if not name:
        st.session_state.form_error = "サブタスク名を入力してください。"
        return

    st.session_state.main_task_pending_sub_tasks.append(
        {
            "name": name,
            "priority": st.session_state.main_task_sub_task_priority,
            "due_date": st.session_state.main_task_sub_task_due_date.isoformat(),
        }
    )
    st.session_state.main_task_sub_task_name = ""
    st.session_state.form_error = None


def _cancel_main_task_form() -> None:
    st.session_state.main_task_pending_sub_tasks = []
    go_home()


def _stage_sub_task() -> None:
    name = st.session_state.sub_task_name.strip()
    if not name:
        st.session_state.form_error = "サブタスク名を入力してください。"
        return

    st.session_state.pending_sub_tasks.append(
        {
            "name": name,
            "priority": st.session_state.sub_task_priority,
            "due_date": st.session_state.sub_task_due_date.isoformat(),
        }
    )
    st.session_state.sub_task_name = ""
    st.session_state.form_error = None


def _register_sub_tasks() -> None:
    task_id = st.session_state.active_main_task_id
    pending_tasks = st.session_state.pending_sub_tasks
    if not pending_tasks:
        st.session_state.form_error = "登録するサブタスクを「追加」してください。"
        return
    database.create_sub_tasks(
        st.session_state.user_id,
        task_id,
        pending_tasks,
    )
    st.session_state.monster_notice = "モンスターは回復した！"
    st.session_state.pending_sub_tasks = []
    st.session_state.pending_sub_task_main_id = None
    st.session_state.form_notice = f"{len(pending_tasks)}件のサブタスクを登録しました。"
    st.session_state.form_error = None
    go_home()


def render_main_task_form() -> None:
    mode = st.session_state.main_task_mode
    title = "メインタスク追加" if mode == "add" else "メインタスク変更"
    st.title(title)
    st.session_state.setdefault("main_task_pending_sub_tasks", [])
    if st.session_state.get("form_error"):
        st.error(st.session_state.form_error)
    st.text_input(
        "メインタスク名",
        placeholder="例：資格試験に合格する",
        key="main_task_name",
    )
    st.date_input("期限", key="main_task_due_date")
    st.markdown("#### サブタスク")
    st.text_input(
        "サブタスク名",
        placeholder="例：参考書を10ページ読む",
        key="main_task_sub_task_name",
    )
    st.selectbox(
        "重要度",
        ("高", "中", "低"),
        index=1,
        key="main_task_sub_task_priority",
    )
    st.date_input("サブタスク期限", key="main_task_sub_task_due_date")
    st.button("追加", on_click=_stage_main_task_sub_task, type="secondary")
    pending_tasks = st.session_state.main_task_pending_sub_tasks
    if pending_tasks:
        st.markdown("#### 追加中のサブタスク")
        for index, task in enumerate(pending_tasks, start=1):
            st.write(
                f"{index}. {task['name']} · 重要度 {task['priority']} · "
                f"期限 {task['due_date']}"
            )
    st.button("登録", on_click=_create_main_task, type="primary")
    st.button("ホームに戻る", on_click=_cancel_main_task_form)


def render_sub_task_form() -> None:
    user_id = st.session_state.user_id
    tasks = database.list_main_tasks(user_id)
    task_ids = {task["id"] for task in tasks}
    task_id = st.session_state.get("active_main_task_id")
    if task_id not in task_ids:
        task_id = tasks[0]["id"] if tasks else None
        if task_id is not None:
            st.session_state.active_main_task_id = task_id

    st.title("サブタスク追加")
    if st.session_state.get("form_error"):
        st.error(st.session_state.form_error)
    if task_id is None:
        st.info("先にメインタスクを追加してください。")
        st.button(
            "メインタスク追加",
            on_click=navigate_to,
            args=(MAIN_TASK,),
        )
        st.button("ホームに戻る", on_click=go_home)
        return
    if st.session_state.get("pending_sub_task_main_id") != task_id:
        st.session_state.pending_sub_tasks = []
        st.session_state.pending_sub_task_main_id = task_id
    selected_task = next(task for task in tasks if task["id"] == task_id)
    st.write("対象メインタスク:", selected_task["name"])
    st.text_input(
        "サブタスク名",
        placeholder="例：参考書を10ページ読む",
        key="sub_task_name",
    )
    st.selectbox("重要度", ("高", "中", "低"), index=1, key="sub_task_priority")
    st.date_input("期限", key="sub_task_due_date")
    st.button("追加", on_click=_stage_sub_task, type="secondary")
    if st.session_state.pending_sub_tasks:
        st.markdown("#### 追加中のサブタスク")
        for index, task in enumerate(st.session_state.pending_sub_tasks, start=1):
            st.write(
                f"{index}. {task['name']} · 重要度 {task['priority']} · "
                f"期限 {task['due_date']}"
            )
    st.button("登録", on_click=_register_sub_tasks, type="primary")
    st.button("ホームに戻る", on_click=go_home)