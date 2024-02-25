from dataclasses import dataclass
from functools import partial
from typing import Optional

import streact as st


@dataclass
class TodoState:
    todos: list[str]
    new_todo_input: str
    edit_todo_input: str
    editing_index: Optional[int]

@st.component
def todo() -> None:
    state = st.use_state(
        TodoState(
            todos=[],
            new_todo_input="",
            edit_todo_input="",
            editing_index=None,
        )
    )

    def new_todo_added(val: str) -> None:
        state.todos.append(val)
        state.new_todo_input = ""

    def clear_todos_clicked() -> None:
        state.todos.clear()

    def edit_todo_clicked(i: int) -> None:
        state.editing_index = i
        state.edit_todo_input = state.todos[i]

    def delete_todo_clicked(i: int) -> None:
        state.todos.pop(i)

    def todo_edited(i: int, val: str) -> None:
        state.todos[i] = val
        state.editing_index = None
        state.edit_todo_input = ""

    for i, todo in enumerate(state.todos):
        if state.editing_index == i:
            st.text_input("Edit todo", set_value=state.edit_todo_input, key=f"edit_input_{i}", on_change=partial(todo_edited, i))
        else:
            st.write(f"- {todo}")
        c1, c2, _ = st.columns([0.15, 0.15, 0.7])
        with c1:
            st.button("Edit", key=f"edit_{i}", on_click=partial(edit_todo_clicked, i), disabled=state.editing_index is not None)
        with c2:
            st.button("Delete", key=f"delete_{i}", on_click=partial(delete_todo_clicked, i), disabled=state.editing_index is not None)
    st.text_input("New todo", set_value=state.new_todo_input, on_change=new_todo_added)
    st.button("Clear todos", on_click=clear_todos_clicked)
