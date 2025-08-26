# pages/pharmacy.py
import customtkinter
from tkinter import messagebox

class PharmacyPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # --- Title ---
        customtkinter.CTkLabel(
            self, 
            text="💊 Pharmacy Management",
            font=("Arial", 24, "bold"),
            text_color="#2E4C80"
        ).pack(pady=20)

        # --- Medicine Entry Form ---
        form_frame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=10)
        form_frame.pack(pady=20, padx=20, fill="x")

        customtkinter.CTkLabel(form_frame, text="Medicine Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = customtkinter.CTkEntry(form_frame, width=250)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(form_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.qty_entry = customtkinter.CTkEntry(form_frame, width=250)
        self.qty_entry.grid(row=1, column=1, padx=10, pady=10)

        customtkinter.CTkLabel(form_frame, text="Price:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.price_entry = customtkinter.CTkEntry(form_frame, width=250)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        # --- Buttons ---
        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        customtkinter.CTkButton(btn_frame, text="➕ Add", command=self.add_medicine).grid(row=0, column=0, padx=10)
        customtkinter.CTkButton(btn_frame, text="✏️ Update", command=self.update_medicine).grid(row=0, column=1, padx=10)
        customtkinter.CTkButton(btn_frame, text="❌ Delete", fg_color="#EF4444", hover_color="#DC2626", command=self.delete_medicine).grid(row=0, column=2, padx=10)

        # --- Medicine List ---
        self.listbox = customtkinter.CTkTextbox(self, width=600, height=250)
        self.listbox.pack(pady=20)

        self.medicines = {}  # simple dict storage (medicine_name → details)
        self.refresh_list()

    # ------------------- CRUD FUNCTIONS -------------------
    def add_medicine(self):
        name = self.name_entry.get().strip()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not (name and qty and price):
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return

        if name in self.medicines:
            messagebox.showerror("Error", "Medicine already exists!")
            return

        self.medicines[name] = {"qty": qty, "price": price}
        self.refresh_list()
        self.clear_fields()
        messagebox.showinfo("Success", f"{name} added!")

    def update_medicine(self):
        name = self.name_entry.get().strip()
        if name not in self.medicines:
            messagebox.showerror("Error", "Medicine not found!")
            return

        self.medicines[name] = {
            "qty": self.qty_entry.get().strip(),
            "price": self.price_entry.get().strip()
        }
        self.refresh_list()
        self.clear_fields()
        messagebox.showinfo("Updated", f"{name} updated!")

    def delete_medicine(self):
        name = self.name_entry.get().strip()
        if name in self.medicines:
            del self.medicines[name]
            self.refresh_list()
            self.clear_fields()
            messagebox.showinfo("Deleted", f"{name} removed!")
        else:
            messagebox.showerror("Error", "Medicine not found!")

    def refresh_list(self):
        self.listbox.delete("1.0", "end")
        for name, details in self.medicines.items():
            self.listbox.insert("end", f"{name} | Qty: {details['qty']} | Price: ${details['price']}\n")

    def clear_fields(self):
        self.name_entry.delete(0, "end")
        self.qty_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
