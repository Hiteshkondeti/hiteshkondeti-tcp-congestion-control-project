
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="TCP Network Optimizer",
    page_icon="🌐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #172554;
}
h1, h2, h3 {
    color: #38bdf8 !important;
}
[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #38bdf8;
}
</style>
""", unsafe_allow_html=True)

st.title("🌐 TCP Network Optimizer")
st.subheader("Network Performance Optimization System")

st.sidebar.title("🌐 Navigation")

page = st.sidebar.radio("Select Page", [
    "Home Dashboard",
    "Network Topology",
    "Network Traffic Data Collection",
    "TCP Congestion Control Analysis",
    "Traffic Management Techniques",
    "Performance Comparison",
    "Conclusion"
])

st.sidebar.divider()
st.sidebar.subheader("Network Configuration")

capacity = st.sidebar.slider(
    "Network Capacity (Mbps)", 10, 100, 50
)

traffic = st.sidebar.slider(
    "Incoming Traffic (Mbps)", 10, 200, 80
)

duration = 10
incoming = traffic * duration
transmitted = min(capacity, traffic) * duration
excess = incoming - transmitted

throughput = transmitted / duration
loss = excess / incoming * 100
queue_time = excess / capacity * 1000
utilization = throughput / capacity * 100

methods = [
    "Without Management",
    "Traffic Shaping",
    "Traffic Policing"
]

comparison = pd.DataFrame({
    "Technique": methods,
    "Throughput (Mbps)": [throughput] * 3,
    "Traffic Loss (%)": [loss, 0, loss],
    "Queue Drain Time (ms)": [0, queue_time, 0],
    "Bandwidth Utilization (%)": [utilization] * 3
})

st.info("Educational Network Simulation | Computer Networks")

# HOME DASHBOARD

if page == "Home Dashboard":

    st.header("🏠 Network Performance Dashboard")

    a, b, c, d = st.columns(4)

    a.metric("Network Capacity", f"{capacity} Mbps")
    b.metric("Incoming Traffic", f"{traffic} Mbps")
    c.metric("Throughput", f"{throughput:.2f} Mbps")
    d.metric("Traffic Loss", f"{loss:.2f}%")

    st.subheader("Project Overview")

    st.write("""
    This project analyzes TCP congestion control
    and traffic management techniques to improve
    network performance, reduce traffic loss,
    and optimize bandwidth utilization.
    """)

    st.subheader("Network Status")

    if traffic > capacity:
        st.error("Network Congestion Detected!")
    else:
        st.success("Network is Operating Normally")

    st.subheader("Bandwidth Utilization")

    st.progress(utilization / 100)
    st.write(f"Bandwidth Utilization: {utilization:.2f}%")

    st.subheader("Traffic Loss Comparison")

    st.bar_chart(
        comparison.set_index("Technique")["Traffic Loss (%)"]
    )


# NETWORK TOPOLOGY

elif page == "Network Topology":

    st.header("🖥️ Network Topology")

    fig, ax = plt.subplots(figsize=(11, 5))

    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    nodes = {
        "Client 1": (1, 4),
        "Client 2": (1, 2.5),
        "Client 3": (1, 1),
        "Switch": (4, 2.5),
        "Router": (7, 2.5),
        "Server": (10, 2.5)
    }

    connections = [
        ("Client 1", "Switch"),
        ("Client 2", "Switch"),
        ("Client 3", "Switch"),
        ("Switch", "Router"),
        ("Router", "Server")
    ]

    for start, end in connections:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]

        ax.plot(
            [x1, x2], [y1, y2],
            color="#38bdf8", linewidth=3
        )

    for name, (x, y) in nodes.items():

        ax.text(
            x, y, name,
            color="white",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.8",
                facecolor="#1e40af",
                edgecolor="#38bdf8"
            )
        )

    ax.text(
        5.5, 3,
        f"{capacity} Mbps",
        color="yellow",
        ha="center"
    )

    ax.set_xlim(-0.2, 11.2)
    ax.set_ylim(0, 5)
    ax.axis("off")

    st.pyplot(fig)
    plt.close(fig)

    st.write("""
    Clients send data through the switch and router
    to the destination server. Congestion occurs
    when incoming traffic exceeds network capacity.
    """)

    st.caption("Conceptual network topology diagram")


# MODULE 1

elif page == "Network Traffic Data Collection":

    st.header("📊 Module 1: Network Traffic Data Collection")

    n = st.slider("Number of Packets", 100, 1000, 500)

    rng = np.random.default_rng(42)

    probability = loss / 100

    status = rng.choice(
        ["Received", "Lost"],
        n,
        p=[1 - probability, probability]
    )

    delays = rng.integers(10, 101, n).astype(float)
    delays[status == "Lost"] = np.nan

    df = pd.DataFrame({
        "Packet ID": range(1, n + 1),
        "Source IP": [
            f"192.168.1.{i}"
            for i in rng.integers(2, 5, n)
        ],
        "Destination IP": "192.168.1.100",
        "Protocol": "TCP",
        "Packet Size (Bytes)": rng.integers(64, 1501, n),
        "Delay (ms)": delays,
        "Status": status
    })

    received = (df["Status"] == "Received").sum()
    lost = (df["Status"] == "Lost").sum()

    a, b, c, d = st.columns(4)

    a.metric("Total Packets", n)
    b.metric("Received Packets", received)
    c.metric("Lost Packets", lost)
    d.metric("Packet Loss", f"{lost/n*100:.2f}%")

    st.subheader("Simulated Network Traffic Dataset")
    st.dataframe(df)

    st.subheader("Average Packet Delay")

    if received > 0:
        st.metric(
            "Average Delay",
            f"{df['Delay (ms)'].mean():.2f} ms"
        )

        st.line_chart(
            df.set_index("Packet ID")["Delay (ms)"]
        )
    else:
        st.warning("No received packets.")

    st.subheader("Packet Status")

    fig, ax = plt.subplots()

    ax.pie(
        [received, lost],
        labels=["Received", "Lost"],
        autopct="%1.1f%%",
        colors=["#22c55e", "#ef4444"]
    )

    st.pyplot(fig)
    plt.close(fig)

    st.download_button(
        "Download Network Dataset",
        df.to_csv(index=False),
        "network_traffic.csv",
        "text/csv"
    )


# MODULE 2

elif page == "TCP Congestion Control Analysis":

    st.header("📈 Module 2: TCP Congestion Control Analysis")

    threshold = st.slider("Slow Start Threshold", 8, 64, 16)
    loss_round = st.slider("Packet Loss Round", 5, 18, 10)

    cwnd = 1
    values = []
    phases = []

    for i in range(1, 21):

        if i == loss_round:

            threshold = max(cwnd // 2, 2)
            cwnd = threshold
            phase = "Fast Recovery (Simplified)"

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

    a, b, c = st.columns(3)

    a.metric("Maximum CWND", max(values))
    b.metric("Average CWND", f"{np.mean(values):.2f}")
    c.metric("Packet Loss Round", loss_round)

    st.subheader("Congestion Window Analysis")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        df["Round"],
        df["CWND"],
        marker="o",
        color="#2563eb",
        linewidth=2
    )

    ax.axvline(
        loss_round,
        color="red",
        linestyle="--",
        label="Packet Loss"
    )

    ax.set_xlabel("Transmission Round")
    ax.set_ylabel("Congestion Window (Packets)")
    ax.set_title("Simplified TCP Reno Simulation")
    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(df)

    st.success("""
    The congestion window is reduced after packet
    loss and gradually increases during recovery.
    """)

    st.download_button(
        "Download TCP Analysis",
        df.to_csv(index=False),
        "tcp_analysis.csv",
        "text/csv"
    )


# MODULE 3

elif page == "Traffic Management Techniques":

    st.header("🚦 Module 3: Traffic Management Techniques")

    technique = st.selectbox(
        "Select Technique", methods
    )

    if technique == "Traffic Shaping":
        queued = excess
        dropped = 0
    else:
        queued = 0
        dropped = excess

    traffic_loss = dropped / incoming * 100
    delay = queued / capacity * 1000

    a, b, c, d = st.columns(4)

    a.metric("Throughput", f"{throughput:.2f} Mbps")
    b.metric("Traffic Loss", f"{traffic_loss:.2f}%")
    c.metric("Queue Drain Time", f"{delay:.2f} ms")
    d.metric("Bandwidth Usage", f"{utilization:.2f}%")

    st.subheader("Traffic Distribution")

    fig, ax = plt.subplots()

    labels = ["Transmitted", "Queued", "Dropped"]
    values = [transmitted, queued, dropped]

    bars = ax.bar(
        labels,
        values,
        color=["#22c55e", "#f59e0b", "#ef4444"]
    )

    ax.bar_label(bars, fmt="%.1f")
    ax.set_ylabel("Traffic (Megabits)")
    ax.set_title("Traffic Management Analysis")

    st.pyplot(fig)
    plt.close(fig)

    if technique == "Traffic Shaping":

        st.success(
            "Traffic shaping queues excess traffic "
            "instead of immediately dropping it."
        )

    elif technique == "Traffic Policing":

        st.warning(
            "Traffic policing drops traffic "
            "that exceeds the configured rate."
        )

    else:

        st.info(
            "Excess traffic is dropped in this "
            "unmanaged network model."
        )


# PERFORMANCE COMPARISON

elif page == "Performance Comparison":

    st.header("📊 Final Performance Comparison")

    st.dataframe(comparison.round(2))

    metrics = [
        "Traffic Loss (%)",
        "Throughput (Mbps)",
        "Queue Drain Time (ms)",
        "Bandwidth Utilization (%)"
    ]

    for metric in metrics:

        fig, ax = plt.subplots(figsize=(8, 4))

        bars = ax.bar(
            ["Unmanaged", "Shaping", "Policing"],
            comparison[metric],
            color=["#ef4444", "#22c55e", "#3b82f6"]
        )

        ax.bar_label(bars, fmt="%.2f", padding=3)
        ax.set_title(metric)
        ax.set_ylabel(metric)
        ax.set_ylim(
            0, max(comparison[metric].max() * 1.2, 1)
        )

        st.pyplot(fig)
        plt.close(fig)

    st.download_button(
        "Download Performance Report",
        comparison.round(2).to_csv(index=False),
        "performance_report.csv",
        "text/csv"
    )


# CONCLUSION

elif page == "Conclusion":

    st.header("📝 Results and Conclusion")

    st.subheader("Final Results")

    st.dataframe(comparison.round(2))

    if traffic > capacity:

        st.success(f"""
        Traffic shaping reduces immediate traffic loss
        from {loss:.2f}% to 0% in this model,
        but requires {queue_time:.2f} ms to drain
        the remaining queued traffic.
        """)

    else:

        st.success("""
        Incoming traffic is within network capacity.
        All three techniques have zero traffic loss
        in this scenario.
        """)

    st.subheader("Conclusion")

    st.write("""
    TCP congestion control regulates the congestion
    window to manage network congestion.

    Traffic shaping reduces immediate traffic loss
    by buffering excess data, while traffic policing
    drops excess traffic.

    Suitable traffic management techniques can
    improve network reliability depending on
    available bandwidth and delay requirements.
    """)

    st.subheader("Future Scope")

    st.write("""
    - Real-time network packet capture
    - TCP Cubic and TCP BBR implementation
    - AI-based network traffic prediction
    - 5G network performance optimization
    """)

    report = f"""
    TCP NETWORK OPTIMIZATION REPORT

    Network Capacity: {capacity} Mbps
    Incoming Traffic: {traffic} Mbps
    Throughput: {throughput:.2f} Mbps
    Unmanaged Traffic Loss: {loss:.2f}%
    Shaping Traffic Loss: 0%
    Shaping Queue Drain Time: {queue_time:.2f} ms

    Conclusion:
    Traffic shaping buffers excess traffic.
    Traffic policing drops excess traffic.
    Throughput is limited by network capacity.

    Note: Results are based on a simplified simulation.
    """

    st.download_button(
        "Download Final Report",
        report,
        "final_report.txt",
        "text/plain"
    )

st.divider()

st.caption(
    "Simulation assumptions: 10-second duration, "
    "unlimited shaping buffer, simplified packet delays. "
    "Not real-time network measurements."
)

st.markdown(
    "**Capstone Project | Computer Networks**"
)
