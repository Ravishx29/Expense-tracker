import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import matplotlib.pyplot as plt

DATA_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return
    note = note_entry.get()

    if not date or not category or amount <= 0:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }

    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    update_expense_list()
    clear_entries()
    messagebox.showinfo("Success", "Expense added successfully.")

def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

def update_expense_list():
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    expenses = load_expenses()
    for i, e in enumerate(expenses, start=1):
        expense_tree.insert("", "end", values=(e["date"], e["category"], f"₹{e['amount']}", e["note"]))

def show_summary_chart():
    expenses = load_expenses()
    if not expenses:
        messagebox.showinfo("No Data", "No expenses to display.")
        return
    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.axis("equal")
    plt.show()

app = tk.Tk()
app.title("Expense Tracker")
app.geometry("700x500")
app.config(padx=10, pady=10)

tk.Label(app, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(app)
date_entry.grid(row=0, column=1)

tk.Label(app, text="Category").grid(row=1, column=0)
category_entry = tk.Entry(app)
category_entry.grid(row=1, column=1)

tk.Label(app, text="Amount").grid(row=2, column=0)
amount_entry = tk.Entry(app)
amount_entry.grid(row=2, column=1)

tk.Label(app, text="Note").grid(row=3, column=0)
note_entry = tk.Entry(app)
note_entry.grid(row=3, column=1)

tk.Button(app, text="Add Expense", command=add_expense).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(app, text="Show Summary Chart", command=show_summary_chart).grid(row=5, column=0, columnspan=2)

columns = ("Date", "Category", "Amount", "Note")
expense_tree = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, width=100)
expense_tree.grid(row=6, column=0, columnspan=2, pady=10)

update_expense_list()
app.mainloop()