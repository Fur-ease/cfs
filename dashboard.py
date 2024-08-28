import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.ttk as ttk
import winsound
import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF

container_data = []
con = sqlite3.connect("containers.db")
cursor = con.cursor()

def populate_table(container_data, table):
    for i, container in enumerate(container_data):
        table.insert("", "end", values=container)

def search_container(container_number, app):
    # Create a new window for the search results
    search_window = ctk.CTkToplevel(app)
    search_window.title("Search Results")
    search_window.geometry("800x400")

    # Create a scrollable frame for the search results
    scrollable_frame = ScrollableFrame(search_window)
    scrollable_frame.pack(pady=20)

    # Create a table to display container data
   # container_table = ctk.CTkTable(scrollable_frame.scrollable_frame, columns=("Container Number", "Size", "Arrival Date", "Days Stayed", "Status"))
    #container_table.pack(pady=10)

    # Populate the table with container data
    #container_data = [
     #   ("CON123", "20ft", "2022-01-01", "30", "In Storage"),
      #  ("CON456", "40ft", "2022-02-15", "15", "In Transit"),
        # Add more container data here
    #]
    #populate_table(container_data, container_table)

#def search_container(container_number, app):
   # pass
    # Create a new window for the search results
   # search_window = ctk.CTkToplevel(app)
   # search_window.title("Search Results")
   # search_window.geometry("350x150")

    # Create a scrollable frame for the search results
   # scrollable_frame = ScrollableFrame(search_window)
   # scrollable_frame.pack(pady=20)

    # Display the container number in the scrollable frame
    #container_label = ctk.CTkLabel(scrollable_frame.scrollable_frame, text=f"Container Number: {container_number}")
    #container_label.pack()

def Yes(app):
    app.destroy()

    import main
    main.show_login_window(app)

def No(exit_window, dashboard):
    exit_window.destroy()
    dashboard.deiconify()



def exit(app):
    dashboard = app
    exit_window = ctk.CTkToplevel(app)
    exit_window.title("Exit")
    exit_window.geometry("350x150")
    # Add a message
    message = ctk.CTkLabel(exit_window, text="Are you sure you want to exit?")
    message.pack(pady=10)

    button_frame = ctk.CTkFrame(exit_window)
    button_frame.pack(pady=20, fill='x')
    Yes_button = ctk.CTkButton(button_frame, text="yes", command=lambda: Yes(app))
    Yes_button.grid(row=2, column=3, padx=(10, 20))
    No_button = ctk.CTkButton(button_frame, text="No", command=lambda: No(exit_window, dashboard))
    No_button.grid(row=2, column=4, padx=(10, 20))


    exit_window.attributes('-topmost', 1)
    # Suspend the app's functioning
    exit_window.grab_set()
    #play_sound()

def play_sound():
    winsound.PlaySound("alert.wav", winsound.SND_FILENAME)

def log_out(app):
    # open exit window
    exit(app)

