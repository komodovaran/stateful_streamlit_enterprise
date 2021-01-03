from __future__ import annotations

import pandas as pd
import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile

from core.core import SessionState, Trace
from lib.serializer import CustomSerializer
from lib.utils import sync_state_after
from pages.app_page import AppPage
from ui import widgets


class LoaderPage(AppPage):
    def __init__(self, serializer: CustomSerializer):
        # Not actually using this for anything. Just demonstrating DI...
        self.serializer = serializer

    @sync_state_after
    def __call__(self, sess: SessionState) -> None:
        st.title(":floppy_disk: Load data here")

        uploaded = widgets.file_uploader("Load file")
        st.write(uploaded)

        sess.data.all_filenames = [file.name for file in uploaded]
        sess.data.selected_filenames = st.multiselect(
            "Select trace(s) to plot",
            sess.data.all_filenames,
            sess.data.selected_filenames,
        )

        traces = [self.parse(file) for file in uploaded]

        sess.data.set_traces(sess.data.all_filenames, traces)

    @staticmethod
    def parse(file: UploadedFile) -> Trace:
        return Trace(name=file.name, data=pd.read_csv(file))
