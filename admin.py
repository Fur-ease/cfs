import sqlite3
import customtkinter as ctk
import tkinter.messagebox as tkmb
import dashboard



con = sqlite3.connect("users.db")
# Create a cursor object
cur = con.cursor()

# Create the users table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    staff_id INTEGER NOT NULL
)
""")

app = ctk.CTk()
app.title("Container Freight Station System")
app.geometry("500x500")

user_entry = None
user_pass = None
user_id = None
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




def login():
    global user_entry, user_pass, user_id

    app.withdraw()
    #app.destroy()

    # Getting the user input from entry widgets
    entered_username = user_entry.get()
    entered_password = int(user_pass.get())
    entered_staffID = user_id.get()

    if not entered_username or not entered_password or not entered_staffID:
        tkmb.showerror("Error", "All fields are required.")
        return

    # Fetch user's credentials from the database
    cur.execute("SELECT username, password, id FROM users WHERE username=?", (entered_username,))
    user = cur.fetchone()

    if user:
        stored_username, stored_password, stored_staffID = user

        if entered_password == stored_password and entered_staffID == str(stored_staffID):
            tkmb.showinfo(title='Login Successful', message='You have logged in Successfully')
            import dashboard
            dashboard.Dashboard(app)
            # Creating new window
            new_window = ctk.CTk()
            new_window.geometry("1050x900")
            ctk.CTkLabel(new_window, text="").pack()
            new_window.title("Home")

            dashboard_obj = dashboard.Dashboard(new_window)
            app.destroy()

            new_window.mainloop()

        elif entered_password != stored_password:
            tkmb.showwarning(title='Wrong password', message='Please check your password')
        elif entered_staffID != str(stored_staffID):
            tkmb.showwarning(title='Wrong ID', message='Please check your ID')

    else:
        tkmb.showwarning(title='User not found', message='Please check your username')



#def add_container():
    # Implement add container logic here
  #  pass

#def clear_and_bill():
    # Implement clear and bill services logic here
 #   pass


def show_dashboard(app):
    # ...
    dashboard(app)
    # ...
def perform_service(app):
    # Implement perform services logic here
    pass

def login_window():
    global user_entry, user_pass, user_id

    login_window = ctk.CTk()
    login_window.geometry("500x500")
    ctk.CTkLabel(login_window, text="Admin Login").pack(pady=20)
    login_window.grab_set()
    app.withdraw()


    # Set the label
    label = ctk.CTkLabel(login_window, text="This is the Login page")
    label.pack(pady=20)

    # Create a frame
    frame = ctk.CTkFrame(master=login_window)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    # Set the label inside the frame
    label = ctk.CTkLabel(master=frame, text='CFS Login')
    label.pack(pady=12, padx=10)

    # Create the text box for taking username input from user
    user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
    user_entry.pack(pady=12, padx=10)

    # Create a text box for taking password input from user
    user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    user_pass.pack(pady=12, padx=10)

    user_id = ctk.CTkEntry(master=frame, placeholder_text="id", show="")
    user_id.pack(pady=12, padx=10)

    # Create a login button to login
    button = ctk.CTkButton(master=frame, text='Login', command= login)
    button.pack(pady=12, padx=10)

    # Create a remember me checkbox
    checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me', command=save())
    checkbox.pack(pady=12, padx=10)

    login_window.mainloop()
    #app.destroy()


def save():
    # Check if the "Remember Me" checkbox is checked
    if checkbox.get() == 1:
        # Get the user input from the entry widgets
        username = user_entry.get()
        password = user_pass.get()
        staff_id = user_id.get()

        # Insert the user information into the database
        cur.execute("""
            INSERT INTO users (username, password, staff_id)
            VALUES (?, ?, ?)
            """, (username, password, staff_id))

        # Commit the changes
        con.commit()

def main():
    global user_entry, user_pass, user_id

    app = ctk.CTk()
    app.geometry("500x500")
    app.title("Container freight station")

    login_window()

    #app.mainloop()

# Creating the main application window
app = ctk.CTk()
app.geometry("500x500")
app.title("Container freight station")

# Set the label
label = ctk.CTkLabel(app, text="This is the Login page")
label.pack(pady=20)

# Create a frame
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

# Set the label inside the frame
label = ctk.CTkLabel(master=frame, text='CFS Login')
label.pack(pady=12, padx=10)

# Create the text box for taking username input from user
user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

# Create a text box for taking password input from user
user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

user_id = ctk.CTkEntry(master=frame, placeholder_text="id", show="")
user_id.pack(pady=12, padx=10)

# Create a login button to login
button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

# Create a remember me checkbox
checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

# Start the main event loop
#app.mainloop()