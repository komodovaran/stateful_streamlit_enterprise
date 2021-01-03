from __future__ import annotations

from abc import ABC
from typing import Optional, Any, Dict, Union, List

import numpy as np
import pandas as pd
from streamlit.hashing import _CodeHasher
from streamlit.report_session import ReportSession
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server


class BaseSessionState(ABC):
    """
    Adapted from https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92

    This object is very dynamic in order to set and retrieve any value, at any time,
    so it inherits from AvailableSessionItems to provide reliable types and autocomplete
    """

    def __init__(
        self,
        session: Union[SessionState, ReportSession],
    ) -> None:

        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize session data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item: Any) -> Optional[Any]:
        """Return a saved session value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item: Any) -> Any:
        """Return a saved session value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item: str, value: Any) -> None:
        """Set session value."""
        self._state["data"][item] = value

    def __setattr__(self, item: str, value: Any) -> None:
        """Set session value."""
        self._state["data"][item] = value

    def clear(self) -> None:
        """Clear session session and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self) -> None:
        """
        Rerun the app with all session values up to date from the beginning to fix
        rollbacks.
        """

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing session value at each run.
        #
        # Example: session.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


class LoadedData:
    """Typesafe container for loaded data"""

    _traces: Dict[str, Trace] = {}

    all_filenames: List[str] = []
    selected_filenames: List[str] = []

    def set_traces(self, names: List[str], traces: List[Trace]) -> None:
        for name, trace in zip(names, traces):
            if name in self._traces:
                continue
            self._traces[name] = trace

        self.all_filenames = names

    def get_trace(self, name: str) -> Trace:
        return self._traces[name]

    def set_trace(self, trace: Trace) -> None:
        self._traces[trace.name] = trace

    def get_all_traces(self) -> List[Trace]:
        return list(self._traces.values())

    def get_selected_traces(self) -> List[Trace]:
        return [self._traces[name] for name in self.selected_filenames]

    def clear_single_fit(self, name: str) -> None:
        self._traces[name].clear_fit()

    def clear_all_fits(self) -> None:
        for name in self.all_filenames:
            self._traces[name].clear_fit()

    @staticmethod
    def traces_to_array(
        traces: List[Trace], use_y_fit: bool
    ) -> Optional[np.ndarray[np.float64]]:

        if not traces:
            return None

        if use_y_fit:
            y_data = [trace.y_fit.values for trace in traces if trace.y_fit is not None]
            if not y_data:
                return None
        else:
            y_data = [trace.y.values for trace in traces]
        return np.stack(y_data)


class SessionState(BaseSessionState):
    """A catalogue to provide type-safe access to certain attributes"""

    def __init__(
        self,
        session: Union[SessionState, ReportSession],
        data: LoadedData,
    ):
        super().__init__(session)
        self.data: LoadedData = data


def _get_report_session() -> ReportSession:
    try:
        session_id: str = get_report_ctx().session_id
    except AttributeError:
        raise RuntimeError("Couldn't start Streamlit application.")
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def get_session_state() -> SessionState:
    """Gets the session state that is fed through the main call entrypoint"""

    streamlit_session = _get_report_session()
    loaded_data_cache = LoadedData()

    if not hasattr(streamlit_session, "_custom_session_state"):
        streamlit_session._custom_session_state = SessionState(
            streamlit_session,
            loaded_data_cache,
        )

    session_state: SessionState = streamlit_session._custom_session_state

    return session_state


class Trace:
    """A single trace entity"""

    def __init__(self, name: str, data: pd.DataFrame):
        self.name = name
        self.data = self._validate_data(data)
        self.x: pd.Series[float] = self.data["x"]
        self.y: pd.Series[float] = self.data["y"]
        self.y_fit: Optional[np.ndarray[np.float64]] = None

    @staticmethod
    def _validate_data(data: pd.DataFrame) -> pd.DataFrame:
        for c in "x", "y":
            if c not in data.columns:
                raise ValueError
        return data

    def clear_fit(self) -> None:
        self.y_fit = None
