import customtkinter
from tkinter import messagebox
from database.connection import get_db
from datetime import datetime

class BillingPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        customtkinter.CTkLabel(self, text="💳 Billing Management", font=("Arial", 24, "bold")).pack(pady=20)

        # Database
        self.db = get_db()
        self.billing = self.db.billing

        # Form Frame
        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(pady=10, padx=20, fill="x")

        customtkinter.CTkLabel(form_frame, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.patient_entry = customtkinter.CTkEntry(form_frame, width=200)
        self.patient_entry.grid(row=0, column=1, pady=5)

        customtkinter.CTkLabel(form_frame, text="Service:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.service_entry = customtkinter.CTkEntry(form_frame, width=200)
        self.service_entry.grid(row=1, column=1, pady=5)

        customtkinter.CTkLabel(form_frame, text="Amount ($):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = customtkinter.CTkEntry(form_frame, width=200)
        self.amount_entry.grid(row=2, column=1, pady=5)

        customtkinter.CTkButton(form_frame, text="➕ Add Bill", command=self.add_bill).grid(row=3, column=0, columnspan=2, pady=10)

        # Bills List Frame
        self.list_frame = customtkinter.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        customtkinter.CTkLabel(self.list_frame, text="Billing Records", font=("Arial", 18, "bold")).pack(pady=10)
        self.total_label = customtkinter.CTkLabel(self.list_frame, text="Total: $0", font=("Arial", 16, "bold"))
        self.total_label.pack(pady=5)

        self.load_bills()

    def add_bill(self):
        patient = self.patient_entry.get().strip()
        service = self.service_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not (patient and service and amount):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a number.")
            return

        # Insert bill into DB
        self.billing.insert_one({
            "patient": patient,
            "service": service,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        messagebox.showinfo("Success", "Bill added successfully.")
        self.clear_form()
        self.load_bills()

    def load_bills(self):
        # Clear old widgets (but keep title/total)
        for widget in self.list_frame.winfo_children():
            if widget not in (self.total_label,):
                widget.destroy()

        total = 0
        for bill in self.billing.find().sort("date", -1):
            text = f"👤 {bill['patient']} | 🛠 {bill['service']} | 💵 ${bill['amount']} | 📅 {bill['date']}"
            customtkinter.CTkLabel(self.list_frame, text=text, anchor="w", font=("Arial", 14)).pack(pady=3, padx=10, anchor="w")
            total += bill["amount"]

        self.total_label.configure(text=f"Total: ${total:.2f}")

    def clear_form(self):
        self.patient_entry.delete(0, "end")
        self.service_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
