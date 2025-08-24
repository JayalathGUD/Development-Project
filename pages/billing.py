import customtkinter

class BillingPage(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        customtkinter.CTkLabel(self, text="Billing", font=("Arial", 24)).pack(pady=20)

        content = customtkinter.CTkTextbox(self, width=600, height=300)
        content.insert("end", "Billing Summary:\n\n- Patient: John Doe\n  Amount: $200\n\n- Patient: Jane Smith\n  Amount: $350")
        content.pack()
