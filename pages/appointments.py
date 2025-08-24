import customtkinter
from tkinter import messagebox
from database.connection import get_db
from datetime import datetime
from tkcalendar import DateEntry  # ✅ calendar widget

class AppointmentsPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        customtkinter.CTkLabel(self, text="📅 Manage Appointments", font=("Arial", 22, "bold")).pack(pady=20)

        self.db = get_db()
        self.appointments = self.db.appointments

        # Form
        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Patient
        customtkinter.CTkLabel(form_frame, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.patient_entry = customtkinter.CTkEntry(form_frame, width=200)
        self.patient_entry.grid(row=0, column=1, pady=5)

        # Doctor
        customtkinter.CTkLabel(form_frame, text="Doctor Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.doctor_entry = customtkinter.CTkEntry(form_frame, width=200)
        self.doctor_entry.grid(row=1, column=1, pady=5)

        # ✅ Smart Date Picker
        customtkinter.CTkLabel(form_frame, text="Date:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = DateEntry(form_frame, width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=2, column=1, pady=5)

        # ✅ Smart Time Picker (dropdowns)
        customtkinter.CTkLabel(form_frame, text="Time:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.hour_option = customtkinter.CTkOptionMenu(form_frame, values=[f"{h:02d}" for h in range(0, 24)], width=70)
        self.hour_option.grid(row=3, column=1, sticky="w", padx=(0, 80), pady=5)
        self.hour_option.set("09")  # default 9 AM

        self.minute_option = customtkinter.CTkOptionMenu(form_frame, values=["00", "15", "30", "45"], width=70)
        self.minute_option.grid(row=3, column=1, sticky="e", padx=(80, 0), pady=5)
        self.minute_option.set("00")

        customtkinter.CTkButton(form_frame, text="➕ Add Appointment", command=self.add_appointment).grid(row=4, column=0, columnspan=2, pady=10)

        # Appointment list
        self.list_frame = customtkinter.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        customtkinter.CTkLabel(self.list_frame, text="All Appointments", font=("Arial", 18, "bold")).pack(pady=10)
        self.load_appointments()

    def add_appointment(self):
        patient = self.patient_entry.get().strip()
        doctor = self.doctor_entry.get().strip()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")  # ✅ from DateEntry
        time = f"{self.hour_option.get()}:{self.minute_option.get()}"

        if not (patient and doctor and date and time):
            messagebox.showwarning("Missing Fields", "Please fill all fields.")
            return

        # Insert into DB
        self.appointments.insert_one({
            "patient": patient,
            "doctor": doctor,
            "date": date,
            "time": time
        })

        messagebox.showinfo("Success", "Appointment added successfully.")
        self.clear_form()
        self.load_appointments()

    def load_appointments(self):
        for widget in self.list_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel) and "All Appointments" in widget.cget("text"):
                continue
            widget.destroy()

        for appt in self.appointments.find().sort("date", 1):
            text = f"👤 {appt['patient']} | 👨‍⚕️ {appt['doctor']} | 📅 {appt['date']} {appt['time']}"
            customtkinter.CTkLabel(self.list_frame, text=text, anchor="w", font=("Arial", 14)).pack(pady=3, padx=10, anchor="w")

    def clear_form(self):
        self.patient_entry.delete(0, "end")
        self.doctor_entry.delete(0, "end")
        self.date_entry.set_date(datetime.today())  # reset date
        self.hour_option.set("09")
        self.minute_option.set("00")
