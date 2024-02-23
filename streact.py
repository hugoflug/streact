from contextvars import ContextVar
from inspect import signature
from typing import Any, Callable, TypeVar

import streamlit as st

_current_key: ContextVar = ContextVar("current_key", default=None)


def component(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "key" not in kwargs:
            raise ValueError(
                "functions decorated with @st.component must be called with the keyword argument 'key'"
            )
        token = _current_key.set(_fully_qualified_key(kwargs["key"]))
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
    if not callable(st_attr):
        return st_attr

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "key" in kwargs:
            kwargs["key"] = _fully_qualified_key(kwargs["key"])
            if "set_value" in kwargs:
                st.session_state[kwargs["key"]] = kwargs["set_value"]
                del kwargs["set_value"]
            if (
                "on_change" in kwargs
                and callable(kwargs["on_change"])
                and len(signature(kwargs["on_change"]).parameters) == 1
            ):
                on_change = kwargs["on_change"]
                kwargs["on_change"] = lambda: on_change(st.session_state[kwargs["key"]])
        return st_attr(*args, **kwargs)

    return wrapper


def _fully_qualified_key(key: str) -> str:
    curr = _current_key.get()
    return f"{curr}::{key}" if curr else key
