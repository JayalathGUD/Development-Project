import customtkinter
from datetime import datetime
import sys

from pages.patients import PatientsPage
from pages.appointments import AppointmentsPage
from pages.doctors import DoctorsPage
from pages.billing import BillingPage
from pages.new_user import NewUserPage
from pages.settings import SettingsPage
from pages.pharmacy import PharmacyPage


username = sys.argv[1] if len(sys.argv) > 1 else "Admin"

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1400x800")
app.title("MedCare - Hospital Management System")
app.resizable(True, True)

# -------------- Header ---------------- #
header = customtkinter.CTkFrame(
    app, 
    height=80, 
    fg_color="#2E86AB",
    corner_radius=0
)
header.pack(fill="x")

# Logo and title
logo_frame = customtkinter.CTkFrame(header, fg_color="transparent", width=300)
logo_frame.pack(side="left", padx=20)

customtkinter.CTkLabel(
    logo_frame,
    text="⚕️",
    font=("Arial", 28),
).pack(side="left", padx=(0, 10))

customtkinter.CTkLabel(
    logo_frame,
    text="MedCare Hospital",
    font=("Arial", 22, "bold"),
    text_color="white"
).pack(side="left")

# User info and clock
user_clock_frame = customtkinter.CTkFrame(header, fg_color="transparent")
user_clock_frame.pack(side="right", padx=20)

greeting = customtkinter.CTkLabel(
    user_clock_frame,
    text=f"Welcome, {username} 👋",
    font=("Arial", 16),
    text_color="white"
)
greeting.pack(anchor="e", pady=(10, 0))

clock_label = customtkinter.CTkLabel(
    user_clock_frame,
    text="",
    font=("Arial", 14),
    text_color="white"
)
clock_label.pack(anchor="e")

def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y  |  %I:%M:%S %p")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# -------------- Sidebar ---------------- #
sidebar = customtkinter.CTkFrame(
    app, 
    width=250, 
    fg_color="#F8FBFF",
    corner_radius=0
)
sidebar.pack(side="left", fill="y")

# Profile section
profile_frame = customtkinter.CTkFrame(sidebar, fg_color="transparent")
profile_frame.pack(pady=30)

# Profile icon
profile_icon = customtkinter.CTkLabel(
    profile_frame,
    text="👨‍💼" if username.lower() == "admin" else "👨‍⚕️",
    font=("Arial", 40),
)
profile_icon.pack()

customtkinter.CTkLabel(
    profile_frame,
    text=username,
    font=("Arial", 18, "bold"),
    text_color="#2E4C80"
).pack(pady=(10, 0))

customtkinter.CTkLabel(
    profile_frame,
    text="Administrator",
    font=("Arial", 12),
    text_color="#6B7280"
).pack()

# Navigation menu
customtkinter.CTkLabel(
    sidebar, 
    text="MAIN NAVIGATION", 
    font=("Arial", 12, "bold"),
    text_color="#6B7280"
).pack(anchor="w", padx=20, pady=(40, 10))

nav_buttons = [
    ("🏠 Patients", PatientsPage),
    ("📅 Appointments", AppointmentsPage),
    ("👨‍⚕️ Doctors", DoctorsPage),
    ("➕ New User", NewUserPage),
    ("💊 Pharmacy", PharmacyPage),   # 👈 Added here
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
        font=("Arial", 16),
        height=50,
        fg_color="transparent",
        text_color="#4B5563",
        hover_color="#E5E7EB",
        anchor="w",
        corner_radius=8,
        command=lambda p=page: load_page(p)
    )
    btn.pack(fill="x", padx=10, pady=5)

customtkinter.CTkButton(
    sidebar, 
    text="🚪 Logout", 
    fg_color="#EF4444", 
    hover_color="#DC2626",
    text_color="white",
    font=("Arial", 14),
    height=40,
    command=app.destroy
).pack(side="bottom", pady=20, padx=10, fill="x")

