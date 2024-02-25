from contextvars import ContextVar
from inspect import currentframe, getframeinfo, signature
from typing import Any, Callable, Optional, TypeVar

import streamlit as st

_current_key: ContextVar = ContextVar("current_key", default=None)


def component(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "key" not in kwargs:
            kwargs["key"] = _source_loc_key()
        if not isinstance(kwargs["key"], str):
            raise ValueError("key must be a string")
        token = _current_key.set(_fully_qualified_key(kwargs["key"], kwargs.get("key_index")))
        if "key" not in signature(func).parameters:
            del kwargs["key"]
        try:
            return func(*args, **kwargs)
        finally:
            _current_key.reset(token)

    return wrapper


T = TypeVar("T")


def use_state(initial: T) -> T:
    key = _current_key.get()
    if key not in st.session_state:
        st.session_state[key] = initial
    return st.session_state[key]


def __getattr__(attr: str) -> Any:
    st_attr = getattr(st, attr)
    if not callable(st_attr) or "key" not in signature(st_attr).parameters:
        return st_attr

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = kwargs.get("key") or _source_loc_key()
        fq_key = _fully_qualified_key(key, kwargs.get("key_index"))
        kwargs["key"] = fq_key
        if "key_index" in kwargs:
            del kwargs["key_index"]
        if "set_value" in kwargs:
            st.session_state[fq_key] = kwargs["set_value"]
            del kwargs["set_value"]
        if (
            "on_change" in kwargs
            and callable(kwargs["on_change"])
            and len(signature(kwargs["on_change"]).parameters) == 1
        ):
            on_change = kwargs["on_change"]
            kwargs["on_change"] = lambda: on_change(st.session_state[fq_key])
        return st_attr(*args, **kwargs)

    return wrapper


def _fully_qualified_key(key: str, index: Optional[int | str] = None) -> str:
    curr = _current_key.get()
    curr_str = curr + "::" if curr else ""
    index_str = "::" + str(index) if index else ""
    return curr_str + key + index_str

def _source_loc_key() -> str:
    caller_frame = getframeinfo(currentframe().f_back.f_back) # type: ignore
    return f"{caller_frame.filename}:{caller_frame.lineno}:{caller_frame.positions.col_offset}" # type: ignore
