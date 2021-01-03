from typing import Any

import jsonpickle
import jsonpickle.ext.numpy

jsonpickle.ext.numpy.register_handlers()


class CustomSerializer:
    @staticmethod
    def serialize(obj: Any) -> None:
        jsonpickle.encode(obj)

    @staticmethod
    def deserialize(obj: Any) -> Any:
        return jsonpickle.decode(obj)
