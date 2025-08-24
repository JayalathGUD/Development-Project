import customtkinter
from database.connection import get_db
from tkinter import messagebox
from bson.objectid import ObjectId
from tkinter import ttk

class NewUserPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.db = get_db()
        self.collection = self.db.users
        self.selected_id = None
        self.users = []

        self.default_font = ("Arial", 16)

        # --- Form Frame ---
        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Username
        customtkinter.CTkLabel(form_frame, text="Username:", font=self.default_font).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.username_entry = customtkinter.CTkEntry(form_frame, width=300, font=self.default_font)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        # Password
        customtkinter.CTkLabel(form_frame, text="Password:", font=self.default_font).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.password_entry = customtkinter.CTkEntry(form_frame, width=300, font=self.default_font, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        # Role
        customtkinter.CTkLabel(form_frame, text="Role:", font=self.default_font).grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.role_option = customtkinter.CTkOptionMenu(form_frame, values=["Admin", "Receptionist", "Doctor"], width=280, font=self.default_font)
        self.role_option.grid(row=2, column=1, pady=5, padx=5)
        self.role_option.set("Admin")

        # Buttons Frame
        btn_frame = customtkinter.CTkFrame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        customtkinter.CTkButton(btn_frame, text="Add", width=80, command=self.add_user, font=self.default_font).pack(side="left", padx=5)
        customtkinter.CTkButton(btn_frame, text="Update", width=80, command=self.update_user, font=self.default_font).pack(side="left", padx=5)
        customtkinter.CTkButton(btn_frame, text="Delete", width=80, command=self.delete_user, font=self.default_font).pack(side="left", padx=5)

        # --- Table Frame ---
        table_frame = customtkinter.CTkFrame(self)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        style.configure("Treeview", font=("Arial", 15), rowheight=30)

        columns = ("username", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")

        self.tree.column("username", width=300)
        self.tree.column("role", width=200)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.load_users()

    def load_users(self):
        self.users = list(self.collection.find())
        self.display_users(self.users)

    def display_users(self, user_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for user in user_list:
            self.tree.insert("", "end", iid=str(user["_id"]), values=(user["username"], user.get("role", "")))

    def clear_form(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.role_option.set("Admin")
        self.selected_id = None

    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            user_id = selected_item[0]
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                self.selected_id = str(user["_id"])
                self.username_entry.delete(0, 'end')
                self.username_entry.insert(0, user["username"])
                # Password not loaded for security reasons (you may decide what to do)
                self.password_entry.delete(0, 'end')
                self.role_option.set(user.get("role", "Admin"))

    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_option.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return

        # Check for duplicate username
        if self.collection.find_one({"username": username}):
            messagebox.showerror("Error", "Username already exists")
            return

        self.collection.insert_one({
            "username": username,
            "password": password,  # TODO: Hash password in production
            "role": role
        })
        messagebox.showinfo("Success", f"User '{username}' added")
        self.clear_form()
        self.load_users()

    def update_user(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a user to update")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_option.get()

        if not username:
            messagebox.showerror("Error", "Username is required")
            return

        # Check for duplicate username excluding current user
        existing = self.collection.find_one({"username": username, "_id": {"$ne": ObjectId(self.selected_id)}})
        if existing:
            messagebox.showerror("Error", "Username already exists")
            return

        update_data = {
            "username": username,
            "role": role
        }
        if password:
            update_data["password"] = password  # Hash in production

        self.collection.update_one({"_id": ObjectId(self.selected_id)}, {"$set": update_data})
        messagebox.showinfo("Success", f"User '{username}' updated")
        self.clear_form()
        self.load_users()

    def delete_user(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a user to delete")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?")
        if confirm:
            self.collection.delete_one({"_id": ObjectId(self.selected_id)})
            messagebox.showinfo("Deleted", "User deleted")
            self.clear_form()
            self.load_users()
