import customtkinter

class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        customtkinter.CTkLabel(self, text="Settings", font=("Arial", 24)).pack(pady=20)

        dark_btn = customtkinter.CTkButton(self, text="Toggle Dark/Light Mode", command=self.toggle_theme)
        dark_btn.pack(pady=20)

    def toggle_theme(self):
        current = customtkinter.get_appearance_mode()
        new_mode = "light" if current == "dark" else "dark"
        customtkinter.set_appearance_mode(new_mode)
