import json
import os

GOALS_FILE = "data/goals.json"


def load_goals():
    if not os.path.exists(GOALS_FILE):
        return []

    with open(GOALS_FILE, "r") as f:
        return json.load(f)


def save_goals(goals):
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=4)


def add_goal(goal):
    goals = load_goals()
    goals.append(goal)
    save_goals(goals)