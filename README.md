# Streact

Making **st**reamlit a little more like **react**, by adding reusable components with local state.

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
    st.text_input("New todo", set_value=state.new_todo, on_change=new_todo_updated)
    st.button("Add todo", on_click=add_todo)

```

More examples can found in [examples](examples).

# Docs
Streact consists of a few new functions, as well as some extensions to the built-in elements in Streamlit.

To use Streact, instead of:

`import streamlit as st`

use

 `import streact as st`

## New functions

### @st.component

The `component` decorator declares a function to be a component. In Streamlit, all keys must be globally unique. Inside a Streact component, keys are only required to be unique within that component. When calling a component function, you must always specify `key` as a key word argument.

### st.use_state
`use_state` returns the current component's state. As input, it takes the initial value of the state. Unlike in React, there is no `set_state`. Just mutate the state directly instead.

## Extensions to Streamlit

Streact extends the functionality of Streamlit input elements (the ones with a `key` parameter):

### on_change
In Streamlit, callbacks have no arguments. In Streact, `on_change` callbacks can optionally take a single argument. If provided, it will be set to the current value of the element.

### set_value
Input elements have a new `set_value` parameter. This will set the value of the element to the provided value. Note how this is different from `value`, which only decides the initial value of the element on first render.

## Streamlit features not supported

Outside of a component, Streact is backwards-compatible with Streamlit. Inside a component:
- The value of an element can no longer be found at `st.session_state[key]`. Use `on_change` callbacks to keep track of element values instead.
- Calling methods on the values returned from layout elements like `columns` or `tabs` is not supported. Instead, use `with` notation.
I.e. instead of:
```python
c1, c2 = st.columns(2)
c1.write("hello!")
```
do
```python
c1, c2 = st.columns(2)
with c1:
    st.write("hello!)
```
