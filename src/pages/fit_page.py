from __future__ import annotations

from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.optimize import curve_fit

from core.core import SessionState, Trace
from lib.utils import sync_state_after
from pages.app_page import AppPage
from ui import widgets


class FitterPage(AppPage):
    def __init__(self) -> None:
        pass

    @sync_state_after
    def __call__(self, sess: SessionState) -> None:
        st.title(":rocket: Single trace fitting page")

        selection = widgets.select_box("Select trace to fit", sess.data.all_filenames)
        if selection is None:
            return

        selected_trace = sess.data.get_trace(selection)

        fit_single = st.button("Fit current trace")
        fit_all = st.button("Fit all traces")
        clear_single = st.button("Clear current fit")
        clear_all = st.button("Clear all fits")

        if fit_single:
            self._fit_single(selection, sess)

        if clear_single:
            sess.data.clear_single_fit(selection)

        if fit_all:
            self._fit_all(sess)

        if clear_all:
            sess.data.clear_all_fits()

        self.plot(selected_trace)

    def _fit_single(self, selection: str, sess: SessionState) -> None:
        fitted_trace = self.fit(self.line, sess.data.get_trace(selection))
        sess.data.set_trace(fitted_trace)

    def _fit_all(self, sess: SessionState) -> None:
        traces = sess.data.get_all_traces()
        for trace in traces:
            fitted_trace = self.fit(self.line, trace)
            sess.data.set_trace(fitted_trace)

    @staticmethod
    def line(
        x: np.ndarray[np.float64], slope: float, intercept: float
    ) -> np.ndarray[np.float64]:
        return slope * x + intercept

    @staticmethod
    def fit(f: Callable, trace: Trace) -> Trace:
        popt, pcov = curve_fit(f, xdata=trace.x, ydata=trace.y)

        trace.y_fit = f(trace.x, *popt)

        return trace

    @staticmethod
    def plot(trace: Trace) -> None:
        x = trace.x.values
        y = trace.y.values

        fig, ax = plt.subplots()

        ax.plot(x, y, color="black")
        if trace.y_fit is not None:
            y_fit: np.ndarray[np.float64] = trace.y_fit.values
            ax.plot(x, y_fit, color="firebrick", linestyle="-")

        st.write(fig)
