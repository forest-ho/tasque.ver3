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
        user_id = parse_user_id(st.session_state.get("user_id"))
        if user_id is not None:
            if not st.session_state.get("browser_user_cookie_warning_shown"):
                st.warning(
                    "ブラウザーのCookieをアプリ側で確認できません。"
                    "このセッション中はデータを利用できますが、"
                    "次回も同じユーザーデータを利用できない場合があります。"
                )
                st.session_state["browser_user_cookie_warning_shown"] = True
            return user_id

        user_id = str(uuid.uuid4())
        st.session_state["user_id"] = user_id
        st.info("ブラウザーごとのユーザーデータを準備しています…")
        st.html(
            f"""
            <script>
            const cookiePolicy = window.location.protocol === "https:"
                ? "; SameSite=None; Secure"
                : "; SameSite=Lax";
            const reloadAttemptKey = "tasque_browser_user_reload_attempted";
            document.cookie = "{COOKIE_NAME}={user_id}; "
                + "Path=/; Max-Age={COOKIE_MAX_AGE_SECONDS}" + cookiePolicy;
            const saved = document.cookie.split("; ").some(
                value => value === "{COOKIE_NAME}={user_id}"
            );
            const reloadAttempted =
                sessionStorage.getItem(reloadAttemptKey) === "1";
            if (saved && !reloadAttempted) {{
                sessionStorage.setItem(reloadAttemptKey, "1");
                window.location.reload();
            }} else if (saved) {{
                document.currentScript.insertAdjacentText(
                    "afterend",
                    "Cookieは保存されましたが、アプリ側で確認できません。ブラウザーのCookie設定をご確認のうえ、ページを再読み込みしてください。"
                );
            }} else {{
                document.currentScript.insertAdjacentText(
                    "afterend",
                    "ユーザー識別用Cookieを保存できません。ブラウザーのCookie設定をご確認ください。"
                );
            }}
            </script>
            """,
            unsafe_allow_javascript=True,
        )
    st.session_state["user_id"] = user_id
    return user_id