def add_container(app, container_table):
    def create_and_insert_container(container_number_entry, size_entry, arrival_date_entry, owner_entry, agent_entry, pool_number_entry):

        # Get container data from user interface
        container_number = container_number_entry.get()
        size = size_entry.get()
        arrival_date = arrival_date_entry.get()
        owner = owner_entry.get()
        agent = agent_entry.get()
        pool_number = pool_number_entry.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('containers.db')
        c = conn.cursor()
        c.execute("""
               CREATE TABLE IF NOT EXISTS containers (
                   id INTEGER PRIMARY KEY,
                   container_number TEXT NOT NULL UNIQUE,
                   size TEXT NOT NULL,
                   arrival_date TEXT NOT NULL,
                   status TEXT NOT NULL,
                   location TEXT NOT NULL,
                   owner TEXT NOT NULL,
                   agent TEXT NOT NULL,
                   pool_number INTEGER NOT NULL
               )
               """)
        if not container_number:
            tkmb.showerror("Error", "Container number is required.")
            return
        # Check if the container number already exists
        if c.execute("SELECT 1 FROM containers WHERE container_number = ?", (container_number,)).fetchone():
            warning_window = ctk.CTkToplevel()
            warning_window.title("Warning")
            warning_window.geometry("300x100")
            tkmb.showwarning("Warning", "Container number already exists.")
            warning_window.attributes('-topmost', 1)
            warning_window.grab_set()
            conn.close()
            return

        # Insert the container data into the containers table
        c.execute(""""
           INSERT INTO containers (container_number, size, arrival_date, status, location, owner, agent, pool_number)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           """, (container_number, size, arrival_date, "0", "In Storage", owner, agent, pool_number))
        success_window = ctk.CTkToplevel()
        success_window.title("Success")
        success_window.geometry("300x100")
        tkmb.showinfo("Success", "Container added")
        success_window.attributes('-topmost', 1)
        success_window.grab_set()

        # Commit the changes
        conn.commit()
        # Clear the container data entry fields
        #container_number_entry.delete(0, 'end')
        #size_entry.delete(0, 'end')
        #arrival_date_entry.delete(0, 'end')
        #owner_entry.delete(0, 'end')

        # Fetch and populate container data
        cursor.execute("SELECT * FROM containers")
        container_data = cursor.fetchall()
        populate_table(container_data, container_table)

        # Commit the changes
        # conn.commit()

        # Close the connection
        # conn.close()


        # Update the container table in the dashboard
        container_table.delete(*container_table.get_children())
        for container in container_data:
            container_table.insert("", "end", values=container)

        #tkmb.showinfo("success", "Container added")

        # Update the container table in the dashboard
        container_data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) for row in conn.execute("SELECT * FROM containers")]
        container_table.delete(*container_table.get_children())
    for container in container_data:
        container_table.insert("", "end", values=container)
        # Display a message container added
        #tkmb.showinfo("Success", "Container added.")

        con.commit()

    # Create a new window for adding a container
        add_container_window = ctk.CTkToplevel(app)
        add_container_window.title("Add Container")
        add_container_window.geometry("900x300")
        add_container_window.grab_set()

    # Create a frame for the container addition form
        container_form_frame = ctk.CTkFrame(add_container_window)
        container_form_frame.pack(pady=20, fill='x')

    # Create labels and entries for container data
        ctk.CTkLabel(container_form_frame, text="Container Number:").grid(row=0, column=0, padx=(20, 0))
        container_number_entry = ctk.CTkEntry(container_form_frame, width=200)
        container_number_entry.grid(row=0, column=1, padx=(10, 20))

        ctk.CTkLabel(container_form_frame, text="Size:").grid(row=1, column=0, padx=(20, 0))
        size_entry = ctk.CTkEntry(container_form_frame, width=200)
        size_entry.grid(row=2, column=1, padx=(10, 20))

        ctk.CTkLabel(container_form_frame, text="Arrival Date:").grid(row=2, column=0, padx=(20, 0))
        arrival_date_entry = ctk.CTkEntry(container_form_frame, width=200)
        arrival_date_entry.grid(row=4, column=1, padx=(10, 20))

        ctk.CTkLabel(container_form_frame, text="Owner:").grid(row=3, column=0, padx=(20, 0))
        owner_entry = ctk.CTkEntry(container_form_frame, width=200)
        owner_entry.grid(row=6, column=1, padx=(10, 20))

        ctk.CTkLabel(container_form_frame, text="Clearing Agent:").grid(row=4, column=0, padx=(20, 0))
        agent_entry = ctk.CTkEntry(container_form_frame, width=200)
        agent_entry.grid(row=8, column=1, padx=(10, 20))

        ctk.CTkLabel(container_form_frame, text="Pool Number:").grid(row=5, column=0, padx=(20, 0))
        pool_number_entry = ctk.CTkEntry(container_form_frame, width=200)
        pool_number_entry.grid(row=10, column=1, padx=(10, 20))

    # Create a button to add the container
        add_button = ctk.CTkButton(container_form_frame, text="Add Container", command=create_and_insert_container(container_number_entry, size_entry, arrival_date_entry, owner_entry, agent_entry, pool_number_entry))
        add_button.grid(row=12, column=0, columnspan=2, pady=(20, 0))

        # Close the add container window
    #app.destroy()

    def back_to_dashboard():
        # Clear the contents of the container addition form
        container_number_entry.delete(0, 'end')
        size_entry.delete(0, 'end')
        arrival_date_entry.delete(0, 'end')
        owner_entry.delete(0, 'end')

        # Hide the container addition interface
        add_container_window.withdraw()

        # Show the dashboard
        #dashboard_obj = app.deiconify(app)

        # Fetch and populate container data
        cursor.execute("SELECT * FROM containers")
        container_data = cursor.fetchall()
        populate_table(container_data, container_table)

    # Create a new window for adding a container
    add_container_window = ctk.CTkToplevel(app)
    add_container_window.title("Add Container")
    add_container_window.geometry("500x300")

    # Clear the contents of the dashboard
    container_table.delete(*container_table.get_children())

    # Create a frame for the container addition form
    container_form_frame = ctk.CTkFrame(add_container_window)
    container_form_frame.pack(pady=20, fill='x')

    # Create labels and entries for container data
    ctk.CTkLabel(container_form_frame, text="Container Number:").grid(row=0, column=0, padx=(20, 0))
    container_number_entry = ctk.CTkEntry(container_form_frame, width=200)
    container_number_entry.grid(row=0, column=1, padx=(10, 20))

    ctk.CTkLabel(container_form_frame, text="Size:").grid(row=1, column=0, padx=(20, 0))
    size_entry = ctk.CTkEntry(container_form_frame, width=200)
    size_entry.grid(row=1, column=1, padx=(10, 20))

    ctk.CTkLabel(container_form_frame, text="Arrival Date:").grid(row=2, column=0, padx=(20, 0))
    arrival_date_entry = ctk.CTkEntry(container_form_frame, width=200)
    arrival_date_entry.grid(row=2, column=1, padx=(10, 20))

    ctk.CTkLabel(container_form_frame, text="Owner:").grid(row=3, column=0, padx=(20, 0))
    owner_entry = ctk.CTkEntry(container_form_frame, width=200)
    owner_entry.grid(row=3, column=1, padx=(10, 20))

    ctk.CTkLabel(container_form_frame, text="Clearing Agent:").grid(row=4, column=0, padx=(20, 0))
    agent_entry = ctk.CTkEntry(container_form_frame, width=200)
    agent_entry.grid(row=4, column=1, padx=(10, 20))

    ctk.CTkLabel(container_form_frame, text="Pool Number:").grid(row=5, column=0, padx=(20, 0))
    agent_entry = ctk.CTkEntry(container_form_frame, width=200)
    agent_entry.grid(row=5, column=1, padx=(10, 20))

    # Create a back button
    back_button = ctk.CTkButton(container_form_frame, text="Back", command=back_to_dashboard)
    back_button.grid(row=9, column=0, padx=(10, 20))

    # Create an ADD button
    add_button = ctk.CTkButton(container_form_frame, text="ADD", command=create_and_insert_container)
    add_button.grid(row=9, column=1, padx=(10, 20))
    add_container_window.attributes('-topmost', 1)
   # add_container_window.grab_set()

