from dataclasses import dataclass

import streact as st


@dataclass
class CounterState:
    value: int


@st.component
def counter(title: str) -> None:
    state = st.use_state(CounterState(value=0))

    st.header(title)

    def button_clicked():
        state.value += 1

    st.button("Click", key="click", on_click=button_clicked)
    st.write(f"Clicked {state.value} times")
