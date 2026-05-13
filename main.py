import random
import os
import sys
import json
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# =========================
# LOAD DATA
# =========================

with open(resource_path("tickets.json"), "r") as f:
    tickets = json.load(f)

with open(resource_path("manager_messages.json"), "r") as f:
    manager_messages = json.load(f)

# =========================
# GAME STATE
# =========================

score = 0
chaos = 0
luck = 0
rounds = 10
current_round = 0
used_tickets = []
current_ticket = None

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Dungeon Human Resources Simulator")
root.geometry("1000x800")
root.configure(bg="#1e1e1e")

# =========================
# UI ELEMENTS
# =========================

header_label = tk.Label(
    root,
    text="DUNGEON HUMAN RESOURCES SIMULATOR",
    font=("Consolas", 20, "bold"),
    fg="white",
    bg="#1e1e1e"
)
header_label.pack(pady=10)

stats_label = tk.Label(
    root,
    text="",
    font=("Consolas", 12),
    fg="#00ff99",
    bg="#1e1e1e"
)
stats_label.pack()

manager_label = tk.Label(
    root,
    text="",
    font=("Consolas", 11, "italic"),
    fg="#ffcc66",
    bg="#1e1e1e",
    wraplength=700,
    justify="left"
)
manager_label.pack(pady=10)

customer_label = tk.Label(
    root,
    text="",
    font=("Consolas", 14, "bold"),
    fg="white",
    bg="#1e1e1e",
    wraplength=700,
    justify="left"
)
customer_label.pack(pady=5)

issue_label = tk.Label(
    root,
    text="",
    font=("Consolas", 12),
    fg="white",
    bg="#1e1e1e",
    wraplength=700,
    justify="left"
)
issue_label.pack(pady=10)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=20)

result_label = tk.Label(
    root,
    text="",
    font=("Consolas", 11),
    fg="#cccccc",
    bg="#1e1e1e",
    wraplength=700,
    justify="left"
)
result_label.pack(pady=10)

next_button = tk.Button(
    root,
    text="Next Ticket",
    font=("Consolas", 12),
    command=lambda: next_ticket()
)

# =========================
# FUNCTIONS
# =========================

def update_stats():
    stats_label.config(
        text=f"Score: {score} | Chaos Level: {chaos} | Luck: {luck} | Round: {current_round}/{rounds}"
    )

def clear_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()

def show_ticket():
    global current_ticket
    global current_round

    if current_round >= rounds:
        show_ending()
        return

    current_round += 1

    update_stats()
    result_label.config(text="")
    next_button.pack_forget()

    # Manager message chance
    if random.randint(1, 2) == 1:
        manager_label.config(
            text="--- MANAGER EMAIL ---\n" + random.choice(manager_messages)
        )
    else:
        manager_label.config(text="")

    # Prevent repeats
    available_tickets = [
        ticket for ticket in tickets
        if ticket not in used_tickets
    ]

    if not available_tickets:
        used_tickets.clear()
        available_tickets = tickets.copy()

    current_ticket = random.choice(available_tickets)
    used_tickets.append(current_ticket)

    customer_label.config(
        text=f"CUSTOMER: {current_ticket['name']}"
    )

    issue_label.config(
        text=f"ISSUE:\n{current_ticket['problem']}"
    )

    clear_buttons()

    for index, solution in enumerate(current_ticket["solutions"]):
        button = tk.Button(
            button_frame,
            text=solution,
            font=("Consolas", 11),
            width=60,
            wraplength=500,
            justify="left",
            command=lambda idx=index: choose_solution(idx)
        )

        button.pack(pady=5)

def choose_solution(choice):
    global score
    global chaos
    global luck

    clear_buttons()

    if choice == current_ticket["correct"]:
        result_text = current_ticket["success"]
        score += 10
        luck += random.randint(1, 10)
    else:
        result_text = current_ticket["failure"]
        chaos += 5
        luck -= random.randint(1, 5)

    # Random chaos escalation
    if random.randint(1, 4) == 1:
        chaos += 1
        result_text += "\n\nReality appears slightly unstable."

    result_label.config(text=result_text)

    update_stats()

    next_button.pack(pady=20)

def next_ticket():
    show_ticket()

def show_ending():
    clear_buttons()

    manager_label.config(text="")
    customer_label.config(text="FINAL REPORT")

    final_text = (
        f"Final Score: {score}\n"
        f"Final Chaos: {chaos}\n"
        f"Final Luck: {luck}\n\n"
    )

    if chaos < 10:
        final_text += (
            "You successfully maintained the dungeon.\n"
            "The kingdom remains mostly functional."
        )
    elif chaos < 20:
        final_text += (
            "Several laws of physics have resigned.\n"
            "Management considers this acceptable."
        )
    else:
        final_text += (
            "The moon has filed a support ticket.\n"
            "Reality is now customer service."
        )

    issue_label.config(text=final_text)

    result_label.config(text="")

    next_button.config(
        text="Exit",
        command=root.destroy
    )

    next_button.pack(pady=20)

# =========================
# START GAME
# =========================

show_ticket()

root.mainloop()

