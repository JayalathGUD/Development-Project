import customtkinter
import subprocess, sys
from tkinter import messagebox
from database.connection import get_db
import hashlib
from PIL import Image, ImageTk
import tkinter as tk

# Set appearance and color theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1100x700")
app.title("MedCare - Login System")
app.resizable(True, True)

# Function to handle login
def login_user():
    db = get_db()
    users = db.users
    u = username_entry.get().strip()
    p = password_entry.get().strip()
    r = role_option.get().strip()

    if not u or not p or not r:
        messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        return

    # Hash entered password
    hashed = hashlib.sha256(p.encode()).hexdigest()

    # Check user in DB
    user = users.find_one({"username": u, "password": hashed, "role": r})

    if user:
        app.destroy()
        # Redirect based on role
        if r == "Admin":
            subprocess.run([sys.executable, "dashboard.py", u])
        elif r == "Doctor":
            subprocess.run([sys.executable, "doctor_dashboard.py", u])
        elif r == "Receptionist":
            subprocess.run([sys.executable, "receptionist_dashboard.py", u])
    else:
        messagebox.showerror("Login Failed", "Invalid username, password, or role.")

# Create main background frame
main_frame = customtkinter.CTkFrame(master=app, fg_color=("#E6F0FF", "#1A3E6F"), corner_radius=0)
main_frame.pack(fill="both", expand=True)

# Left panel with medical imagery
left_panel = customtkinter.CTkFrame(master=main_frame, width=450, fg_color=("#3B8ED0", "#1F538D"), corner_radius=0)
left_panel.pack(side="left", fill="y", padx=(0, 20))
left_panel.pack_propagate(False)

# Medical icon/logo
logo_label = customtkinter.CTkLabel(
    master=left_panel, 
    text="⚕️", 
    font=("Arial", 60),
    text_color="white"
)
logo_label.pack(pady=(80, 20))

# Welcome text
welcome_label = customtkinter.CTkLabel(
    master=left_panel,
    text="Welcome to MedCare",
    font=("Arial", 28, "bold"),
    text_color="white"
)
welcome_label.pack(pady=(0, 10))

# Subtitle
subtitle_label = customtkinter.CTkLabel(
    master=left_panel,
    text="Medical Management System",
    font=("Arial", 16),
    text_color="white"
)
subtitle_label.pack(pady=(0, 50))

# Decorative medical icons
icons_frame = customtkinter.CTkFrame(master=left_panel, fg_color="transparent")
icons_frame.pack(pady=(50, 0))

icon1 = customtkinter.CTkLabel(
    master=icons_frame,
    text="❤️",
    font=("Arial", 30),
    text_color="white"
)
icon1.pack(side="left", padx=15)

icon2 = customtkinter.CTkLabel(
    master=icons_frame,
    text="🩺",
    font=("Arial", 30),
    text_color="white"
)
icon2.pack(side="left", padx=15)

icon3 = customtkinter.CTkLabel(
    master=icons_frame,
    text="💊",
    font=("Arial", 30),
    text_color="white"
)
icon3.pack(side="left", padx=15)

# Right panel with login form
right_panel = customtkinter.CTkFrame(master=main_frame, fg_color="white", corner_radius=20)
right_panel.pack(side="right", fill="both", expand=True, padx=(0, 40), pady=40)

# Login form container
form_frame = customtkinter.CTkFrame(master=right_panel, fg_color="white")
form_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title_label = customtkinter.CTkLabel(
    master=form_frame, 
    text="Login to Your Account", 
    font=("Arial", 28, "bold"),
    text_color="#2E4C80"
)
title_label.pack(pady=(0, 30))

# Username field
username_entry = customtkinter.CTkEntry(
    master=form_frame, 
    placeholder_text="Username",
    width=320,
    height=50,
    corner_radius=12,
    border_color="#3B8ED0",
    fg_color="#F8FBFF",
    text_color="#2E4C80",
    font=("Arial", 14)
)
username_entry.pack(pady=(0, 20))

# Password field
password_entry = customtkinter.CTkEntry(
    master=form_frame, 
    placeholder_text="Password", 
    show="•",
    width=320,
    height=50,
    corner_radius=12,
    border_color="#3B8ED0",
    fg_color="#F8FBFF",
    text_color="#2E4C80",
    font=("Arial", 14)
)
password_entry.pack(pady=(0, 20))

# Role selection
role_option = customtkinter.CTkOptionMenu(
    master=form_frame, 
    values=["Admin", "Receptionist", "Doctor"],
    width=320,
    height=50,
    corner_radius=12,
    button_color="#3B8ED0",
    fg_color="#F8FBFF",
    text_color="#2E4C80",
    font=("Arial", 14),
    dropdown_font=("Arial", 14),
    dropdown_text_color="#2E4C80",
    dropdown_fg_color="#F8FBFF",
    dropdown_hover_color="#3B8ED0"
)
role_option.set("Select Role")
role_option.pack(pady=(0, 30))

# Login button
login_button = customtkinter.CTkButton(
    master=form_frame, 
    text="Login", 
    command=login_user,
    width=320,
    height=50,
    corner_radius=12,
    font=("Arial", 16, "bold"),
    fg_color="#3B8ED0",
    hover_color="#2A6CA8",
    text_color="white"
)
login_button.pack(pady=(0, 20))

# Forgot password link
forgot_link = customtkinter.CTkLabel(
    master=form_frame,
    text="Forgot Password?",
    font=("Arial", 12, "underline"),
    text_color="#3B8ED0",
    cursor="hand2"
)
forgot_link.pack(pady=(0, 30))

# Footer text
footer_label = customtkinter.CTkLabel(
    master=right_panel,
    text="© 2023 MedCare Hospital Management System. All rights reserved.",
    font=("Arial", 10),
    text_color="gray"
)
footer_label.pack(side="bottom", pady=20)

# Add some decorative elements
decoration1 = customtkinter.CTkFrame(master=right_panel, width=80, height=80, fg_color="transparent")
decoration1.place(relx=0.1, rely=0.1)
decoration1_label = customtkinter.CTkLabel(
    master=decoration1,
    text="➕",
    font=("Arial", 40),
    text_color="#3B8ED0"
)
decoration1_label.place(relx=0.5, rely=0.5, anchor="center")

decoration2 = customtkinter.CTkFrame(master=right_panel, width=60, height=60, fg_color="transparent")
decoration2.place(relx=0.9, rely=0.85)
decoration2_label = customtkinter.CTkLabel(
    master=decoration2,
    text="❤️",
    font=("Arial", 30),
    text_color="#3B8ED0"
)
decoration2_label.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()