import customtkinter
from datetime import datetime
import sys

from pages.patients import PatientsPage
from pages.appointments import AppointmentsPage
from pages.doctors import DoctorsPage
from pages.billing import BillingPage
from pages.new_user import NewUserPage
from pages.settings import SettingsPage

username = sys.argv[1] if len(sys.argv) > 1 else "Admin"

customtkinter.set_appearance_mode("light")  # or "dark"
customtkinter.set_default_color_theme("blue")  # You can customize themes

app = customtkinter.CTk()
app.geometry("1200x700")
app.title("Hospital Management Dashboard")
app.resizable(True, True)

# -------------- Header ---------------- #
header = customtkinter.CTkFrame(app, height=60, fg_color="#f1f1f1")
header.pack(fill="x")

customtkinter.CTkLabel(
    header,
    text="🏥 Hospital Dashboard",
    font=("Arial", 22, "bold")
).place(x=20, y=15)

greeting = customtkinter.CTkLabel(
    header,
    text=f"Welcome, {username} 👋",
    font=("Arial", 18)
)
greeting.place(relx=0.5, rely=0.5, anchor="center")

clock_label = customtkinter.CTkLabel(
    header,
    text="",
    font=("Arial", 16)
)
clock_label.place(relx=0.98, y=20, anchor="ne")

def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y  |  %I:%M:%S %p")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# -------------- Sidebar ---------------- #
sidebar = customtkinter.CTkFrame(app, width=200, fg_color="#e6e6e6")
sidebar.pack(side="left", fill="y")

customtkinter.CTkLabel(sidebar, text="Menu", font=("Arial", 18, "bold")).pack(pady=20)

nav_buttons = [
    ("🏠 Patients", PatientsPage),
    ("📅 Appointments", AppointmentsPage),
    ("👨‍⚕️ Doctors", DoctorsPage),
    ("➕ New User", NewUserPage),
    ("💳 Billing", BillingPage),
    ("⚙️ Settings", SettingsPage),
]

def load_page(page_cls):
    for widget in content.winfo_children():
        widget.destroy()
    page = page_cls(content)
    page.pack(expand=True, fill="both")

for text, page in nav_buttons:
    btn = customtkinter.CTkButton(
        sidebar,
        text=text,
        font=("Arial", 14),
        width=180,
        command=lambda p=page: load_page(p)
    )
    btn.pack(pady=6, padx=10)

customtkinter.CTkButton(
    sidebar, text="🚪 Logout", fg_color="red", command=app.destroy, width=180
).pack(side="bottom", pady=30)

# -------------- Main Content ---------------- #
content = customtkinter.CTkFrame(app)
content.pack(side="right", expand=True, fill="both")

load_page(PatientsPage)

app.mainloop()
