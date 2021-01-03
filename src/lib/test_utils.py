from __future__ import annotations

from typing import cast
from unittest.mock import Mock

from mock import patch

from core.core import SessionState
from lib.utils import sync_state_after
from pages.app_page import AppPage


class MockPage(AppPage):
    @sync_state_after
    def __call__(self, sess: SessionState) -> None:
        pass


def test_autosync_decorator_calls_session_state() -> None:
    page: AppPage = MockPage()
    session_state: SessionState = cast(Mock, SessionState)

    with patch.object(
        session_state, SessionState.sync.__name__, return_value=None
    ) as mock:
        page(session_state)
        assert mock.called
