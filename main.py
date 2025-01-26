import bcrypt
import json
import os
import csv
from datetime import datetime

# File paths
USERS_FILE = 'users.txt'
TASKS_FILE = 'tasks.json'
EXPENSES_FILE = 'expenses.csv'

# Utility Functions
def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def load_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

def save_csv(data, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

# User Authentication
def register_user():
    username = input("Enter a new username: ")
    if user_exists(username):
        print("Username already exists. Try again.")
        return None

    password = input("Enter a new password: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}:{hashed_password.decode('utf-8')}\n")
    
    print("User registered successfully!")
    return username

def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    with open(USERS_FILE, 'r') as f:
        users = f.readlines()

    for user in users:
        stored_username, stored_password = user.strip().split(':')
        if username == stored_username and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Login successful!")
            return username

    print("Invalid credentials. Try again.")
    return None

def user_exists(username):
    with open(USERS_FILE, 'r') as f:
        users = f.readlines()
    for user in users:
        if user.strip().split(':')[0] == username:
            return True
    return False

# Task Management
def add_task(username):
    tasks = load_json(TASKS_FILE)
    if username not in tasks:
        tasks[username] = []
    
    description = input("Enter task description: ")
    task_id = len(tasks[username]) + 1
    task = {"task_id": task_id, "description": description, "status": "Pending"}
    tasks[username].append(task)
    save_json(tasks, TASKS_FILE)
    print("Task added successfully!")

def view_tasks(username):
    tasks = load_json(TASKS_FILE)
    if username not in tasks or len(tasks[username]) == 0:
        print("No tasks found.")
        return

    for task in tasks[username]:
        print(f"Task ID: {task['task_id']}, Description: {task['description']}, Status: {task['status']}")

def mark_task_completed(username):
    task_id = int(input("Enter task ID to mark as completed: "))
    tasks = load_json(TASKS_FILE)
    if username not in tasks:
        print("No tasks found.")
        return
    
    for task in tasks[username]:
        if task['task_id'] == task_id:
            task['status'] = 'Completed'
            save_json(tasks, TASKS_FILE)
            print("Task marked as completed.")
            return
    
    print("Task ID not found.")

def delete_task(username):
    task_id = int(input("Enter task ID to delete: "))
    tasks = load_json(TASKS_FILE)
    if username not in tasks:
        print("No tasks found.")
        return

    for task in tasks[username]:
        if task['task_id'] == task_id:
            tasks[username].remove(task)
            save_json(tasks, TASKS_FILE)
            print("Task deleted.")
            return
    
    print("Task ID not found.")

# Budget Tracking
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter expense category: ")
    amount = float(input("Enter expense amount: "))
    description = input("Enter expense description: ")

    expense = [date, category, amount, description]
    expenses = load_csv(EXPENSES_FILE)
    expenses.append(expense)
    save_csv(expenses, EXPENSES_FILE)
    print("Expense added successfully!")

def view_expenses():
    expenses = load_csv(EXPENSES_FILE)
    if len(expenses) == 0:
        print("No expenses recorded.")
        return

    print("Expenses:")
    for expense in expenses:
        print(f"Date: {expense[0]}, Category: {expense[1]}, Amount: ${expense[2]}, Description: {expense[3]}")

def track_budget(budget):
    expenses = load_csv(EXPENSES_FILE)
    total_expenses = sum(float(expense[2]) for expense in expenses)
    remaining_balance = budget - total_expenses

    if remaining_balance < 0:
        print(f"Warning: You have exceeded your budget! You are over by ${abs(remaining_balance)}.")
    else:
        print(f"You have ${remaining_balance} left for the month.")

# Menus
def task_manager_menu(username):
    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_task(username)
        elif choice == '2':
            view_tasks(username)
        elif choice == '3':
            mark_task_completed(username)
        elif choice == '4':
            delete_task(username)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def budget_tracker_menu():
    while True:
        print("\nBudget Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Track Budget")
        print("4. Save Expenses")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            budget = float(input("Enter your monthly budget: $"))
            track_budget(budget)
        elif choice == '4':
            print("Expenses saved successfully.")
            break
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

# Main Program
def main():
    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = login_user()
            if username:
                while True:
                    print("\nChoose an option:")
                    print("1. Task Manager")
                    print("2. Budget Tracker")
                    print("3. Logout")
                    option = input("Enter your choice: ")

                    if option == '1':
                        task_manager_menu(username)
                    elif option == '2':
                        budget_tracker_menu()
                    elif option == '3':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Try again.")
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
