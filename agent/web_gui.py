import streamlit as st
import json
import uuid
import os

TODO_FILE = 'todo.json'

st.title("📝 Task Entry for Autonomous Agent")

task = st.text_area("Enter a new task:", placeholder="e.g., Send an email to Sarah about Q2 report")
if st.button("Add Task"):
    if task.strip():
        new_task = {"id": str(uuid.uuid4()), "task": task}
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
        else:
            tasks = []
        tasks.append(new_task)
        with open(TODO_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
        st.success("Task added!")
    else:
        st.warning("Task cannot be empty!")

if st.button("View Current Tasks"):
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE) as f:
            tasks = json.load(f)
        for t in tasks:
            st.write(f"- {t['task']} (ID: {t['id']})")
