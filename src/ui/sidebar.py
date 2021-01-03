from typing import List, cast

import streamlit as st


def sidebar_title(title: str) -> None:
    st.sidebar.title(title)


def radio_button(title: str, options: List[str]) -> str:
    return cast(str, st.sidebar.radio(title, options))
