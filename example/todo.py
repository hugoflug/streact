from dataclasses import dataclass
from functools import partial

import streact as st


@dataclass
class TodoState:
    todos: list[str]
    text_input: str


@st.component
def todo() -> None:
    state = st.use_state(
        TodoState(
            todos=[],
            text_input="",
        )
    )

    def text_input_updated(val: str) -> None:
        state.text_input = val

    def clear_todos() -> None:
        state.todos.clear()

    def add_todo() -> None:
        if state.text_input:
            state.todos.append(state.text_input)
        state.text_input = ""

    def delete_todo(index: int) -> None:
        state.todos.pop(index)

    for i, todo in enumerate(state.todos):
        st.write(f"- {todo}")
        st.button("Delete", key=f"delete_{i}", on_click=partial(delete_todo, i))
    st.text_input("New todo", set_value=state.text_input, key="new", on_change=text_input_updated)
    st.button("Add todo", key="add", on_click=add_todo)
    st.button("Clear todos", key="clear", on_click=clear_todos)
