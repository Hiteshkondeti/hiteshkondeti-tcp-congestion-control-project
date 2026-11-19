
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TCP Network Analysis", layout="wide")

st.title("🌐 TCP Congestion Control")
st.subheader("Network Performance Optimization")

st.sidebar.title("Project Modules")

module = st.sidebar.radio("Select Module", [
    "Network Traffic Data Collection",
    "TCP Congestion Control Analysis",
    "Traffic Management Techniques"
])

if module == "Network Traffic Data Collection":

    st.header("Module 1: Network Traffic Data Collection")

    n = st.slider("Number of Packets", 100, 1000, 500)

    rng = np.random.default_rng(42)

    df = pd.DataFrame({
        "Packet ID": range(1, n+1),
        "Packet Size (Bytes)": rng.integers(64, 1501, n),
        "Delay (ms)": rng.integers(10, 101, n),
        "Status": rng.choice(
            ["Received", "Lost"], n, p=[0.95, 0.05]
        )
    })

    st.info("Using simulated network traffic data.")

    st.dataframe(df)

    loss = (df["Status"] == "Lost").mean() * 100

    a, b, c = st.columns(3)

    a.metric("Total Packets", n)
    b.metric("Average Delay", f"{df['Delay (ms)'].mean():.2f} ms")
    c.metric("Packet Loss", f"{loss:.2f}%")

    st.line_chart(df.set_index("Packet ID")["Delay (ms)"])

    st.download_button(
        "Download Network Dataset",
        df.to_csv(index=False),
        "network_traffic.csv",
        "text/csv"
    )

elif module == "TCP Congestion Control Analysis":

    st.header("Module 2: TCP Congestion Control Analysis")

    threshold = st.slider("Slow Start Threshold", 8, 64, 16)
    loss_round = st.slider("Packet Loss Round", 5, 18, 10)

    cwnd = 1
    values = []
    phases = []

    for i in range(1, 21):

        if i == loss_round:
            threshold = max(cwnd // 2, 2)
            cwnd = threshold
            phase = "Simplified Fast Recovery"

        elif cwnd < threshold:
            cwnd = min(cwnd * 2, threshold)
            phase = "Slow Start"

        else:
            cwnd += 1
            phase = "Congestion Avoidance"

        values.append(cwnd)
        phases.append(phase)

    df = pd.DataFrame({
        "Round": range(1, 21),
        "CWND": values,
        "Phase": phases
    })

    st.info("Simplified TCP Reno-style simulation")

    st.line_chart(df.set_index("Round")["CWND"])

    st.dataframe(df)

    st.metric("Maximum Congestion Window", max(values))

elif module == "Traffic Management Techniques":

    st.header("Module 3: Traffic Management Techniques")

    bandwidth = st.slider("Network Capacity (Mbps)", 10, 100, 50)

    traffic = st.slider("Incoming Traffic (Mbps)", 10, 200, 80)

    technique = st.selectbox("Select Technique", [
        "Without Traffic Management",
        "Traffic Shaping",
        "Traffic Policing"
    ])

    duration = 10
    incoming = traffic * duration
    transmitted = min(traffic, bandwidth) * duration
    excess = incoming - transmitted

    if technique == "Traffic Shaping":
        queued = excess
        dropped = 0
    else:
        queued = 0
        dropped = excess

    loss = dropped / incoming * 100
    throughput = transmitted / duration
    delay = queued / bandwidth * 1000

    a, b, c = st.columns(3)

    a.metric("Throughput", f"{throughput:.2f} Mbps")
    b.metric("Traffic Loss", f"{loss:.2f}%")
    c.metric("Queue Drain Time", f"{delay:.2f} ms")

    df = pd.DataFrame({
        "Traffic": ["Transmitted", "Queued", "Dropped"],
        "Megabits": [transmitted, queued, dropped]
    })

    st.bar_chart(df.set_index("Traffic"))

    st.dataframe(df)

    st.info("Simplified traffic model over 10 seconds with unlimited shaping buffer.")

st.divider()
st.caption("Capstone Project | Computer Networks")
