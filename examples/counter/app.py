import streact as st

from examples.counter.counter import counter

t1, t2 = st.tabs(["Counter 1", "Counter2"])
with t1:
    counter("My counter", key="counter1")
with t2:
    counter("My other counter", key="counter2")