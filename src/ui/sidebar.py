from typing import List, cast

import streamlit as st


def radio_button(title: str, options: List[str]) -> str:
    return cast(str, st.sidebar.radio(title, options))