#def open_container_window(container_id, dashboard_window):
    # Hide the dashboard window
  #  dashboard_window.withdraw()

    # Create a new window to bill and clear the container
 #   container_window = ctk.CTkToplevel()
 #   container_window.title("Container Details")
 #   container_window.geometry("400x200")
 #   container_window.attributes('-topmost', 1)  # Make window topmost
 #   container_window.grab_set()  # Grab focus until closed

    # Add container details to the window
#    ctk.CTkLabel(container_window, text=f"Container ID: {container_id}").pack(pady=10)
#    bill_button = ctk.CTkButton(container_window, text="Bill Container")
#    bill_button.pack(pady=5)
 #   clear_button = ctk.CTkButton(container_window, text="Clear Container")
#    clear_button.pack(pady=5)

    # Add a back button to return to the dashboard
 #    back_button.pack(pady=10)

def back_to_dashboard(container_window, dashboard_window):
    # Close the container window
     container_window.destroy()

    # Show the dashboard window
     dashboard_window.deiconify()


def open_container_window(container_id, dashboard_window):
    # Hide the dashboard window
    dashboard_window.withdraw()

    try:
        # Fetch container details from the database
        cursor.execute("SELECT * FROM containers WHERE id = ?", (container_id,))
        container_details = cursor.fetchone()

        if container_details:
            # Extract container details
            container_number = container_details[1]
            size = container_details[2]
            arrival_date = container_details[3]
            clearance_date = container_details[4]
            status = container_details[5]
            location = container_details[6]
            owner = container_details[7]
            

            # Calculate days stayed and cost
            if clearance_date:
                clearance_datetime = datetime.strptime(clearance_date, '%Y-%m-%d')
            else:
                clearance_datetime = datetime.now()
            arrival_datetime = datetime.strptime(arrival_date, '%Y-%m-%d')
            days_stayed = (clearance_datetime - arrival_datetime).days
            cost = max(days_stayed - 10, 0) * 100

            # Create a new window to display container details
            container_window = ctk.CTkToplevel()
            container_window.title("Container Details")
            container_window.geometry("10500x1050")
            container_window.attributes('-topmost', 1)  # Make window topmost
            container_window.grab_set()  # Grab focus until closed

            # Add container details to the window
            ctk.CTkLabel(container_window, text=f"Container Number: {container_number}").pack(pady=5)
            ctk.CTkLabel(container_window, text=f"Size: {size}").pack()
            ctk.CTkLabel(container_window, text=f"Arrival Date: {arrival_date}").pack()
            ctk.CTkLabel(container_window, text=f"Clearance Date: {clearance_date}").pack()
            ctk.CTkLabel(container_window, text=f"Status: {status}").pack()  # Add status label
            ctk.CTkLabel(container_window, text=f"Location: {location}").pack()
            ctk.CTkLabel(container_window, text=f"Days Stayed: {days_stayed}").pack()
            ctk.CTkLabel(container_window, text=f"Cost: ${cost}").pack()

            # Entry field for adding clearance date
            ctk.CTkLabel(container_window, text="Clearance Date:").pack()
            clearance_date_entry = ctk.CTkEntry(container_window)
            clearance_date_entry.pack()

        else:
            raise ValueError("Failed to fetch container details from the database.")
    except Exception as e:
        tkmb.showerror("Error", str(e))


        # Entry field for adding clearance date
        ctk.CTkLabel(container_window, text="Clearance Date:").pack()
        clearance_date_entry = ctk.CTkEntry(container_window)
        clearance_date_entry.pack()

        # Function to bill the container
        def bill_container():
            # Update the clearance date in the database
            clearance_date = clearance_date_entry.get()
            cursor.execute("UPDATE containers SET clearance_date = ? WHERE id = ?", (clearance_date, container_id))
            con.commit()

            # Generate invoice
            invoice_text = f"Container Number: {container_number}\n" \
                           f"Owner: {owner}\n" \
                           f"Size: {size}\n" \
                           f"Arrival Date: {arrival_date}\n" \
                           f"Clearance Date: {clearance_date}\n" \
                           f"Days Stayed: {days_stayed}\n" \
                           f"Cost: ${cost}\n"

            with open(f"{container_number}_invoice.txt", "w") as invoice_file:
                invoice_file.write(invoice_text)

            tkmb.showinfo("Success", "Container billed successfully. Invoice generated.")

            # Close the container window
            container_window.destroy()

            # Show the dashboard window
            dashboard_window.deiconify()

        # Add a button to bill the container
        bill_button = ctk.CTkButton(container_window, text="Bill Container", command=bill_container)
        bill_button.pack(pady=5)

        # Add a back button to return to the dashboard
        back_button = ctk.CTkButton(container_window, text="Back", command=lambda: back_to_dashboard(container_window, dashboard_window))
        back_button.pack(pady=10)

    except Exception as e:
        tkmb.showerror("Error", str(e))

        # Show the dashboard window
        dashboard_window.deiconify()






