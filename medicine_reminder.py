import time
import subprocess
from datetime import datetime
import os

FILE_NAME = "medicines.txt"


def speak(text):
    try:
        subprocess.Popen([
            'powershell', '-Command',
            f'Add-Type -AssemblyName System.Speech; '
            f'$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            f'$s.Speak("{text}")'
        ])
    except Exception as e:
        print(f"Voice error: {e}")


def load_medicines():
    medicines = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) < 3:
                    continue
                medicines.append({
                    "name": parts[0],
                    "time": parts[1],
                    "days": [d.strip() for d in parts[2:]]
                })
    return medicines


def save_all(medicines):
    with open(FILE_NAME, "w") as file:
        for med in medicines:
            file.write(f"{med['name']},{med['time']},{','.join(med['days'])}\n")


def add_medicine():
    medicines = load_medicines()
    name = input("Enter medicine name: ").strip()
    med_time = input("Enter time (HH:MM): ").strip()
    days_input = input("Enter days (Mon,Tue,Wed): ").strip()
    days = [d.strip() for d in days_input.split(",") if d.strip()]

    medicines.append({
        "name": name,
        "time": med_time,
        "days": days
    })
    save_all(medicines)
    print(f" '{name}' added!")


def show_medicines():
    meds = load_medicines()
    if not meds:
        print("No medicines!")
        return
    print("\n--- Medicines ---")
    for i, m in enumerate(meds, 1):
        print(f"{i}. {m['name']} at {m['time']} on {', '.join(m['days'])}")


def delete_medicine():
    meds = load_medicines()
    if not meds:
        print("No medicines!")
        return
    show_medicines()
    try:
        choice = int(input("\nEnter number to delete: "))
        if 1 <= choice <= len(meds):
            removed = meds.pop(choice - 1)
            save_all(meds)
            print(f" '{removed['name']}' deleted!")
        else:
            print(" Invalid!")
    except ValueError:
        print(" Invalid!")


def check_reminders():
    print(" Reminder chal raha hai... (band karne ke liye Ctrl+C)")
    reminded = set()

    while True:
        meds = load_medicines()
        now_time = datetime.now().strftime("%H:%M")
        today = datetime.now().strftime("%a")

        # Debug - har check pe time print hoga
        print(f" Checking... {now_time} | {today}", end="\r")

        for m in meds:
            key = (m["name"], now_time)
            if m["time"] == now_time and today in m["days"] and key not in reminded:
                for i in range(4):
                    msg = f"Time to take your medicine {m['name']}"
                    print(f"\n REMINDER:({i+1}/4): {msg}")
                    speak(msg)
                    time.sleep(5)
                print("Reminder completed")
                reminded.add(key)

        if now_time not in [m["time"] for m in meds]:
            reminded.clear()

        time.sleep(15)


# MENU
print("=" * 45)
print(" Medicine Reminder System")
print("=" * 45)

while True:
    print("\n1. Add Medicine")
    print("2. Show Medicines")
    print("3. Delete Medicine")
    print("4. Start Reminder (menu band ho jaayega)")
    print("5. Exit")

    try:
        choice = input("Enter choice: ").strip()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break

    if choice == "1":
        add_medicine()
    elif choice == "2":
        show_medicines()
    elif choice == "3":
        delete_medicine()
    elif choice == "4":
        check_reminders()
    elif choice == "5":
        print("Goodbye! Allah Hafiz ")
        break
    else:
        print(" Invalid choice!")
