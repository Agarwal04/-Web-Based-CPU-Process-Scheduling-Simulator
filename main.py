import streamlit as st
import pandas as pd
import time
import io

from models.process import Process
from algorithms.fcfs import fcfs
from algorithms.sjfs import sjfs
from algorithms.hrrn import hrrn
from algorithms.ljfs import ljfs
from algorithms.lrtf import lrtf
from algorithms.priority import priority
from algorithms.roundrobin import round_robin
from algorithms.srtf import srtf
from assets.gantt_chart import draw_gantt_chart

st.title("CPU Scheduler Simulator")

# Algorithm selection first (to know if priority column is needed)
algo = st.selectbox(
    "Choose Algorithm",
    ["FCFS", "SJF", "HRRN", "LJFS", "LRTF", "Priority", "Round Robin", "SRTF"],
    key="algo"
)

# Number of processes input
n = st.number_input("Number of Processes", min_value=1, step=1, value=3)

# Prepare default data for process table
default_data = {
    "Process ID": [f"P{i+1}" for i in range(n)],
    "Arrival Time": [0 for _ in range(n)],
    "Burst Time": [1 for _ in range(n)],
}

# Add Priority column if needed
if "Priority" in algo:
    default_data["Priority"] = [1 for _ in range(n)]

# Editable DataFrame for process inputs
df = pd.DataFrame(default_data)
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Time Quantum for Round Robin
if algo == "Round Robin":
    time_quantum = st.number_input("Enter Time Quantum", min_value=1, step=1)

if st.button("Run Scheduler"):
    # Convert dataframe rows into Process objects
    processes = []
    try:
        for idx, row in edited_df.iterrows():
            if "Priority" in edited_df.columns:
                p = Process(str(row["Process ID"]), int(row["Arrival Time"]), int(row["Burst Time"]), int(row["Priority"]))
            else:
                p = Process(str(row["Process ID"]), int(row["Arrival Time"]), int(row["Burst Time"]))
            processes.append(p)
    except Exception as e:
        st.error(f"Error parsing input data: {e}")
        st.stop()

    execution_log = []
    scheduled = []

    # Run selected scheduling algorithm
    if algo == "FCFS":
        scheduled, execution_log = fcfs(processes)
    elif algo == "SJF":
        scheduled = sjfs(processes)
    elif algo == "HRRN":
        scheduled = hrrn(processes)
    elif algo == "LJFS":
        scheduled = ljfs(processes)
    elif algo == "LRTF":
        scheduled, execution_log = lrtf(processes)
    elif algo == "Priority":
        scheduled, execution_log = priority(processes)
    elif algo == "Round Robin":
        scheduled, execution_log = round_robin(processes, time_quantum)
    elif algo == "SRTF":
        scheduled, execution_log = srtf(processes)

    # Prepare execution log for display & gantt chart
    if execution_log:
        log = execution_log
    else:
        log = [{"pid": p.pid, "start": p.start, "end": p.completion} for p in scheduled]

    # Display Real-time Execution Log and Progress Bar with improved UI
    st.subheader("Execution Log")
    log_placeholder = st.empty()
    status_text = st.empty()
    progress = st.progress(0)

    logs_display = ""
    for i, entry in enumerate(log):
        line = f"[{entry['start']:>3} - {entry['end']:>3}] ➤ {entry['pid']}"
        logs_display += line + "\n"

        log_placeholder.markdown(
            f"<pre style='background-color:#f0f0f0; padding:10px; border-radius:5px; font-family:monospace;'>{logs_display}</pre>",
            unsafe_allow_html=True,
        )

        progress.progress((i + 1) / len(log))
        time.sleep(2)
    
    status_text.text("Simulation completed!")
    st.success("All processes have finished executing.")

    # Draw Gantt chart
    gif_path = draw_gantt_chart(log, title=f"Gantt Chart - {algo}")
    if gif_path:
        st.image(gif_path)
    else:
        st.warning("Could not generate Gantt chart.")

    # Show process details in a table
    data = []
    for p in scheduled:
        data.append({
            "PID": p.pid,
            "Arrival Time": p.arrival,
            "Burst Time": p.burst,
            "Completion Time": p.completion,
            "Waiting Time": p.waiting,
            "Turnaround Time": p.turnaround
        })

    df_result = pd.DataFrame(data)
    st.subheader("Process Details")
    st.dataframe(df_result)

    # Download button for process details CSV
    csv_buffer = io.StringIO()
    df_result.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="Download Process Details as CSV",
        data=csv_data,
        file_name=f"process_details_{algo}.csv",
        mime="text/csv"
    )

    # Calculate and show averages
    avg_wt = sum(p.waiting for p in scheduled) / len(scheduled)
    avg_tat = sum(p.turnaround for p in scheduled) / len(scheduled)

    st.subheader("Summary")
    st.write(f"**Average Waiting Time:** {avg_wt:.2f}")
    st.write(f"**Average Turnaround Time:** {avg_tat:.2f}")
 
 
