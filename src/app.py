from typing import Dict

import streamlit as st

from core.core import get_session_state, SessionState
from lib.serializer import CustomSerializer
from lib.utils import sync_state_after
from pages.app_page import AppPage
from pages.fit_page import FitterPage
from pages.loader_page import LoaderPage
from pages.plotter_page import PlotterPage
from ui import sidebar


class Main(AppPage):
    @sync_state_after
    def __call__(self, sess: SessionState) -> None:
        pages: Dict[str, AppPage] = {
            "Load files": LoaderPage(serializer=CustomSerializer()),
            "Fit": FitterPage(),
            "Plot": PlotterPage(),
        }

        st.sidebar.title(":floppy_disk: Page states")
        selected_page = sidebar.radio_button("Select your page", list(pages.keys()))

        self.display_page_with_session(sess, pages, selected_page)

    @staticmethod
    def display_page_with_session(
        sess: SessionState, pages: Dict[str, AppPage], selected_page: str
    ) -> None:
        pages[selected_page](sess)


if __name__ == "__main__":
    Main()(get_session_state())
