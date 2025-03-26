import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from a_star_task_scheduler import Task, AStarTaskScheduler

def main():
    st.title("A* Task Scheduler")
    
    # Sidebar for task input
    st.sidebar.header("📋 Task Configuration")
    
    # Session state to store tasks
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    
    # Task input fields
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        task_name = st.text_input("Task Name")
    
    with col2:
        task_duration = st.number_input("Duration", min_value=1, step=1)
    
    # Dependency selection
    if st.session_state.tasks:
        dependencies = st.sidebar.multiselect(
            "Select Dependencies", 
            [task.name for task in st.session_state.tasks]
        )
    else:
        dependencies = []
    
    # Add task button
    if st.sidebar.button("Add Task"):
        if task_name and task_duration:
            new_task = Task(task_name, task_duration, dependencies)
            st.session_state.tasks.append(new_task)
        else:
            st.sidebar.warning("Please enter task name and duration")
    
    # Display current tasks
    if st.session_state.tasks:
        task_data = [
            {
                "Task Name": task.name, 
                "Duration": task.duration, 
                "Dependencies": ", ".join(task.dependencies or ["None"])
            } 
            for task in st.session_state.tasks
        ]
        df = pd.DataFrame(task_data)
        st.sidebar.dataframe(df)
    
    # Main area for scheduling and results
    st.header("🚀 Scheduling Results")
    
    # Scheduling section
    if st.button("Run A* Scheduling"):
        if st.session_state.tasks:
            try:
                # Initialize scheduler
                scheduler = AStarTaskScheduler(st.session_state.tasks)
                
                # Perform A* scheduling
                schedule = scheduler.a_star_schedule()
                
                # Display scheduling results
                results_df = pd.DataFrame(
                    schedule, 
                    columns=["Task", "Start Time", "End Time"]
                )
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Tasks", len(schedule))
                with col2:
                    st.metric("Total Time", results_df['End Time'].max())
                with col3:
                    st.metric("Earliest Finish", results_df['End Time'].min())
                
                # Results table
                st.subheader("Scheduling Details")
                st.dataframe(results_df)
                
                # Gantt Chart
                st.subheader("📊 Task Timeline")
                fig = create_gantt_chart(schedule)
                st.plotly_chart(fig)
            
            except Exception as e:
                st.error(f"Scheduling Error: {e}")
        else:
            st.warning("Please add tasks before scheduling")

def create_gantt_chart(schedule):
    """Create an interactive Gantt chart for task schedule."""
    df = []
    for task, start, end in schedule:
        df.append(dict(Task=task, Start=start, Finish=end))
    
    fig = ff.create_gantt(
        df, 
        index_col='Task', 
        show_colorbar=True, 
        group_tasks=True,
        title='Task Scheduling Gantt Chart'
    )
    
    fig.update_layout(
        height=400,
        title_x=0.5,
        xaxis_title="Time",
        yaxis_title="Tasks"
    )
    
    return fig

if __name__ == "__main__":
    main()