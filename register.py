import customtkinter
import subprocess, sys
from tkinter import messagebox
from database.connection import get_db
import hashlib

app = customtkinter.CTk()
customtkinter.set_appearance_mode("light")
app.geometry("900x600")
app.title("Register")
app.resizable(True, True)

def register_user():
    db = get_db()
    users = db.users
    u = username_entry.get().strip()
    p = password_entry.get().strip()
    cp = confirm_password_entry.get().strip()
    r = role_option.get().strip()

    if not (u and p and cp and r):
        messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        return

    if p != cp:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    if users.find_one({"username": u}):
        messagebox.showerror("Error", "Username already exists.")
        return

    # 🔒 hash password with sha256
    hashed = hashlib.sha256(p.encode()).hexdigest()
    users.insert_one({"username": u, "password": hashed, "role": r})

    messagebox.showinfo("Success", f"Registered as {r}!")
    app.destroy()
    subprocess.run([sys.executable, "login.py"])

# ================== UI ===================
frame = customtkinter.CTkFrame(master=app, width=400)
frame.place(relx=0.5, rely=0.5, anchor="center")

customtkinter.CTkLabel(master=frame, text="Register", font=("Arial", 24)).pack(pady=20)

username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
username_entry.pack(pady=10, padx=20)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_entry.pack(pady=10, padx=20)

confirm_password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Confirm Password", show="*")
confirm_password_entry.pack(pady=10, padx=20)

role_option = customtkinter.CTkOptionMenu(master=frame, values=["Admin", "Receptionist", "Doctor"])
role_option.pack(pady=10)
role_option.set("Admin")

customtkinter.CTkButton(master=frame, text="Register", command=register_user).pack(pady=20)

app.mainloop()
