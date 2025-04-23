import streamlit as st
from streamlit_option_menu import option_menu

def center_all_headers():
    st.markdown(
        """
        <style>
            /* Center all header text */
            h1, h2, h3 {
                text-align: center;
                color: #2E7D32; /* Dark Green */
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply to all headers
center_all_headers()

with st.sidebar:
    selected = option_menu(
        menu_title="Algorithm",
        options = ["Intro","FCFS","SJF","Round-Robin","Priority_Scheduling"],
        menu_icon= "emoji-heart-eyes-fill",
        default_index=0,
    )


if selected == "Intro":
    st.header(" :white_check_mark: CPU Scheduling Simulation :clock3:",  divider= 'blue')
    st.markdown('<h2 class="subtitle">An Overview of Different Scheduling Techniques</h2>', unsafe_allow_html=True)

    st.markdown(
        """
        CPU Scheduling is a crucial process in operating systems that determines how CPU time is allocated to processes. 
        Efficient scheduling improves performance and resource utilization. Below are the main types of scheduling algorithms:
        """,
        unsafe_allow_html=True,
    )

    # CPU Scheduling Algorithms Overview
    algorithms = {
        "First Come First Serve (FCFS)": "FCFS is a non-preemptive algorithm where the process that arrives first gets executed first.",
        "Shortest Job First (SJF)": "SJF selects the process with the shortest burst time. Can be preemptive or non-preemptive.",
        "Round Robin (RR)": "RR allocates CPU time to each process in a cyclic order with a fixed time quantum.",
        "Priority Scheduling": "Processes are assigned priority levels. Lower priority numbers get executed first."
       
    }

    # Display Algorithms in a Styled Format
    for algo, desc in algorithms.items():
        with st.container():
            st.markdown(f'<div class="container"><h3>📌 {algo}</h3><p class="description">{desc}</p></div>', unsafe_allow_html=True)

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Developed By-----")
    

    #Profile Section
    col1, col2 = st.columns([1, 2])  

    with col1:
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        st.image("profilePic.jpg", caption="Pritam Paul", width=150)  
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="bio">👋 Hi, I am Pritam Paul, a passionate developer with an interest in Operating Systems and Computer Science. I love building applications that help in understanding complex concepts like CPU Scheduling.</p>', unsafe_allow_html=True)
        st.markdown('<p class="bio">💻 This project is a simple yet powerful tool to visualize different CPU scheduling algorithms.</p>', unsafe_allow_html=True)
        st.markdown('<p class="bio">🚀 Explore the simulation and deepen your understanding!</p>', unsafe_allow_html=True)


if selected == "FCFS":
 
    
    import pandas as pd
    import matplotlib.pyplot as plt

    # Function to simulate FCFS Scheduling
    def fcfs_scheduling(processes):
        # Sort processes by arrival time
        processes.sort(key=lambda x: x[1])  

        n = len(processes)
        c_t = [0] * n
        tAT = [0] * n
        wT = [0] * n
        start_time = [0] * n

        # Track CPU idle times
        timeline = []  # Stores (process_id, start_time, end_time)

        # Calculate Completion Time, Turnaround Time, and Waiting Time
        current_time = 0
        for i in range(n):
            pid, at, bt = processes[i]
            
            # If CPU is idle before this process starts, add idle time to timeline
            if current_time < at:
                timeline.append(("IDLE", current_time, at))
                current_time = at  # Move time to process arrival

            start_time[i] = current_time
            c_t[i] = current_time + bt
            tAT[i] = c_t[i] - at
            wT[i] = tAT[i] - bt

            # Append process execution to timeline
            timeline.append((pid, start_time[i], c_t[i]))
            
            current_time = c_t[i]  # Move time to end of execution

        # Prepare results table
        results = []
        for i in range(n):
            results.append([
                processes[i][0],  # Process ID
                processes[i][1],  # Arrival Time
                processes[i][2],  # Burst Time
                c_t[i],  # Completion Time
                tAT[i],  # Turnaround Time
                wT[i]  # Waiting Time
            ])
        
        return results, timeline

    # Function to plot Gantt Chart including CPU idle time
    def plot_gantt_chart(timeline):
        fig, ax = plt.subplots(figsize=(8, 4))

        for process_id, start, end in timeline:
            color = 'lightgreen' if process_id != "IDLE" else 'lightgray'  # Different color for IDLE time
            ax.barh(y=0, width=end - start, left=start, color=color, edgecolor='black')
            ax.text(start + (end - start) / 2, 0, f"{process_id}", va='center', ha='center', fontsize=12, fontweight='bold')

        ax.set_yticks([])
        ax.set_xticks([t[1] for t in timeline] + [timeline[-1][2]])  # Show start & end times
        ax.set_xlabel("Time")
        ax.set_title("Gantt Chart for FCFS Scheduling (Includes CPU Idle Time)")
        
        st.pyplot(fig)

    # Streamlit App UI
    st.title("✅ FCFS CPU Scheduling Simulator")

    st.write("Enter process details below to simulate **First-Come, First-Served (FCFS)** Scheduling.")

    # User Input for Processes
    num_processes = st.number_input("Number of Processes", min_value=1, max_value=10, value=3, step=1)

    process_list = []
    for i in range(num_processes):
        col1, col2, col3 = st.columns(3)
        with col1:
            pid = st.text_input(f"Process {i+1} ID", f"P{i+1}")
        with col2:
            at = st.number_input(f"Arrival Time (P{i+1})", min_value=0, value=i * 2, step=1)
        with col3:
            bt = st.number_input(f"Burst Time (P{i+1})", min_value=1, value=5, step=1)
        
        process_list.append([pid, at, bt])

    # Run Simulation Button
    if st.button("Simulate FCFS Scheduling"):
        # Run FCFS Algorithm
        results, timeline = fcfs_scheduling(process_list)

        # Convert results to DataFrame
        df = pd.DataFrame(results, columns=["Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"])
        
        st.subheader("📊 Scheduling Results")
        st.write(df)

        st.subheader("📈 Gantt Chart")
        plot_gantt_chart(timeline)

        # Calculate Average Times
        avg_tat = sum([p[4] for p in results]) / len(results)
        avg_wt = sum([p[5] for p in results]) / len(results)
        
        st.write(f"**🔹 Average Turnaround Time:** {avg_tat:.2f}")
        st.write(f"**🔹 Average Waiting Time:** {avg_wt:.2f}")

if selected == "SJF":
    
    import pandas as pd
    import matplotlib.pyplot as plt

    # Function to simulate Non-Preemptive SJF Scheduling
    def sjf_scheduling(processes):
        # Sort processes by arrival time initially
        processes.sort(key=lambda x: x[1])  

        n = len(processes)
        completed = [False] * n
        completion_time = [0] * n
        turnaround_time = [0] * n
        waiting_time = [0] * n
        start_time = [0] * n

        timeline = []  # Stores (process_id, start_time, end_time)
        current_time = 0
        completed_processes = 0

        while completed_processes < n:
            # Find process with shortest burst time among those that have arrived
            ready_queue = [p for p in processes if p[1] <= current_time and not completed[processes.index(p)]]
            
            if not ready_queue:
                # CPU is idle if no process is ready
                next_arrival = min([p[1] for p in processes if not completed[processes.index(p)]])
                timeline.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                continue

            # Choose process with shortest burst time
            ready_queue.sort(key=lambda x: x[2])  
            selected_process = ready_queue[0]
            index = processes.index(selected_process)

            start_time[index] = current_time
            completion_time[index] = current_time + selected_process[2]
            turnaround_time[index] = completion_time[index] - selected_process[1]
            waiting_time[index] = turnaround_time[index] - selected_process[2]
            completed[index] = True
            completed_processes += 1

            # Append process execution to timeline
            timeline.append((selected_process[0], start_time[index], completion_time[index]))
            
            current_time = completion_time[index]  # Move time forward

        # Prepare results table
        results = []
        for i in range(n):
            results.append([
                processes[i][0],  # Process ID
                processes[i][1],  # Arrival Time
                processes[i][2],  # Burst Time
                completion_time[i],  # Completion Time
                turnaround_time[i],  # Turnaround Time
                waiting_time[i]  # Waiting Time
            ])
        
        return results, timeline

    # Function to plot Gantt Chart including CPU idle time
    def plot_gantt_chart(timeline):
        fig, ax = plt.subplots(figsize=(8, 4))

        for process_id, start, end in timeline:
            color = 'lightblue' if process_id != "IDLE" else 'lightgray'  # Different color for IDLE time
            ax.barh(y=0, width=end - start, left=start, color=color, edgecolor='black')
            ax.text(start + (end - start) / 2, 0, f"{process_id}", va='center', ha='center', fontsize=12, fontweight='bold')

        ax.set_yticks([])
        ax.set_xticks([t[1] for t in timeline] + [timeline[-1][2]])  # Show start & end times
        ax.set_xlabel("Time")
        ax.set_title("Gantt Chart for SJF Scheduling (Includes CPU Idle Time)")
        
        st.pyplot(fig)

    # Streamlit App UI
    st.title("🔹 SJF CPU Scheduling Simulator (Non-Preemptive)")

    st.write("Enter process details below to simulate **Shortest Job First (SJF)** Scheduling.")

    # User Input for Processes
    num_processes = st.number_input("Number of Processes", min_value=1, max_value=10, value=3, step=1)

    process_list = []
    for i in range(num_processes):
        col1, col2, col3 = st.columns(3)
        with col1:
            pid = st.text_input(f"Process {i+1} ID", f"P{i+1}")
        with col2:
            at = st.number_input(f"Arrival Time (P{i+1})", min_value=0, value=i * 2, step=1)
        with col3:
            bt = st.number_input(f"Burst Time (P{i+1})", min_value=1, value=5, step=1)
        
        process_list.append([pid, at, bt])

    # Run Simulation Button
    if st.button("Simulate SJF Scheduling"):
        # Run SJF Algorithm
        results, timeline = sjf_scheduling(process_list)

        # Convert results to DataFrame
        df = pd.DataFrame(results, columns=["Process ID", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"])
        
        st.subheader("📊 Scheduling Results")
        st.write(df)

        st.subheader("📈 Gantt Chart")
        plot_gantt_chart(timeline)

        # Calculate Average Times
        avg_tat = sum([p[4] for p in results]) / len(results)
        avg_wt = sum([p[5] for p in results]) / len(results)
        
        st.write(f"**🔹 Average Turnaround Time:** {avg_tat:.2f}")
        st.write(f"**🔹 Average Waiting Time:** {avg_wt:.2f}")



if selected == "Round-Robin":
    st.write("Hii")
if selected == "Priority_Scheduling":
    st.write("Hii")