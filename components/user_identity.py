import uuid

import streamlit as st

COOKIE_NAME = "tasque_browser_user"
COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 365 * 5


def parse_user_id(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return None
    if str(parsed) != value.lower():
        return None
    return str(parsed)


def ensure_browser_user_id() -> str:
    user_id = parse_user_id(st.context.cookies.get(COOKIE_NAME))
    if user_id is None:
        user_id = str(uuid.uuid4())
        st.info("ブラウザーごとのユーザーデータを準備しています…")
        st.iframe(
            f"""
            <script>
            const secure = window.location.protocol === "https:" ? "; Secure" : "";
            document.cookie = "{COOKIE_NAME}={user_id}; "
                + "Path=/; Max-Age={COOKIE_MAX_AGE_SECONDS}; SameSite=Lax" + secure;
            const saved = document.cookie.split("; ").some(
                value => value === "{COOKIE_NAME}={user_id}"
            );
            if (saved) {{
                window.parent.location.reload();
            }} else {{
                document.body.innerText =
                    "ユーザー識別用Cookieを保存できません。ブラウザーのCookie設定をご確認ください。";
                document.body.style.cssText =
                    "font: 14px sans-serif; color: #fff; padding: 8px;";
            }}
            </script>
            """,
            height=48,
        )
        st.stop()
    st.session_state.user_id = user_id
    return user_id
