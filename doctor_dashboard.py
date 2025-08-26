import customtkinter
from datetime import datetime
import sys
from tkinter import ttk, messagebox
from bson import ObjectId   # for MongoDB ObjectId
from database.connection import get_db   # <-- use your DB connection

# ------------------ Database ------------------ #
db = get_db()
appointments_col = db.appointments   # collection: appointments

# ------------------ Main Window ------------------ #
username = sys.argv[1] if len(sys.argv) > 1 else "Doctor"

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1200x700")
app.title("Doctor Dashboard")
app.resizable(True, True)

# ------------------ Header ------------------ #
header = customtkinter.CTkFrame(app, height=60, fg_color="#f1f1f1")
header.pack(fill="x")

customtkinter.CTkLabel(
    header, text="👨‍⚕️ Doctor Dashboard", font=("Arial", 22, "bold")
).place(x=20, y=15)

greeting = customtkinter.CTkLabel(
    header, text=f"Welcome, Dr. {username} 👋", font=("Arial", 18)
)
greeting.place(relx=0.5, rely=0.5, anchor="center")

clock_label = customtkinter.CTkLabel(header, text="", font=("Arial", 16))
clock_label.place(relx=0.98, y=20, anchor="ne")

def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y  |  %I:%M:%S %p")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# ------------------ Sidebar ------------------ #
sidebar = customtkinter.CTkFrame(app, width=200, fg_color="#e6e6e6")
sidebar.pack(side="left", fill="y")

customtkinter.CTkLabel(sidebar, text="Menu", font=("Arial", 18, "bold")).pack(pady=20)

# ------------------ Pages ------------------ #
def show_appointments(content):
    """Doctor can view and update real appointments"""
    for widget in content.winfo_children():
        widget.destroy()

    customtkinter.CTkLabel(content, text="📅 My Appointments", font=("Arial", 22, "bold")).pack(pady=20)

    # Treeview for appointments
    columns = ("id", "patient", "date", "time", "status")
    tree = ttk.Treeview(content, columns=columns, show="headings", height=12)
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    # Load data from DB
    def load_data():
        tree.delete(*tree.get_children())
        for appt in appointments_col.find():
            tree.insert(
                "", "end",
                values=(
                    str(appt["_id"]),
                    appt.get("patient", ""),
                    appt.get("date", ""),
                    appt.get("time", ""),
                    appt.get("status", "Pending")
                )
            )

    load_data()

    # Mark as Done button
    def mark_done():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an appointment from the list.")
            return

        appt_values = tree.item(selected[0], "values")
        appt_id = appt_values[0]   # first column = _id

        try:
            result = appointments_col.update_one(
                {"_id": ObjectId(appt_id)}, {"$set": {"status": "Done"}}
            )
        except:
            # if _id is stored as string, not ObjectId
            result = appointments_col.update_one(
                {"_id": appt_id}, {"$set": {"status": "Done"}}
            )

        if result.matched_count > 0:
            messagebox.showinfo("Updated", f"Appointment {appt_id} marked as Done ✅")
            load_data()
        else:
            messagebox.showerror("Not Found", f"No appointment found with ID {appt_id}")

    customtkinter.CTkButton(content, text="✅ Mark as Done", command=mark_done).pack(pady=10)


def show_patients(content):
    for widget in content.winfo_children():
        widget.destroy()
    customtkinter.CTkLabel(content, text="🧑 Patients Assigned", font=("Arial", 24)).pack(pady=50)


def show_prescription(content):
    for widget in content.winfo_children():
        widget.destroy()
    customtkinter.CTkLabel(content, text="📝 Prescription Page", font=("Arial", 24)).pack(pady=50)


def show_settings(content):
    for widget in content.winfo_children():
        widget.destroy()
    customtkinter.CTkLabel(content, text="⚙️ Doctor Settings", font=("Arial", 24)).pack(pady=50)

# ------------------ Sidebar Buttons ------------------ #
menu_buttons = [
    ("📅 My Appointments", show_appointments),
    ("🧑 Patients", show_patients),
    ("📝 Write Prescription", show_prescription),
    ("⚙️ Settings", show_settings),
]

def load_page(page):
    for widget in content.winfo_children():
        widget.destroy()
    page(content)

for text, page in menu_buttons:
    btn = customtkinter.CTkButton(sidebar, text=text, font=("Arial", 14), width=180, command=lambda p=page: load_page(p))
    btn.pack(pady=6, padx=10)

customtkinter.CTkButton(sidebar, text="🚪 Logout", fg_color="red", command=app.destroy, width=180).pack(side="bottom", pady=30)

# ------------------ Main Content ------------------ #
content = customtkinter.CTkFrame(app)
content.pack(side="right", expand=True, fill="both")

# Default page
load_page(show_appointments)

app.mainloop()
