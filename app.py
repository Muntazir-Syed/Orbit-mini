import streamlit as st
import pandas as pd
import plotly.express as px

from modules.goals import *
from modules.tasks import *
from modules.coach import ask_orbit

st.set_page_config(
    page_title="Orbit Mini",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 Orbit")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Goals",
        "Tasks",
        "AI Coach",
        "Analytics"
    ]
)

# =========================
# DASHBOARD
# =========================

if page == "Dashboard":

    st.title("🚀 Orbit Dashboard")

    goals = load_goals()
    tasks = load_tasks()

    completed = sum(
        1 for t in tasks
        if t["completed"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Goals", len(goals))
    col2.metric("Tasks", len(tasks))
    col3.metric("Completed", completed)

    st.divider()

    st.subheader("Recent Goals")

    if goals:
        for goal in goals[-5:]:
            st.write("🎯", goal)
    else:
        st.info("No goals added yet.")

# =========================
# GOALS
# =========================

elif page == "Goals":

    st.title("🎯 Goals")

    goal = st.text_input(
        "Enter Goal"
    )

    if st.button("Add Goal"):

        if goal.strip():
            add_goal(goal)
            st.success("Goal Added")
            st.rerun()

    st.subheader("Your Goals")

    goals = load_goals()

    if goals:
        for g in goals:
            st.write("✅", g)
    else:
        st.info("No goals available.")

# =========================
# TASKS
# =========================

elif page == "Tasks":

    st.title("📝 Tasks")

    task_input = st.text_input(
        "Enter Task"
    )

    if st.button("Add Task"):

        if task_input.strip():
            add_task(task_input)
            st.rerun()

    st.subheader("Task List")

    tasks = load_tasks()

    changed = False

    for i, task in enumerate(tasks):

        completed = st.checkbox(
            task["task"],
            value=task["completed"],
            key=f"task_{i}"
        )

        if completed != task["completed"]:
            tasks[i]["completed"] = completed
            changed = True

    if changed:
        save_tasks(tasks)

# =========================
# AI COACH
# =========================

elif page == "AI Coach":

    st.title("🤖 Orbit AI Coach")

    prompt = st.text_area(
        "Ask Orbit anything",
        height=150,
        placeholder="Example: I have many goals but keep procrastinating. What should I do?"
    )

    if st.button("Get Advice"):

        if prompt.strip():

            with st.spinner("Orbit is thinking..."):

                response = ask_orbit(prompt)

            st.subheader("Response")
            st.write(response)

        else:
            st.warning("Please enter a question.")

# =========================
# ANALYTICS
# =========================

elif page == "Analytics":

    st.title("📊 Analytics")

    tasks = load_tasks()

    completed = sum(
        1 for t in tasks
        if t["completed"]
    )

    pending = len(tasks) - completed

    df = pd.DataFrame(
        {
            "Status": [
                "Completed",
                "Pending"
            ],
            "Count": [
                completed,
                pending
            ]
        }
    )

    fig = px.pie(
        df,
        names="Status",
        values="Count",
        title="Task Completion"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )