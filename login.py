import customtkinter
import subprocess, sys
from tkinter import messagebox
from database.connection import get_db
import hashlib

app = customtkinter.CTk()
customtkinter.set_appearance_mode("light") 
app.geometry("900x600")
app.title("Login")
app.resizable(True, True)

def login_user():
    db = get_db()
    users = db.users
    u = username_entry.get().strip()
    p = password_entry.get().strip()
    r = role_option.get().strip()

    if not u or not p or not r:
        messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        return

    # ✅ find user by username & role
    user = users.find_one({"username": u, "role": r})

    if user:
        # hash the entered password and compare
        hashed_input = hashlib.sha256(p.encode()).hexdigest()
        if user["password"] == hashed_input:
            app.destroy()
            subprocess.run([sys.executable, "dashboard.py", u])
            return

    # if no match
    messagebox.showerror("Login Failed", "Invalid username, password, or role.")

frame = customtkinter.CTkFrame(master=app, width=400)
frame.place(relx=0.5, rely=0.5, anchor="center")

customtkinter.CTkLabel(master=frame, text="Login", font=("Arial", 24)).pack(pady=20)

username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
username_entry.pack(pady=10, padx=20)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_entry.pack(pady=10, padx=20)

role_option = customtkinter.CTkOptionMenu(master=frame, values=["Admin", "Receptionist", "Doctor"])
role_option.pack(pady=10)
role_option.set("Admin")  # Default value

customtkinter.CTkButton(master=frame, text="Login", command=login_user).pack(pady=20)

app.mainloop()
