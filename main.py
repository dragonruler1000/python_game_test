import random
import os
import json

# =========================
# DATA
# =========================

# Load tickets from JSON file
with open("tickets.json", "r") as f:
    tickets = json.load(f)

# Load manager messages from JSON file
with open("manager_messages.json", "r") as f:
    manager_messages = json.load(f)

# =========================
# GAME STATE
# =========================

score = 0
chaos = 0
luck = 0
rounds = 10

# =========================
# FUNCTIONS
# =========================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("=" * 50)
    print("      DUNGEON HUMAN RESOURCES SIMULATOR")
    print("=" * 50)
    print(f"Score: {score} | Chaos Level: {chaos} | Luck: {luck}")
    print()


def show_manager_message():
    print("\n--- MANAGER EMAIL ---")
    print(random.choice(manager_messages))
    print("---------------------\n")


def run_ticket(ticket):
    global score
    global chaos
    global luck

    print(f"CUSTOMER: {ticket['name']}")
    print(f"ISSUE: {ticket['problem']}")
    print()

    for i, solution in enumerate(ticket["solutions"], start=1):
        print(f"{i}. {solution}")

    print()

    while True:
        choice = input("Choose a solution: ")

        if choice.isdigit():
            choice = int(choice) - 1

            if 0 <= choice < len(ticket["solutions"]):
                break

        print("Invalid choice. Try again.")

    print()

    if choice == ticket["correct"]:
        print(ticket["success"])
        score += 10
        luck += random.randint(1, 10)
    else:
        print(ticket["failure"])
        chaos += 5
        luck -= random.randint(1, 5)

    # Random chaos escalation
    if random.randint(1, 4) == 1:
        chaos += 1
        print("\nReality appears slightly unstable.")

    input("\nPress Enter to continue...")


def ending():
    clear_screen()

    print("=" * 50)
    print("FINAL REPORT")
    print("=" * 50)
    print(f"Final Score: {score}")
    print(f"Final Chaos: {chaos}")
    print(f"Final Luck: {luck}")
    print()

    if chaos < 10:
        print("You successfully maintained the dungeon.")
        print("The kingdom remains mostly functional.")
    elif chaos < 20:
        print("Several laws of physics have resigned.")
        print("Management considers this acceptable.")
    else:
        print("The moon has filed a support ticket.")
        print("Reality is now customer service.")

# =========================
# MAIN GAME LOOP
# =========================

used_tickets = []

for round_number in range(rounds):

    clear_screen()
    print_header()

    # Show random manager messages sometimes
    if random.randint(1, 2) == 1:
        show_manager_message()

    # Prevent immediate repeats
    available_tickets = [
        ticket for ticket in tickets
        if ticket not in used_tickets
    ]

    # Reset if all tickets used
    if not available_tickets:
        used_tickets.clear()
        available_tickets = tickets.copy()

    ticket = random.choice(available_tickets)
    used_tickets.append(ticket)

    run_ticket(ticket)

ending()