from typing import List

import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile


def file_uploader(label: str) -> List[UploadedFile]:
    files: List[UploadedFile] = st.file_uploader(
        label=label,
        accept_multiple_files=True,
    )
    return files


def select_box(label: str, options: List[str]) -> str:
    selected: str = st.selectbox(label, options)
    return selected
