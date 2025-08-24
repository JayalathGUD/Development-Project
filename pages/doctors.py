import customtkinter
from database.connection import get_db
from tkinter import messagebox, filedialog
from bson.objectid import ObjectId
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shutil

class DoctorsPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.db = get_db()
        self.collection = self.db.doctors
        self.selected_id = None
        self.doctors = []
        self.photo_path = None

        self.default_font = ("Arial", 16)

        # Search Bar
        search_frame = customtkinter.CTkFrame(self)
        search_frame.pack(pady=10, padx=20, fill="x")

        customtkinter.CTkLabel(search_frame, text="Search: ", font=self.default_font).pack(side="left", padx=(10, 0))
        self.search_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Search by name or specialization", width=400, font=self.default_font)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_doctors)

        # Form
        top_frame = customtkinter.CTkFrame(self)
        top_frame.pack(pady=5, padx=20, fill="x")

        # --- Photo Upload and Preview ---
        photo_frame = customtkinter.CTkFrame(top_frame)
        photo_frame.pack(side="left", padx=20)

        self.image_label = customtkinter.CTkLabel(photo_frame, text="No Image", width=150, height=150)
        self.image_label.pack(pady=5)

        upload_btn = customtkinter.CTkButton(photo_frame, text="Upload Photo", command=self.upload_photo, font=self.default_font)
        upload_btn.pack(pady=5)

        form_frame = customtkinter.CTkFrame(top_frame)
        form_frame.pack(side="left", padx=20)

        self.name_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Doctor Name", width=300, font=self.default_font)
        self.name_entry.pack(pady=5)

        self.specialization_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Specialization", width=300, font=self.default_font)
        self.specialization_entry.pack(pady=5)

        self.contact_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Contact", width=300, font=self.default_font)
        self.contact_entry.pack(pady=5)

        self.price_entry = customtkinter.CTkEntry(form_frame, placeholder_text="Consultation Price", width=300, font=self.default_font)
        self.price_entry.pack(pady=5)

        button_frame = customtkinter.CTkFrame(form_frame)
        button_frame.pack(pady=10)

        customtkinter.CTkButton(button_frame, text="Add", width=80, command=self.add_doctor, font=self.default_font).pack(side="left", padx=5)
        customtkinter.CTkButton(button_frame, text="Update", width=80, command=self.update_doctor, font=self.default_font).pack(side="left", padx=5)
        customtkinter.CTkButton(button_frame, text="Delete", width=80, command=self.delete_doctor, font=self.default_font).pack(side="left", padx=5)

        # Table View
        table_frame = customtkinter.CTkFrame(self)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        style.configure("Treeview", font=("Arial", 15), rowheight=30)

        columns = ("name", "specialization", "contact", "price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("name", text="Name")
        self.tree.heading("specialization", text="Specialization")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("price", text="Price")

        self.tree.column("name", width=200)
        self.tree.column("specialization", width=180)
        self.tree.column("contact", width=140)
        self.tree.column("price", width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.load_doctors()

    def load_doctors(self):
        self.doctors = list(self.collection.find())
        self.display_doctors(self.doctors)

    def display_doctors(self, doctor_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for doc in doctor_list:
            self.tree.insert("", "end", iid=str(doc["_id"]), values=(doc["name"], doc["specialization"], doc["contact"], doc.get("price", "")))

    def filter_doctors(self, event=None):
        keyword = self.search_entry.get().strip().lower()
        filtered = [
            doc for doc in self.doctors
            if keyword in doc['name'].lower()
            or keyword in doc['specialization'].lower()
            or keyword in doc['contact'].lower()
        ]
        self.display_doctors(filtered)

    def add_doctor(self):
        name = self.name_entry.get()
        spec = self.specialization_entry.get()
        contact = self.contact_entry.get()
        price = self.price_entry.get()

        if not name or not spec or not contact:
            messagebox.showerror("Error", "All fields required")
            return

        self.collection.insert_one({
            "name": name,
            "specialization": spec,
            "contact": contact,
            "price": price,
            "photo_path": self.photo_path or ""
        })

        messagebox.showinfo("Success", "Doctor added")
        self.clear_form()
        self.load_doctors()

    def update_doctor(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a doctor to update")
            return

        data = {
            "name": self.name_entry.get(),
            "specialization": self.specialization_entry.get(),
            "contact": self.contact_entry.get(),
            "price": self.price_entry.get()
        }

        if self.photo_path:
            data["photo_path"] = self.photo_path

        self.collection.update_one({"_id": ObjectId(self.selected_id)}, {"$set": data})
        messagebox.showinfo("Updated", "Doctor updated")
        self.clear_form()
        self.load_doctors()

    def delete_doctor(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a doctor to delete")
            return

        self.collection.delete_one({"_id": ObjectId(self.selected_id)})
        messagebox.showinfo("Deleted", "Doctor deleted")
        self.clear_form()
        self.load_doctors()

    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.specialization_entry.delete(0, 'end')
        self.contact_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.selected_id = None
        self.photo_path = None
        self.image_label.configure(text="No Image", image="")

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            doc_id = selected_item[0]
            doc = self.collection.find_one({"_id": ObjectId(doc_id)})
            if doc:
                self.selected_id = str(doc["_id"])
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, doc["name"])
                self.specialization_entry.delete(0, 'end')
                self.specialization_entry.insert(0, doc["specialization"])
                self.contact_entry.delete(0, 'end')
                self.contact_entry.insert(0, doc["contact"])
                self.price_entry.delete(0, 'end')
                self.price_entry.insert(0, doc.get("price", ""))
                self.photo_path = doc.get("photo_path", "")
                if self.photo_path and os.path.exists(self.photo_path):
                    self.show_photo(self.photo_path)
                else:
                    self.image_label.configure(text="No Image", image="")

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            filename = os.path.basename(file_path)
            dest_path = f"assets/images/doctors/{filename}"
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
