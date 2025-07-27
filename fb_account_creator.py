import os
import time
import random
from termcolor import colored
from datetime import datetime

# Helper functions for colored output
def info(text): print(colored(text, 'blue'))
def success(text): print(colored(text, 'green'))
def error(text): print(colored(text, 'red'))
def warn(text): print(colored(text, 'yellow'))

# ফাইল পাথ
NUMBERS_FILE = "numbers.txt"
ACCOUNTS_FILE = "accounts.txt"
HISTORY_FILE = "history.txt"

# নাম্বার লোড করা
def load_numbers():
    nums = []
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, "r") as f:
            nums = [line.strip() for line in f if line.strip()]
    return nums

# নাম্বার সংরক্ষণ
def save_numbers(numbers):
    with open(NUMBERS_FILE, "w") as f:
        for num in numbers:
            f.write(num + "\n")

# Add Number ফিচার
def add_numbers():
    info("\n📥 Enter phone numbers one by one (type 0 to finish):")
    new_numbers = []
    existing_numbers = set(load_numbers())

    while True:
        number = input("> ").strip()
        if number == "0":
            break
        if not (number.startswith("+880") or number.startswith("01")) or len(number) < 11:
            warn("⚠️ Invalid number format! Try again.")
            continue
        if number in existing_numbers or number in new_numbers:
            warn("⚠️ Number already added, skip.")
        else:
            new_numbers.append(number)

    if new_numbers:
        with open(NUMBERS_FILE, "a") as f:
            for num in new_numbers:
                f.write(num + "\n")
        success(f"✅ {len(new_numbers)} new number(s) added successfully!\n")
    else:
        info("ℹ️ No new numbers added.\n")

# Delete Number ফিচার
def delete_numbers():
    numbers = load_numbers()
    if not numbers:
        warn("⚠️ No numbers to delete.\n")
        return

    while True:
        info("\n🗑️ Numbers List:")
        for idx, num in enumerate(numbers, 1):
            print(f"{idx}. {num}")
        print("0. Back to Main Menu")

        choice = input("Enter line number to delete or 0 to go back: ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(numbers):
            warn("⚠️ Invalid choice! Try again.")
            continue
        idx = int(choice) - 1
        removed = numbers.pop(idx)
        save_numbers(numbers)
        success(f"Deleted number: {removed}")

# View Accounts ফিচার
def view_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        info("ℹ️ No accounts created yet.\n")
        return
    info("\n📄 Saved Accounts:")
    with open(ACCOUNTS_FILE, "r") as f:
        lines = f.readlines()
        if not lines:
            info("ℹ️ No accounts found.\n")
            return
        for idx, line in enumerate(lines, 1):
            print(f"{idx}. {line.strip()}")
    print()

# History Log ফিচার
def view_history():
    if not os.path.exists(HISTORY_FILE):
        info("ℹ️ No history found.\n")
        return
    info("\n📅 Account Creation History:")
    with open(HISTORY_FILE, "r") as f:
        logs = f.readlines()
        if not logs:
            info("ℹ️ History is empty.\n")
            return
        for line in logs:
            print(line.strip())
    print()

# Random name generator (faker নয়, সিম্পল)
def generate_random_name():
    first_names = ["Rahim", "Karim", "Alam", "Sujon", "Mamun", "Arif", "Jahid", "Rana", "Babul", "Nabil"]
    last_names = ["Hossain", "Khan", "Ahmed", "Islam", "Chowdhury", "Sarkar", "Rahman", "Ali", "Mia", "Faruk"]
    return random.choice(first_names) + " " + random.choice(last_names)

# Random password generator (সিম্পল)
def generate_password(length=8):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
    return "".join(random.choice(chars) for _ in range(length))

# সিমুলেটেড Facebook একাউন্ট তৈরি প্রক্রিয়া (OTP verification সহ)
def create_account_flow(numbers_to_use):
    success_accounts = []
    failed_accounts = []

    info(f"\n🔢 Starting account creation for {len(numbers_to_use)} number(s)...\n")

    for number in numbers_to_use:
        info(f"Sending OTP to {number}...")
        time.sleep(1)  # simulate sending OTP

        otp = input(f"Enter OTP for {number}: ").strip()
        # সিমুলেশন: 6 digit otp, যদি 6 digit না হয় fail
        if len(otp) == 6 and otp.isdigit():
            name = generate_random_name()
            password = generate_password()
            success(f"[+] Success: {number} | Name: {name} | Pass: {password}")
            success_accounts.append((number, name, password))
            # accounts.txt এ সেভ
            with open(ACCOUNTS_FILE, "a") as f:
                date_str = datetime.now().strftime("%Y-%m-%d")
                f.write(f"{number} | {name} | {password} | {date_str}\n")
        else:
            error(f"[!] Failed: {number} | Reason: Invalid OTP")
            failed_accounts.append(number)

        time.sleep(random.randint(2, 4))  # delay to avoid blocking

    # history.txt তে যোগ করো
    if success_accounts:
        date_str = datetime.now().strftime("%Y-%m-%d")
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{date_str} → {len(success_accounts)} accounts created\n")

    # summary
    success(f"\n✅ Account creation completed!")
    info(f"Total: {len(numbers_to_use)} | Success: {len(success_accounts)} | Failed: {len(failed_accounts)}\n")

# Create Account ফিচারের মেনু
def create_account():
    numbers = load_numbers()
    if not numbers:
        warn("⚠️ No numbers available. Please add numbers first.\n")
        return

    info("\n🔢 How many accounts do you want to create? (5, 10, 20)")
    while True:
        choice = input("Enter choice: ").strip()
        if choice in ["5", "10", "20"]:
            count = int(choice)
            break
        else:
            warn("⚠️ Invalid input! Please enter 5, 10, or 20.")

    if count > len(numbers):
        warn(f"⚠️ Only {len(numbers)} numbers available, proceeding with available numbers.")

    to_use = numbers[:count]
    create_account_flow(to_use)

# Main Menu
def main_menu():
    while True:
        print(colored("""
==============================
   Auto Facebook Creator
==============================
[1] Add Numbers
[2] Delete Numbers
[3] Create Account
[4] View Accounts
[5] History Log
[0] Exit
""", "cyan"))
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_numbers()
        elif choice == "2":
            delete_numbers()
        elif choice == "3":
            create_account()
        elif choice == "4":
            view_accounts()
        elif choice == "5":
            view_history()
        elif choice == "0":
            info("Exiting... Goodbye!")
            break
        else:
            warn("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()