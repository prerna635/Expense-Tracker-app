import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()

# Add expense to DB
def add_expense():
    amount = entry_amount.get()
    category = combo_category.get()
    date = entry_date.get()

    if not amount or not category or not date:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                   (amount, category, date))
    conn.commit()
    messagebox.showinfo("Success", "Expense added successfully!")
    entry_amount.delete(0, tk.END)
    combo_category.set("")
    entry_date.delete(0, tk.END)
    load_expenses()

# Load all expenses into table
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM expenses")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# Show pie chart by category
def show_pie_chart():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("Info", "No data to display")
        return
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.show()

# Show line chart over time
def show_line_chart():
    cursor.execute("SELECT date, SUM(amount) FROM expenses GROUP BY date ORDER BY date")
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("Info", "No data to display")
        return
    dates = [row[0] for row in data]
    amounts = [row[1] for row in data]
    plt.figure(figsize=(8,4))
    plt.plot(dates, amounts, marker="o", color="blue")
    plt.xticks(rotation=45)
    plt.title("Expenses Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Amount")
    plt.tight_layout()
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Expense Tracker - Day 22/30")
root.geometry("1000x700")  # Increased size
# root.state('zoomed')  # Uncomment to start maximized

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_input)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Category:").grid(row=0, column=2, padx=5, pady=5)
combo_category = ttk.Combobox(frame_input, values=["Food", "Travel", "Shopping", "Bills", "Other"])
combo_category.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_input, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=5, padx=5, pady=5)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

btn_add = tk.Button(frame_input, text="Add Expense", command=add_expense)
btn_add.grid(row=0, column=6, padx=5, pady=5)

# Expense table
columns = ("ID", "Amount", "Category", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

# Column headings & widths
tree.heading("ID", text="ID")
tree.column("ID", width=80, anchor=tk.CENTER)
tree.heading("Amount", text="Amount")
tree.column("Amount", width=200, anchor=tk.CENTER)
tree.heading("Category", text="Category")
tree.column("Category", width=300, anchor=tk.CENTER)
tree.heading("Date", text="Date")
tree.column("Date", width=200, anchor=tk.CENTER)

tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Buttons for visualization
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_pie = tk.Button(frame_buttons, text="Show Pie Chart", command=show_pie_chart)
btn_pie.grid(row=0, column=0, padx=10)

btn_line = tk.Button(frame_buttons, text="Show Line Chart", command=show_line_chart)
btn_line.grid(row=0, column=1, padx=10)

load_expenses()
root.mainloop()