# -------------- Main Content ---------------- #
content = customtkinter.CTkFrame(app, fg_color="#FFFFFF")
content.pack(side="right", expand=True, fill="both", padx=20, pady=20)

# Dashboard overview cards (only shown when no page is loaded)
overview_frame = customtkinter.CTkFrame(content, fg_color="transparent")
overview_frame.pack(fill="both", expand=True)

customtkinter.CTkLabel(
    overview_frame,
    text="Dashboard Overview",
    font=("Arial", 24, "bold"),
    text_color="#2E4C80"
).pack(pady=(20, 30))

stats_frame = customtkinter.CTkFrame(overview_frame, fg_color="transparent")
stats_frame.pack(fill="x", pady=(0, 30))

stats = [
    {"title": "Total Patients", "value": "1,248", "icon": "👥", "change": "+12%"},
    {"title": "Today's Appointments", "value": "36", "icon": "📅", "change": "+5%"},
    {"title": "Available Doctors", "value": "24", "icon": "🩺", "change": "+2%"},
    {"title": "Revenue", "value": "$12,845", "icon": "💰", "change": "+8%"},
]

for i, stat in enumerate(stats):
    card = customtkinter.CTkFrame(
        stats_frame,
        width=200,
        height=120,
        fg_color="#F9FAFB",
        border_color="#E5E7EB",
        border_width=1,
        corner_radius=12
    )
    card.grid(row=0, column=i, padx=(0, 15), sticky="nsew")
    card.grid_propagate(False)
    
    # Icon
    customtkinter.CTkLabel(
        card,
        text=stat["icon"],
        font=("Arial", 24)
    ).place(x=20, y=20)
    
    # Value
    customtkinter.CTkLabel(
        card,
        text=stat["value"],
        font=("Arial", 24, "bold"),
        text_color="#1F2937"
    ).place(x=20, y=50)
    
    # Title
    customtkinter.CTkLabel(
        card,
        text=stat["title"],
        font=("Arial", 12),
        text_color="#6B7280"
    ).place(x=20, y=85)
    
    # Change indicator
    customtkinter.CTkLabel(
        card,
        text=stat["change"],
        font=("Arial", 10),
        text_color="#10B981"
    ).place(x=160, y=20)

# Configure grid weights
stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Recent activity section
activity_frame = customtkinter.CTkFrame(overview_frame, fg_color="transparent")
activity_frame.pack(fill="both", expand=True)

customtkinter.CTkLabel(
    activity_frame,
    text="Recent Activity",
    font=("Arial", 20, "bold"),
    text_color="#2E4C80"
).pack(anchor="w", pady=(0, 15))

# Activity list
activities = [
    {"action": "New patient registered", "time": "10 mins ago", "user": "Dr. Smith"},
    {"action": "Appointment completed", "time": "30 mins ago", "user": "Dr. Johnson"},
    {"action": "Lab results uploaded", "time": "1 hour ago", "user": "Nurse Williams"},
    {"action": "Prescription issued", "time": "2 hours ago", "user": "Dr. Brown"},
    {"action": "Billing payment received", "time": "3 hours ago", "user": "Receptionist"},
]

for activity in activities:
    activity_item = customtkinter.CTkFrame(
        activity_frame,
        height=60,
        fg_color="#F9FAFB",
        border_color="#E5E7EB",
        border_width=1,
        corner_radius=8
    )
    activity_item.pack(fill="x", pady=5)
    
    customtkinter.CTkLabel(
        activity_item,
        text=activity["action"],
        font=("Arial", 14),
        text_color="#374151"
    ).place(x=15, y=10)
    
    customtkinter.CTkLabel(
        activity_item,
        text=activity["user"],
        font=("Arial", 12),
        text_color="#6B7280"
    ).place(x=15, y=35)
    
    customtkinter.CTkLabel(
        activity_item,
        text=activity["time"],
        font=("Arial", 12),
        text_color="#9CA3AF"
    ).place(x=250, y=22)

# Load the default page (this will replace the overview)
load_page(PatientsPage)

app.mainloop()