import customtkinter
from datetime import datetime
from tkinter import ttk, messagebox
from bson import ObjectId
from database.connection import get_db

# ------------------ Database ------------------ #
db = get_db()
appointments_col = db.appointments
medicines_col = db.medicines
bills_col = db.bills   # new bills collection

# ------------------ Main Window ------------------ #
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1400x850")
app.title("Doctor Dashboard")
app.resizable(True, True)

# ------------------ Header ------------------ #
header = customtkinter.CTkFrame(app, height=70, fg_color="#f1f1f1")
header.pack(fill="x")

customtkinter.CTkLabel(
    header,
    text="👨‍⚕️ Doctor Dashboard",
    font=("Arial", 26, "bold")
).place(x=20, y=15)

clock_label = customtkinter.CTkLabel(header, text="", font=("Arial", 18))
clock_label.place(relx=0.98, y=20, anchor="ne")

def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y  |  %I:%M:%S %p")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# ------------------ Style for Tables ------------------ #
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
style.configure("Treeview", font=("Arial", 15), rowheight=38)

# ------------------ Appointments Table ------------------ #
customtkinter.CTkLabel(app, text="📅 My Appointments", font=("Arial", 22, "bold")).pack(pady=10)

appt_columns = ("id", "patient", "date", "time", "status")
appt_tree = ttk.Treeview(app, columns=appt_columns, show="headings", height=10)
appt_tree.pack(padx=20, pady=10, fill="x")

for col in appt_columns:
    appt_tree.heading(col, text=col.capitalize())
    appt_tree.column(col, width=220, anchor="center")

def load_appointments():
    appt_tree.delete(*appt_tree.get_children())
    for appt in appointments_col.find():
        status = appt.get("status", "Pending")
        appt_tree.insert(
            "",
            "end",
            values=(
                str(appt["_id"]),
                appt.get("patient", ""),
                appt.get("date", ""),
                appt.get("time", ""),
                status,
            ),
            tags=(status,)
        )
    appt_tree.tag_configure("Pending", background="#ffe6e6")  # red
    appt_tree.tag_configure("Done", background="#e6ffe6")     # green

load_appointments()

# ------------------ Treatment Form ------------------ #
def open_treatment_form(appt_id, patient_name):
    win = customtkinter.CTkToplevel(app)
    win.geometry("700x600")
    win.title("Treatment Form")

    customtkinter.CTkLabel(win, text=f"Treatment for {patient_name}", font=("Arial", 20, "bold")).pack(pady=10)

    # Description
    customtkinter.CTkLabel(win, text="📝 Treatment Description:").pack(anchor="w", padx=20)
    desc_entry = customtkinter.CTkTextbox(win, width=600, height=100)
    desc_entry.pack(padx=20, pady=10)

    # Medicines table
    customtkinter.CTkLabel(win, text="💊 Prescribe Medicines (double-click row to set qty)").pack(anchor="w", padx=20)

    med_columns = ("id", "name", "stock", "price", "qty")
    med_tree = ttk.Treeview(win, columns=med_columns, show="headings", height=8)
    med_tree.pack(padx=20, pady=10, fill="x")

    for col in med_columns:
        med_tree.heading(col, text=col.capitalize())
        med_tree.column(col, width=120, anchor="center")

    prescribed = {}

    def load_meds():
        med_tree.delete(*med_tree.get_children())
        for med in medicines_col.find():
            med_tree.insert(
                "",
                "end",
                values=(
                    str(med["_id"]),
                    med.get("name", ""),
                    med.get("stock", "N/A"),
                    med.get("price", "N/A"),
                    prescribed.get(str(med["_id"]), 0)
                )
            )

    def on_double_click_med(event):
        selected = med_tree.selection()
        if not selected:
            return
        med_values = med_tree.item(selected[0], "values")
        med_id, med_name = med_values[0], med_values[1]

        qty_win = customtkinter.CTkInputDialog(
            text=f"Enter quantity for {med_name}:", title="Set Quantity"
        )
        qty = qty_win.get_input()

        if qty and qty.isdigit():
            prescribed[med_id] = int(qty)
            load_meds()

    med_tree.bind("<Double-1>", on_double_click_med)
    load_meds()

    # Save Button
    def save_treatment():
        description = desc_entry.get("1.0", "end").strip()
        if not description:
            messagebox.showerror("Error", "Please enter a treatment description.")
            return

        # Prepare medicines list
        meds_list = []
        for med_id, qty in prescribed.items():
            med = medicines_col.find_one({"_id": ObjectId(med_id)})
            if med:
                meds_list.append({
                    "name": med["name"],
                    "qty": qty,
                    "price": med.get("price", 0),
                    "subtotal": qty * float(med.get("price", 0))
                })

        # Save bill
        bill = {
            "appointment_id": appt_id,
            "patient": patient_name,
            "description": description,
            "medicines": meds_list,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        bills_col.insert_one(bill)

        # Update appointment
        appointments_col.update_one({"_id": ObjectId(appt_id)}, {"$set": {"status": "Done"}})

        messagebox.showinfo("Success", "Treatment saved & bill generated ✅")
        win.destroy()
        load_appointments()

    customtkinter.CTkButton(win, text="💾 Save Treatment", command=save_treatment).pack(pady=20)

# ------------------ Appointment Double Click ------------------ #
def on_double_click_appt(event):
    selected = appt_tree.selection()
    if not selected:
        return
    appt_values = appt_tree.item(selected[0], "values")
    appt_id, patient, status = appt_values[0], appt_values[1], appt_values[4]

    if status == "Done":
        messagebox.showinfo("Info", "This appointment is already marked as Done ✅")
        return

    open_treatment_form(appt_id, patient)

appt_tree.bind("<Double-1>", on_double_click_appt)

# ------------------ Run ------------------ #
app.mainloop()
