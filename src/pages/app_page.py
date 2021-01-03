from abc import ABC, abstractmethod

from core.core import SessionState


class AppPage(ABC):
    """
    An application page. Each application page class must be a callable function
    to the nature of Streamlit
    """

    @abstractmethod
    def __call__(self, sess: SessionState) -> None:
        raise NotImplementedError
