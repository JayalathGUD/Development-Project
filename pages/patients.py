import customtkinter
from database.connection import get_db
from tkinter import messagebox, filedialog
from bson.objectid import ObjectId
import os, shutil, csv
from tkinter import ttk
from PIL import Image, ImageTk


class PatientsPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.db = get_db()
        self.collection = self.db.patients
        self.selected_id = None
        self.patients = []
        self.photo_path = None

        self.default_font = ("Arial", 16)

        # Search Bar
        search_frame = customtkinter.CTkFrame(self)
        search_frame.pack(pady=10, padx=20, fill="x")

        customtkinter.CTkLabel(search_frame, text="Search: ", font=self.default_font).pack(side="left", padx=(10, 0))
        self.search_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Search by name", width=400, font=self.default_font)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_patients)

        export_btn = customtkinter.CTkButton(search_frame, text="Export CSV", command=self.export_to_csv, font=self.default_font)
        export_btn.pack(side="right", padx=10)

        # Form
        top_frame = customtkinter.CTkFrame(self)
        top_frame.pack(pady=5, padx=20, fill="x")

        # Photo Frame
        photo_frame = customtkinter.CTkFrame(top_frame)
        photo_frame.pack(side="left", padx=20)

        self.image_label = customtkinter.CTkLabel(photo_frame, text="No Image", width=150, height=150)
        self.image_label.pack(pady=5)

        upload_btn = customtkinter.CTkButton(photo_frame, text="Upload Photo", command=self.upload_photo, font=self.default_font)
        upload_btn.pack(pady=5)

        form_frame = customtkinter.CTkFrame(top_frame)
        form_frame.pack(side="left", padx=20)

        self.name_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Patient Name", width=300, font=self.default_font)
        self.name_entry.pack(pady=5)

        self.age_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Age", width=300, font=self.default_font)
        self.age_entry.pack(pady=5)

        self.gender_entry = customtkinter.CTkComboBox(form_frame, values=["Male", "Female", "Other"], width=300, font=self.default_font)
        self.gender_entry.set("Male")
        self.gender_entry.pack(pady=5)

        self.dob_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Date of Birth (YYYY-MM-DD)", width=300, font=self.default_font)
        self.dob_entry.pack(pady=5)

        self.email_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Email", width=300, font=self.default_font)
        self.email_entry.pack(pady=5)

        self.contact_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Contact", width=300, font=self.default_font)
        self.contact_entry.pack(pady=5)

        self.emergency_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Emergency Contact", width=300, font=self.default_font)
        self.emergency_entry.pack(pady=5)

        self.blood_entry = customtkinter.CTkComboBox(form_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=300, font=self.default_font)
        self.blood_entry.set("O+")
        self.blood_entry.pack(pady=5)

        self.address_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Address", width=300, font=self.default_font)
        self.address_entry.pack(pady=5)

        button_frame = customtkinter.CTkFrame(form_frame)
        button_frame.pack(pady=10)

        customtkinter.CTkButton(button_frame, text="Add", width=80, command=self.add_patient, font=self.default_font).pack(side="left", padx=5)
        customtkinter.CTkButton(button_frame, text="Update", width=80, command=self.update_patient, font=self.default_font).pack(side="left", padx=5)
        customtkinter.CTkButton(button_frame, text="Delete", width=80, command=self.delete_patient, font=self.default_font).pack(side="left", padx=5)

        # Table View
        table_frame = customtkinter.CTkFrame(self)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        style.configure("Treeview", font=("Arial", 15), rowheight=30)

        columns = ("name", "age", "gender", "dob", "contact", "email", "blood_group", "emergency_contact", "address")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=140)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.load_patients()

    def load_patients(self):
        self.patients = list(self.collection.find())
        self.display_patients(self.patients)

    def display_patients(self, patient_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for patient in patient_list:
            self.tree.insert("", "end", iid=str(patient["_id"]), values=(
                patient.get("name", ""),
                patient.get("age", ""),
                patient.get("gender", ""),
                patient.get("dob", ""),
                patient.get("contact", ""),
                patient.get("email", ""),
                patient.get("blood_group", ""),
                patient.get("emergency_contact", ""),
                patient.get("address", "")
            ))

    def filter_patients(self, event=None):
        keyword = self.search_entry.get().strip().lower()
        filtered = [
            patient for patient in self.patients
            if keyword in patient['name'].lower()
        ]
        self.display_patients(filtered)

    def add_patient(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        contact = self.contact_entry.get()

        if not name or not age or not contact:
            messagebox.showerror("Error", "Name, Age, and Contact are required")
            return

        self.collection.insert_one({
            "name": name,
            "age": age,
            "gender": self.gender_entry.get(),
            "dob": self.dob_entry.get(),
            "contact": contact,
            "email": self.email_entry.get(),
            "emergency_contact": self.emergency_entry.get(),
            "blood_group": self.blood_entry.get(),
            "address": self.address_entry.get(),
            "photo_path": self.photo_path or ""
        })

        messagebox.showinfo("Success", "Patient added")
        self.clear_form()
        self.load_patients()

    def update_patient(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a patient to update")
            return

        data = {
            "name": self.name_entry.get(),
            "age": self.age_entry.get(),
            "gender": self.gender_entry.get(),
            "dob": self.dob_entry.get(),
            "contact": self.contact_entry.get(),
            "email": self.email_entry.get(),
            "emergency_contact": self.emergency_entry.get(),
            "blood_group": self.blood_entry.get(),
            "address": self.address_entry.get()
        }

        if self.photo_path:
            data["photo_path"] = self.photo_path

        self.collection.update_one({"_id": ObjectId(self.selected_id)}, {"$set": data})
        messagebox.showinfo("Updated", "Patient updated")
        self.clear_form()
        self.load_patients()

    def delete_patient(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a patient to delete")
            return

        self.collection.delete_one({"_id": ObjectId(self.selected_id)})
        messagebox.showinfo("Deleted", "Patient deleted")
        self.clear_form()
        self.load_patients()

    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
        self.gender_entry.set("Male")
        self.dob_entry.delete(0, 'end')
        self.contact_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.emergency_entry.delete(0, 'end')
        self.blood_entry.set("O+")
        self.address_entry.delete(0, 'end')
        self.selected_id = None
        self.photo_path = None
        self.image_label.configure(text="No Image", image="")

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            patient_id = selected_item[0]
            patient = self.collection.find_one({"_id": ObjectId(patient_id)})
            if patient:
                self.selected_id = str(patient["_id"])
                self.name_entry.delete(0, 'end'); self.name_entry.insert(0, patient.get("name", ""))
                self.age_entry.delete(0, 'end'); self.age_entry.insert(0, patient.get("age", ""))
                self.gender_entry.set(patient.get("gender", "Male"))
                self.dob_entry.delete(0, 'end'); self.dob_entry.insert(0, patient.get("dob", ""))
                self.contact_entry.delete(0, 'end'); self.contact_entry.insert(0, patient.get("contact", ""))
                self.email_entry.delete(0, 'end'); self.email_entry.insert(0, patient.get("email", ""))
                self.emergency_entry.delete(0, 'end'); self.emergency_entry.insert(0, patient.get("emergency_contact", ""))
                self.blood_entry.set(patient.get("blood_group", "O+"))
                self.address_entry.delete(0, 'end'); self.address_entry.insert(0, patient.get("address", ""))

                self.photo_path = patient.get("photo_path", "")
                if self.photo_path and os.path.exists(self.photo_path):
                    self.show_photo(self.photo_path)
                else:
                    self.image_label.configure(text="No Image", image="")

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            filename = os.path.basename(file_path)
            dest_path = f"assets/images/patients/{filename}"
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(file_path, dest_path)
            self.photo_path = dest_path
            self.show_photo(dest_path)

    def show_photo(self, path):
        try:
            img = Image.open(path).resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk, text="")
            self.image_label.image = img_tk
        except:
            self.image_label.configure(text="Invalid Image", image="")

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Name", "Age", "Gender", "DOB", "Contact", "Email", "Blood Group", "Emergency Contact", "Address"])
                    for patient in self.patients:
                        writer.writerow([
                            patient.get("name", ""),
                            patient.get("age", ""),
                            patient.get("gender", ""),
                            patient.get("dob", ""),
                            patient.get("contact", ""),
                            patient.get("email", ""),
                            patient.get("blood_group", ""),
                            patient.get("emergency_contact", ""),
                            patient.get("address", "")
                        ])
                messagebox.showinfo("Exported", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
