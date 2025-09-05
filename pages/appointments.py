import customtkinter
from tkinter import messagebox
from database.connection import get_db
from datetime import datetime
from tkcalendar import DateEntry  # ✅ calendar widget


class AppointmentsPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#FFFFFF")

        self.db = get_db()
        self.appointments = self.db.appointments
        self.doctors_collection = self.db.doctors

        # Main container
        main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        customtkinter.CTkLabel(
            header_frame,
            text="📅 Appointment Management",
            font=("Arial", 24, "bold"),
            text_color="#2E4C80"
        ).pack(side="left")

        # Two-column layout
        content_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Left column - Form
        form_container = customtkinter.CTkFrame(content_frame, width=400, fg_color="#F8FAFC", corner_radius=12)
        form_container.pack(side="left", fill="y", padx=(0, 20))
        form_container.pack_propagate(False)

        customtkinter.CTkLabel(
            form_container,
            text="Schedule New Appointment",
            font=("Arial", 18, "bold"),
            text_color="#2E4C80"
        ).pack(pady=20)

        # Form frame
        form_frame = customtkinter.CTkFrame(form_container, fg_color="transparent")
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Patient
        customtkinter.CTkLabel(
            form_frame,
            text="Patient Name:",
            font=("Arial", 14),
            text_color="#374151"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.patient_entry = customtkinter.CTkEntry(
            form_frame,
            width=200,
            height=40,
            corner_radius=8,
            border_color="#D1D5DB",
            fg_color="#FFFFFF",
            text_color="#1F2937"
        )
        self.patient_entry.grid(row=0, column=1, pady=10, padx=(0, 10))

        # Doctor Dropdown
        customtkinter.CTkLabel(
            form_frame,
            text="Doctor Name:",
            font=("Arial", 14),
            text_color="#374151"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        doctors = [doc["name"] for doc in self.doctors_collection.find()]
        if not doctors:
            doctors = ["No Doctors Available"]

        self.doctor_option = customtkinter.CTkOptionMenu(
            form_frame,
            values=doctors,
            width=200,
            height=40,
            fg_color="#FFFFFF",
            button_color="#3B82F6",
            text_color="#1F2937",
            dropdown_text_color="#1F2937",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#EFF6FF"
        )
        self.doctor_option.grid(row=1, column=1, pady=10, padx=(0, 10))
        self.doctor_option.set(doctors[0])

        # Date Picker
        customtkinter.CTkLabel(
            form_frame,
            text="Date:",
            font=("Arial", 14),
            text_color="#374151"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.date_entry = DateEntry(
            form_frame,
            width=18,
            background="#3B82F6",
            foreground="white",
            borderwidth=1,
            date_pattern="yyyy-mm-dd"
        )
        self.date_entry.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="w")

        # Time Picker
        customtkinter.CTkLabel(
            form_frame,
            text="Time:",
            font=("Arial", 14),
            text_color="#374151"
        ).grid(row=3, column=0, padx=10, pady=10, sticky="w")

        time_frame = customtkinter.CTkFrame(form_frame, fg_color="transparent")
        time_frame.grid(row=3, column=1, pady=10, sticky="w")

        self.hour_option = customtkinter.CTkOptionMenu(
            time_frame,
            values=[f"{h:02d}" for h in range(0, 24)],
            width=70,
            height=35,
            fg_color="#FFFFFF",
            button_color="#3B82F6",
            text_color="#1F2937",
            dropdown_text_color="#1F2937",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#EFF6FF"
        )
        self.hour_option.pack(side="left", padx=(0, 5))
        self.hour_option.set("09")

        self.minute_option = customtkinter.CTkOptionMenu(
            time_frame,
            values=["00", "15", "30", "45"],
            width=70,
            height=35,
            fg_color="#FFFFFF",
            button_color="#3B82F6",
            text_color="#1F2937",
            dropdown_text_color="#1F2937",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#EFF6FF"
        )
        self.minute_option.pack(side="left", padx=(5, 0))
        self.minute_option.set("00")

        # Add Appointment Button
        customtkinter.CTkButton(
            form_frame,
            text="➕ Add Appointment",
            command=self.add_appointment,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white"
        ).grid(row=4, column=0, columnspan=2, pady=20)

        # Right column - Appointment list
        list_container = customtkinter.CTkFrame(content_frame, fg_color="#F8FAFC", corner_radius=12)
        list_container.pack(side="right", fill="both", expand=True)

        customtkinter.CTkLabel(
            list_container,
            text="Scheduled Appointments",
            font=("Arial", 18, "bold"),
            text_color="#2E4C80"
        ).pack(pady=20)

        self.list_frame = customtkinter.CTkScrollableFrame(list_container, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_appointments()

    def add_appointment(self):
        patient = self.patient_entry.get().strip()
        doctor = self.doctor_option.get().strip()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        time = f"{self.hour_option.get()}:{self.minute_option.get()}"

        if not (patient and doctor and date and time):
            messagebox.showwarning("Missing Fields", "Please fill all fields.")
            return

        # 🔍 Prevent double-booking for same doctor, date & time
        existing = self.appointments.find_one({
            "doctor": doctor,
            "date": date,
            "time": time
        })
        if existing:
            messagebox.showerror(
                "Conflict",
                f"Dr. {doctor} already has an appointment at {date} {time}."
            )
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
            widget.destroy()

        appointments = list(self.appointments.find().sort("date", 1))

        if not appointments:
            customtkinter.CTkLabel(
                self.list_frame,
                text="No appointments scheduled",
                font=("Arial", 14),
                text_color="#6B7280"
            ).pack(pady=20)
            return

        for appt in appointments:
            appt_frame = customtkinter.CTkFrame(
                self.list_frame,
                fg_color="#FFFFFF",
                border_color="#E5E7EB",
                border_width=1,
                corner_radius=8
            )
            appt_frame.pack(fill="x", pady=5, padx=5)

            text = f"👤 {appt['patient']} | 👨‍⚕️ {appt['doctor']} | 📅 {appt['date']} {appt['time']}"

            customtkinter.CTkLabel(
                appt_frame,
                text=text,
                anchor="w",
                font=("Arial", 14),
                text_color="#374151"
            ).pack(pady=10, padx=15, anchor="w")

    def clear_form(self):
        self.patient_entry.delete(0, "end")

        # reload doctors in case new doctors were added
        doctors = [doc["name"] for doc in self.doctors_collection.find()]
        if doctors:
            self.doctor_option.configure(values=doctors)
            self.doctor_option.set(doctors[0])
        else:
            self.doctor_option.configure(values=["No Doctors Available"])
            self.doctor_option.set("No Doctors Available")

        self.date_entry.set_date(datetime.today())
        self.hour_option.set("09")
        self.minute_option.set("00")
