# Streact

Making **st**reamlit a little more like **react**, by adding component-local state and more user-friendly callbacks.

It looks like this:
```python
from dataclasses import dataclass
import streact as st

@dataclass
class TodoState:
    todos: list[str]
    new_todo: str

@st.component
def todo():
    state = st.use_state(
        TodoState(
            todos=[],
            new_todo=""
        )
    )

    def new_todo_updated(val: str):
        state.new_todo = val

    def add_todo():
        state.todos.append(state.new_todo)
        state.new_todo = ""

    for todo in state.todos:
        st.write(f"- {todo}")
    st.text_input("New todo", set_value=state.text_input, on_change=new_todo_updated)
    st.button("Add todo", on_click=add_todo)

```

To use, instead of:

`import streamlit as st`

use

 `import streact as st`

## New functions

### @st.component

The `component` decorator declares a function to be a component. Inside a component, all keys are only required to be unique within that component. Note that when calling a component function, you must always specify `key` as a key word argument.

### st.use_state
`use_state` returns the current component's state. As input, it takes the initial value of the state. Unlike in React, there is no `set_state`. Just mutate the state directly instead.

## Extensions to Streamlit input elements

Streact extends the functionality of Streamlit input elements (the ones with a `key` parameter):

### on_change
`on_change` callbacks can now optionally take a single argument. If provided, it will be set to the current value of the element.

### set_value
Input elements have a new `set_value` parameter. This will set the value of the element to the provided value. Note how this is different from `value`, which only decides the initial value of the element on first render.