def clear_and_bill(app):
    # Implement clear and bill services logic here
    pass

def perform_service(app):
    # Implement perform services logic here
    pass

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = ctk.CTkCanvas(self)
        scrollbar = ctk.CTkScrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



def Dashboard(app):
    def __init__(self, master, app):
        self.master = master
        self.app = app


    # Create a frame for the search bar and buttons
    search_frame = ctk.CTkFrame(app)
    search_frame.pack(pady=20, fill='x')

    # Create a search bar for the container number
    ctk.CTkLabel(search_frame, text="Container Number:").grid(row=0, column=0, padx=(20, 0))
    container_number_entry = ctk.CTkEntry(search_frame, width=200)
    container_number_entry.grid(row=0, column=1, padx=(10, 20))

    # Create a search button
    search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: search_container(container_number_entry.get(), app))
    search_button.grid(row=0, column=2, padx=(10, 20))

    # Create a frame for the table
    table_frame = ctk.CTkFrame(app)
    table_frame.pack(pady=20, fill='x')

    # Create a table to display container data
    container_table = ttk.Treeview(table_frame, columns=("Id", "Container Number", "Size", "Arrival Date", "Days Stayed", "Status"))
    container_table.pack(pady=10)

    # Define the column headings
    container_table.heading("Id", text="id")
    container_table.heading("Container Number", text="Container Number")
    container_table.heading("Size", text="Size")
    container_table.heading("Arrival Date", text="Arrival Date")
    container_table.heading("Days Stayed", text="Days Stayed")
    container_table.heading("Status", text="Status")

    # Define the column widths
    container_table.column("Id", width=300)
    container_table.column("Container Number", width=300)
    container_table.column("Size", width=100)
    container_table.column("Arrival Date", width=150)
    container_table.column("Days Stayed", width=150)
    container_table.column("Status", width=150)

    # Bind double-click event to open_container_window function
    container_table.bind("<Double-1>", lambda event: open_container_window(
        container_table.item(container_table.selection())['values'][0], app))

    # Fetch and populate container data
    cursor.execute("SELECT * FROM containers")
    container_data = cursor.fetchall()
    populate_table(container_data, container_table)

        # Create a frame for the buttons
    button_frame = ctk.CTkFrame(app)
    button_frame.pack(pady=20, fill='x')

    # Create a button for adding a new container
    add_container_button = ctk.CTkButton(button_frame, text="Add New Container", command=lambda: add_container(app,container_table))
    add_container_button.grid(row=0, column=0, padx=(10, 20))

    # Create a button for clearing and billing container services
    clear_and_bill_button = ctk.CTkButton(button_frame, text="Clear and Bill Containers", command=lambda: clear_and_bill(app))
    clear_and_bill_button.grid(row=0, column=1, padx=(10, 20))

    # Create a button for performing container services
    perform_service_button = ctk.CTkButton(button_frame, text="Container Services", command=lambda: perform_service(app))
    perform_service_button.grid(row=0, column=2, padx=(10, 20))

    button_frame = ctk.CTkFrame(app)
    button_frame.pack(pady=20, fill='x')

    # Create a log out button
    log_out_button = ctk.CTkButton(button_frame, text="Log Out", command=lambda: log_out(app))
    log_out_button.grid(row=0, column=3, padx=(10, 20))
