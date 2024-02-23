
import streact as st
from example.counter import counter
from example.todo import todo

st.write("# TODO app")
todo(key="todo")

st.divider()

st.write("# Counters")
counter("One", key="one")
counter("Two", key="two")

