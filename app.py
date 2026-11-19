import streamlit as st

st.title("TCP Congestion Control")
st.subheader("Network Performance Optimization")

st.sidebar.title("Project Modules")

st.sidebar.radio("Select Module", [
    "Network Traffic Data Collection",
    "TCP Congestion Control Analysis",
    "Traffic Management Techniques"
])

st.success("Project successfully running!")
