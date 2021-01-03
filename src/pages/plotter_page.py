from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.pyplot import Figure, Axes

from core.core import SessionState
from lib.utils import sync_state_after, timeit
from pages.app_page import AppPage


class PlotterPage(AppPage):
    def __init__(self) -> None:
        pass

    @sync_state_after
    def __call__(self, sess: SessionState) -> None:
        st.title(":icecream: Plotting page")
        st.subheader(":point_left: Select traces to plot from *Load files*")
        traces = sess.data.get_selected_traces()

        if traces:
            st.header("Traces")
            selected_traces_array = sess.data.traces_to_array(traces, use_y_fit=False)
            if selected_traces_array is not None:
                self.plot(selected_traces_array, color="black")

            st.header("Fits")
            fitted_traces_array = sess.data.traces_to_array(traces, use_y_fit=True)
            if fitted_traces_array is not None:
                self.plot(fitted_traces_array, color="firebrick")
            else:
                st.subheader("There are no fits!")

    @staticmethod
    def plot(traces: np.ndarray[np.float64], color: str) -> None:
        ypts = traces
        xpts = np.linspace(0, ypts.shape[1], ypts.shape[1])

        fig: Figure
        ax: Axes

        fig, ax = plt.subplots()
        for n in range(ypts.shape[0]):
            ax.plot(xpts, ypts[n, ...], alpha=0.5, color=color)  # type: ignore

        st.write(fig)
