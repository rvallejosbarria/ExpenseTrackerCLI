import datetime
import argparse
import json

from expense import Expense
from typing import Optional

def load_expenses(filename: str):
  try:
    with open(filename, "r") as file:
      data = json.load(file)
      if isinstance(data, list):
        return [Expense.from_dict(item) for item in data]  # Convert dictionaries to Expense objects
      else:
        raise TypeError("Expected a list of dictionaries in the JSON file")
  except FileNotFoundError:
    print(f"{filename} not found. Starting with an empty list.")
    return []
  except IOError:
    print(f"An I/O error occurred while trying to read the file {filename}.")
    return []
  except json.JSONDecodeError:
    print(f"{filename} is empty or contains invalid JSON. Starting with an empty list.")
    return []

def get_next_id(expenses: list) -> int:
  if expenses:
    return max(expense.id for expense in expenses) + 1  # Increment the highest existing ID by 1
  else:
    return 1  # If no expense exist, start with ID 1

def save_expenses(filename: str, expenses: list) -> None:
  try:
    with open(filename, "w") as file:
      json.dump([expense.to_dict() for expense in expenses], file, indent=4)  # Convert Expense objects to dictionaries and save as JSON
  except IOError:
    print(f"An I/O error occurred while trying to write to the file {filename}.")
  except TypeError as e:
    print("Failed to serialize object to JSON: {e}")

def find_expense_by_id(expenses: list, expense_id: int) -> Optional[Expense]:
  for expense in expenses:
    if expense.id == expense_id:
      return expense
  return None

def main():
  filename = 'expenses.json'

  expenses = load_expenses(filename)

  parser = argparse.ArgumentParser(description="CLI app to manage your finances")

  # Define subcommands for various operations
  subparsers = parser.add_subparsers(dest='command', help='Subcommand to run')

  # Subcommand for adding a new expense
  add_parser = subparsers.add_parser('add', help='Add a new expense')
  add_parser.add_argument('description', type=str, help='Description of the expense')

  add_parser.add_argument('amount', type=int, help='Amount of the expense')
  add_parser.add_argument('--expense-date', type=str, default=datetime.datetime.now().date().isoformat(), help='Time of creation of the expense')

  args = parser.parse_args()  # Parse the command-line arguments

  if args.command == 'add':
    new_id = get_next_id(expenses) # Generate a new expense ID

    # Create a new expense and append it to the list
    expense = Expense(new_id, args.expense_date, args.description, args.amount, datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat())
    expenses.append(expense)

    save_expenses(filename, expenses) # Save expenses to the file

    print(f"Expense added successfully (ID: {expense.id})")
  else:
    parser.print_help() # Print help message if no valid subcommand is provided

if __name__ == "__main__":
  main()