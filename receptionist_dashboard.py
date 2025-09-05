import customtkinter
from datetime import datetime
import sys
from tkinter import ttk, messagebox
from bson import ObjectId
from database.connection import get_db
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# ---------------- Database ---------------- #
db = get_db()
bills_col = db.bills
appointments_col = db.appointments

# ---------------- Get username ---------------- #
username = sys.argv[1] if len(sys.argv) > 1 else "Receptionist"

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1200x700")
app.title("Receptionist Dashboard")
app.resizable(True, True)

# ---------------- Header ---------------- #
header = customtkinter.CTkFrame(app, height=60, fg_color="#f1f1f1")
header.pack(fill="x")

customtkinter.CTkLabel(
    header,
    text="📋 Receptionist Dashboard",
    font=("Arial", 22, "bold")
).place(x=20, y=15)

clock_label = customtkinter.CTkLabel(header, text="", font=("Arial", 16))
clock_label.place(relx=0.98, y=20, anchor="ne")

def update_clock():
    now = datetime.now().strftime("%A, %d %B %Y  |  %I:%M:%S %p")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# ---------------- Sidebar ---------------- #
sidebar = customtkinter.CTkFrame(app, width=200, fg_color="#e6e6e6")
sidebar.pack(side="left", fill="y")

customtkinter.CTkLabel(sidebar, text="Menu", font=("Arial", 18, "bold")).pack(pady=20)

# ---------------- Main Content ---------------- #
content = customtkinter.CTkFrame(app)
content.pack(side="right", expand=True, fill="both")

# ---------------- Billing Page ---------------- #
def load_billing_page(content):
    for widget in content.winfo_children():
        widget.destroy()

    customtkinter.CTkLabel(
        content, text="💳 Billing & Medical Reports", font=("Arial", 22, "bold")
    ).pack(pady=10)

    # Table
    columns = ("id", "patient", "doctor", "created_at")
    bill_tree = ttk.Treeview(content, columns=columns, show="headings", height=12)
    bill_tree.pack(padx=20, pady=10, fill="x")

    for col in columns:
        bill_tree.heading(col, text=col.capitalize())
        bill_tree.column(col, width=250, anchor="center")

    # Load bills
    def load_bills():
        bill_tree.delete(*bill_tree.get_children())
        for bill in bills_col.find().sort("created_at", -1):
            appt_id = bill.get("appointment_id")
            appointment = appointments_col.find_one({"_id": ObjectId(appt_id)}) if appt_id else None
            doctor_name = appointment.get("doctor") if appointment else "N/A"
            doctor_price = float(appointment.get("price", 0)) if appointment else 0.0

            bill_tree.insert(
                "",
                "end",
                values=(
                    str(bill["_id"]),
                    bill.get("patient", ""),
                    f"{doctor_name} (Rs.{doctor_price})",
                    bill.get("created_at", ""),
                ),
            )

    load_bills()

    # Detail box
    detail_box = customtkinter.CTkTextbox(content, width=1000, height=250)
    detail_box.pack(padx=20, pady=15)

    selected_bill_id = {"id": None}  # to keep track for printing

    # Show bill details
    def on_bill_select(event):
        selected = bill_tree.selection()
        if not selected:
            return
        bill_id = bill_tree.item(selected[0], "values")[0]
        selected_bill_id["id"] = bill_id
        bill = bills_col.find_one({"_id": ObjectId(bill_id)})
        if bill:
            detail_box.delete("1.0", "end")
            appt_id = bill.get("appointment_id")
            appointment = appointments_col.find_one({"_id": ObjectId(appt_id)}) if appt_id else None
            doctor_name = appointment.get("doctor") if appointment else "N/A"
            doctor_price = float(appointment.get("price", 0)) if appointment else 0.0

            detail_box.insert("end", f"🧾 Patient: {bill['patient']}\n")
            detail_box.insert("end", f"👨‍⚕️ Doctor: {doctor_name} | Consultation Price: Rs.{doctor_price}\n")
            detail_box.insert("end", f"📅 Date: {bill['created_at']}\n\n")
            detail_box.insert("end", f"📝 Medical Report:\n{bill['description']}\n\n")
            detail_box.insert("end", "💊 Prescribed Medicines:\n")
            
            total_meds = 0
            for med in bill.get("medicines", []):
                subtotal = med["subtotal"]
                total_meds += subtotal
                detail_box.insert(
                    "end",
                    f" - {med['name']} (x{med['qty']}) = Rs.{subtotal}\n"
                )
            total_bill = total_meds + doctor_price
            detail_box.insert("end", f"\n💰 Total Bill: Rs.{total_bill} (Doctor + Medicines)\n")

    bill_tree.bind("<<TreeviewSelect>>", on_bill_select)

    # ---------------- Print Bill Button ---------------- #
    def print_bill():
        bill_id = selected_bill_id.get("id")
        if not bill_id:
            messagebox.showwarning("Select Bill", "Please select a bill first!")
            return
        bill = bills_col.find_one({"_id": ObjectId(bill_id)})
        if not bill:
            messagebox.showerror("Error", "Bill not found!")
            return
        
        appt_id = bill.get("appointment_id")
        appointment = appointments_col.find_one({"_id": ObjectId(appt_id)}) if appt_id else None
        doctor_name = appointment.get("doctor") if appointment else "N/A"
        doctor_price = float(appointment.get("price", 0)) if appointment else 0.0

        filename = f"Bill_{bill_id}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        y = height - 50
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, "🏥 Hospital Bill")
        y -= 40

        c.setFont("Helvetica", 14)
        c.drawString(50, y, f"Patient: {bill['patient']}")
        y -= 25
        c.drawString(50, y, f"Doctor: {doctor_name} | Consultation Price: Rs.{doctor_price}")
        y -= 25
        c.drawString(50, y, f"Date: {bill['created_at']}")
        y -= 40
        c.drawString(50, y, "📝 Medical Report:")
        y -= 25
        text = bill.get("description", "")
        for line in text.split("\n"):
            c.drawString(60, y, line)
            y -= 20
        y -= 20
        c.drawString(50, y, "💊 Prescribed Medicines:")
        y -= 25
        total_meds = 0
        for med in bill.get("medicines", []):
            subtotal = med["subtotal"]
            total_meds += subtotal
            c.drawString(60, y, f"{med['name']} (x{med['qty']}) = Rs.{subtotal}")
            y -= 20

        y -= 20
        total_bill = total_meds + doctor_price
        c.drawString(50, y, f"💰 Total Bill: Rs.{total_bill} (Doctor + Medicines)")

        c.save()
        messagebox.showinfo("Printed", f"Bill saved as {filename} ✅")

    customtkinter.CTkButton(content, text="🖨️ Print Bill", command=print_bill, fg_color="#3B82F6").pack(pady=10)

# ---------------- Page Loader ---------------- #
def load_page(page):
    for widget in content.winfo_children():
        widget.destroy()

    if page == "billing":
        load_billing_page(content)
    else:
        customtkinter.CTkLabel(content, text=page, font=("Arial", 24)).pack(pady=50)

# ---------------- Sidebar Buttons ---------------- #
menu_buttons = [
    ("🏥 Register Patient", "Register Patient Page"),
    ("📅 Book Appointment", "Appointment Booking Page"),
    ("💳 Billing", "billing"),
    ("📞 Contact Doctors", "Contact Doctor Page"),
    ("⚙️ Settings", "Receptionist Settings"),
]

for text, page in menu_buttons:
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

# ---------------- Default Page ---------------- #
load_page("Register Patient Page")

# ---------------- Run ---------------- #
app.mainloop()
