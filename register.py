import customtkinter
import subprocess, sys
from tkinter import messagebox
from database.connection import get_db
import hashlib

# Set appearance and color theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1000x700")
app.title("MedCare - Registration")
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

def go_to_login():
    app.destroy()
    subprocess.run([sys.executable, "login.py"])

# ================== UI ===================
# Background frame
background_frame = customtkinter.CTkFrame(master=app, fg_color=("#E6F0FF", "#1A3E6F"), corner_radius=0)
background_frame.pack(fill="both", expand=True)

# Main content frame
main_frame = customtkinter.CTkFrame(master=background_frame, width=500, height=600, corner_radius=20)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Left decorative panel
left_panel = customtkinter.CTkFrame(master=main_frame, width=200, fg_color=("#3B8ED0", "#1F538D"), corner_radius=20)
left_panel.place(relx=0, rely=0, relheight=1)

# Medical icon/logo
logo_label = customtkinter.CTkLabel(
    master=left_panel, 
    text="⚕️", 
    font=("Arial", 40),
    text_color="white"
)
logo_label.place(relx=0.5, rely=0.2, anchor="center")

welcome_label = customtkinter.CTkLabel(
    master=left_panel,
    text="Create Account",
    font=("Arial", 20, "bold"),
    text_color="white"
)
welcome_label.place(relx=0.5, rely=0.3, anchor="center")

message_label = customtkinter.CTkLabel(
    master=left_panel,
    text="Join our medical system",
    font=("Arial", 12),
    text_color="white",
    wraplength=150
)
message_label.place(relx=0.5, rely=0.4, anchor="center")

# Right form panel
form_frame = customtkinter.CTkFrame(master=main_frame, fg_color="transparent")
form_frame.place(relx=0.7, rely=0.5, anchor="center")

# Title
title_label = customtkinter.CTkLabel(
    master=form_frame, 
    text="Create Account", 
    font=("Arial", 24, "bold"),
    text_color="#2E4C80"
)
title_label.pack(pady=(0, 30))

# Username field
username_label = customtkinter.CTkLabel(
    master=form_frame, 
    text="Username", 
    font=("Arial", 12),
    text_color="#374151"
)
username_label.pack(anchor="w", pady=(0, 5))

username_entry = customtkinter.CTkEntry(
    master=form_frame, 
    placeholder_text="Enter your username",
    width=300,
    height=45,
    corner_radius=10,
    border_color="#D1D5DB",
    fg_color="#F8FBFF",
    text_color="#1F2937",
    font=("Arial", 14)
)
username_entry.pack(pady=(0, 15))

# Password field
password_label = customtkinter.CTkLabel(
    master=form_frame, 
    text="Password", 
    font=("Arial", 12),
    text_color="#374151"
)
password_label.pack(anchor="w", pady=(0, 5))

password_entry = customtkinter.CTkEntry(
    master=form_frame, 
    placeholder_text="Enter your password", 
    show="*",
    width=300,
    height=45,
    corner_radius=10,
    border_color="#D1D5DB",
    fg_color="#F8FBFF",
    text_color="#1F2937",
    font=("Arial", 14)
)
password_entry.pack(pady=(0, 15))

# Confirm Password field
confirm_password_label = customtkinter.CTkLabel(
    master=form_frame, 
    text="Confirm Password", 
    font=("Arial", 12),
    text_color="#374151"
)
confirm_password_label.pack(anchor="w", pady=(0, 5))

confirm_password_entry = customtkinter.CTkEntry(
    master=form_frame, 
    placeholder_text="Confirm your password", 
    show="*",
    width=300,
    height=45,
    corner_radius=10,
    border_color="#D1D5DB",
    fg_color="#F8FBFF",
    text_color="#1F2937",
    font=("Arial", 14)
)
confirm_password_entry.pack(pady=(0, 15))

# Role selection
role_label = customtkinter.CTkLabel(
    master=form_frame, 
    text="Role", 
    font=("Arial", 12),
    text_color="#374151"
)
role_label.pack(anchor="w", pady=(0, 5))

role_option = customtkinter.CTkOptionMenu(
    master=form_frame, 
    values=["Admin", "Receptionist", "Doctor"],
    width=300,
    height=45,
    corner_radius=10,
    button_color="#3B8ED0",
    fg_color="#F8FBFF",
    text_color="#1F2937",
    font=("Arial", 14),
    dropdown_font=("Arial", 14),
    dropdown_text_color="#1F2937",
    dropdown_fg_color="#F8FBFF",
    dropdown_hover_color="#3B8ED0"
)
role_option.set("Select Role")
role_option.pack(pady=(0, 20))

# Register button
register_button = customtkinter.CTkButton(
    master=form_frame, 
    text="Register", 
    command=register_user,
    width=300,
    height=45,
    corner_radius=10,
    font=("Arial", 16, "bold"),
    fg_color="#3B8ED0",
    hover_color="#2A6CA8",
    text_color="white"
)
register_button.pack(pady=(0, 15))

# Login link
login_frame = customtkinter.CTkFrame(master=form_frame, fg_color="transparent")
login_frame.pack()

customtkinter.CTkLabel(
    master=login_frame,
    text="Already have an account?",
    font=("Arial", 12),
    text_color="#6B7280"
).pack(side="left")

login_link = customtkinter.CTkLabel(
    master=login_frame,
    text="Login here",
    font=("Arial", 12, "underline"),
    text_color="#3B8ED0",
    cursor="hand2"
)
login_link.pack(side="left", padx=(5, 0))
login_link.bind("<Button-1>", lambda e: go_to_login())

# Footer text
footer_label = customtkinter.CTkLabel(
    master=main_frame,
    text="© 2023 MedCare Hospital Management System. All rights reserved.",
    font=("Arial", 10),
    text_color="gray"
)
footer_label.place(relx=0.5, rely=0.95, anchor="center")

# Add some decorative elements
decoration1 = customtkinter.CTkFrame(master=background_frame, width=80, height=80, fg_color=("#3B8ED0", "#1F538D"), corner_radius=40)
decoration1.place(relx=0.1, rely=0.1)

decoration2 = customtkinter.CTkFrame(master=background_frame, width=60, height=60, fg_color=("#3B8ED0", "#1F538D"), corner_radius=30)
decoration2.place(relx=0.85, rely=0.8)

app.mainloop()