import subprocess
import sqlite3
import customtkinter as ctk
import tkinter.messagebox as tkmb
import dashboard
import admin
import homepage



con = sqlite3.connect("agents.db")
# Create a cursor object
cur = con.cursor()

# Create the users table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

app = ctk.CTk()
app.title("Container Freight Station System")
app.geometry("500x500")
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




def logins():
    # Pre-defined username and password
    username = "weston"
    password = "12345"

    username1 = "clearing agent"
    password1 = "20104"

    # Getting the user input from entry widgets
    entered_username = user_entry.get()
    entered_password = user_pass.get()

    # Checking if the entered username and password match the predefined values
    if (entered_username == username and entered_password == password or
        entered_username == username1 and entered_password == password1):
        tkmb.showinfo(title="Login Successful", message="You have logged in Successfully", )

        # Creating a new window with a message


        import homepage
        homepage.Homepage(app)
        # Creating new window
        new_window = ctk.CTk()
        new_window.geometry("1050x900")
        ctk.CTkLabel(new_window, text="").pack()
        new_window.title("Home")

        homepage_obj = homepage.Homepage(new_window)
        #app.destroy()


        #new_window.mainloop()

    elif (entered_username == username and entered_password != password or
          entered_username == username1 and entered_password != password1):
        tkmb.showwarning(title='Wrong password', message='Please check your password')
    elif (entered_username != username and entered_password == password or
          entered_username != username1 and entered_password == password1):
        tkmb.showwarning(title='Wrong username', message='Please check your username')
    else:
        tkmb.showwarning(title='Wrong password', message='Please check your password and username')



#def add_container():
    # Implement add container logic here
  #  pass

def show_admin():
    admin.show_admin_login_window(app)
    app.destroy()


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

def show_login_window():
    login_window = ctk.CTk()
    login_window.geometry("500x500")
    ctk.CTkLabel(login_window, text="").pack(pady=20)

    admin.login_window()
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

    # Create a login button to login
    button = ctk.CTkButton(master=frame, text='Login', command=lambda: logins(app, user_entry, user_pass))
    button.pack(pady=12, padx=10)

    # Create a remember me checkbox
    checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me', command=save())
    checkbox.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text_color='black', text='Login as admin', command= show_login_window())
    button.configure(bg='white', underline=True)
    button.pack(pady=12, padx=10)

    login_window.mainloop(app)
    app.withdraw()


def save():
    # Check if the "Remember Me" checkbox is checked
    if checkbox.get() == 1:
        # Get the user input from the entry widgets
        username = user_entry.get()
        password = user_pass.get()

        # Insert the user information into the database
        cur.execute("""
            INSERT INTO agents (username, password)
            VALUES (?, ?, ?)
            """, (username, password))

        # Commit the changes
        con.commit()

def main():
    app = ctk.CTk()
    app.geometry("500x500")
    app.title("Container freight station")

    show_login_window(app)

    app.mainloop()
    app.withdraw()

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

# Create a login button to login
button = ctk.CTkButton(master=frame, text='Login', command=logins)
button.pack(pady=12, padx=10)

# Create a remember me checkbox
checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)


button = ctk.CTkButton(master=frame, text='Login as admin', command=lambda: show_login_window())
button.pack(pady=52, padx=50)

# Start the main event loop
app.mainloop()