import sqlite3
import customtkinter as ctk
import tkinter.messagebox as tkmb


def Homepage(app):
    import tkinter as tk
    import tkinter.ttk as ttk

    # Data for the table (replace with your actual data)
    orders_data = [
        ["Order 1", "Customer A", "Pending"],
        ["Order 2", "Customer B", "Pending"],
    ]

    # Create the main application window
    root = tk.Tk()
    root.title("Dashboard")

    # Create a frame to hold the dashboard widgets
    dashboard_frame = ttk.Frame(root, width=800, height=400)
    dashboard_frame.grid(row=0, column=0, padx=10, pady=10)

    # Create the table
    orders_table = ttk.Treeview(dashboard_frame, columns=("Order ID", "Customer", "Status"), show="headings")
    orders_table.heading("Order ID", text="Order ID")
    orders_table.heading("Customer", text="Customer")
    orders_table.heading("Status", text="Status")
    for row in orders_data:
        orders_table.insert("", "end", values=row)
    orders_table.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    # Create other widgets
    title_text = ttk.Label(dashboard_frame, text="Oxides Pending")
    title_text.grid(row=0, column=1, padx=10, pady=10)
    number_label1 = ttk.Label(dashboard_frame, text="2")
    number_label1.grid(row=1, column=1, padx=10, pady=10)
    number_label2 = ttk.Label(dashboard_frame, text="3")
    number_label2.grid(row=2, column=1, padx=10, pady=10)
    text_label1 = ttk.Label(dashboard_frame, text="CVER ORDERS")
    text_label1.grid(row=1, column=2, padx=10, pady=10)
    text_label2 = ttk.Label(dashboard_frame, text="LAST SCHEDULES")
    text_label2.grid(row=2, column=2, padx=10, pady=10)

    # Run the application
    #root.mainloop()
