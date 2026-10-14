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
        .st-key-loading-overlay {
            position: fixed;
            inset: 0;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #111827;
        }
        .st-key-loading-overlay [data-testid="stVerticalBlock"] {
            width: 100%;
            align-items: center;
        }
        .st-key-loading-overlay [data-testid="stElementContainer"] {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        .st-key-loading-overlay [data-testid="stImage"] {
            width: min(72vw, 20rem);
            margin-inline: auto;
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
        .monster-display {
            width: min(100%, 280px);
            margin: 0 auto 1rem;
        }
        .monster-hp-bar {
            position: relative;
            width: 100%;
            height: 24px;
            margin: 0 auto 0.4rem;
        }
        .monster-hp-track {
            position: absolute;
            top: 8px;
            right: 0;
            left: 0;
            height: 8px;
            overflow: hidden;
            background: #382a31;
            -webkit-mask-position: center;
            mask-position: center;
            -webkit-mask-size: 100% 24px;
            mask-size: 100% 24px;
            -webkit-mask-repeat: no-repeat;
            mask-repeat: no-repeat;
        }
        .monster-hp-fill {
            height: 100%;
        }
        .monster-hp-label {
            position: absolute;
            inset: 0;
            z-index: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 0.8rem;
            font-weight: 700;
            line-height: 1;
            text-shadow: 0 1px 2px #000, 0 0 3px #000;
        }
        .monster-art {
            display: block;
            width: 250px;
            max-width: 100%;
            height: auto;
            margin: 0 auto;
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


def show_loading_overlay(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Required image asset not found: {path}")
    with st.container(key="loading-overlay"):
        st.image(str(path), width=320)
