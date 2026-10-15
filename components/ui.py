from pathlib import Path

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
            --quest-ink: #f8f0d8;
            --quest-panel: rgba(20, 28, 43, 0.94);
            --quest-gold: #e5bd67;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: #111827;
            color: var(--quest-ink);
        }
        [data-testid="stHeader"],
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        #MainMenu,
        footer {
            display: none !important;
        }
        [data-testid="stAppViewContainer"] > .main {
            padding-top: 1rem;
        }
        .block-container {
            max-width: 34rem;
            padding: 1rem 1rem 2rem;
        }
        [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] {
            width: 100%;
        }
        div.stButton > button,
        div.stFormSubmitButton > button {
            width: 100%;
            min-height: 2.9rem;
            border: 2px solid var(--quest-gold);
            border-radius: 0.8rem;
            background: linear-gradient(180deg, #405575, #26374f);
            color: #fff8e7;
            font-weight: 700;
            box-shadow: 0 3px 0 #111827;
        }
        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            border-color: #ffe49a;
            color: #fff;
            background: #4b6386;
        }
        [data-testid="stMetric"] {
            padding: 0.8rem;
            border: 1px solid rgba(229, 189, 103, 0.65);
            border-radius: 0.8rem;
            background: var(--quest-panel);
        }
        [data-testid="stDialog"] {
            max-width: min(92vw, 30rem);
        }
        [data-testid="stDialog"] > div {
            background: #19263a;
            border: 1px solid var(--quest-gold);
        }
        [data-testid="stDateInput"] input,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] > div {
            border-radius: 0.65rem;
        }
        [data-testid="stImage"] img {
            max-width: 100%;
            height: auto;
        }
        .quest-panel {
            padding: 1rem;
            border: 1px solid rgba(229, 189, 103, 0.65);
            border-radius: 0.9rem;
            background: var(--quest-panel);
            margin: 0.5rem 0 1rem;
        }
        .quest-muted {
            color: #d4d9e2;
        }
        .calendar-month-heading {
            padding: 0.35rem 0;
            color: var(--quest-ink);
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
        }
        .calendar-weekday {
            padding: 0.35rem 0;
            color: var(--quest-gold);
            font-weight: 700;
            text-align: center;
        }
        .calendar-empty-day {
            min-height: 2.9rem;
        }
        .calendar-quest-list {
            margin: 0.6rem 0 0;
            padding-left: 1.4rem;
        }
        .calendar-quest-list li {
            margin: 0.35rem 0;
        }
        .calendar-quest-completed {
            color: #9ca3af;
            text-decoration-line: line-through;
            text-decoration-style: double;
        }
        [class*="st-key-calendar_day_"] div.stButton > button,
        .st-key-calendar_today div.stButton > button {
            min-height: 2.7rem;
            padding: 0;
            border: 1px solid rgba(229, 189, 103, 0.25);
            border-radius: 0.65rem;
            background: rgba(20, 28, 43, 0.72);
            box-shadow: none;
        }
        .st-key-calendar_today div.stButton > button {
            border-color: rgba(232, 103, 113, 0.65);
            background: rgba(232, 103, 113, 0.28);
            color: #fff1f1;
        }
        [class*="st-key-calendar_day_"] div.stButton > button:hover,
        .st-key-calendar_today div.stButton > button:hover {
            border-color: var(--quest-gold);
            background: rgba(229, 189, 103, 0.2);
            color: #fff;
        }
        @media (max-width: 480px) {
            .block-container {
                padding: 0.7rem 0.8rem 1.5rem;
            }
            h1 {
                font-size: 1.8rem !important;
            }
            h2 {
                font-size: 1.4rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_asset(path: Path, *, width: int = 380) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Required image asset not found: {path}")
    st.image(str(path), width=width)
