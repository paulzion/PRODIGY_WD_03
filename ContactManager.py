import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONTACTS_FILE = 'contacts.json'

class ContactManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Manager")
        self.geometry("400x300")
        
        self.contacts = self.load_contacts()
        
        self.create_widgets()
        
    def create_widgets(self):
        self.label_name = ttk.Label(self, text="Name:")
        self.label_name.grid(column=0, row=0, padx=10, pady=5)
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(column=1, row=0, padx=10, pady=5)

        self.label_phone = ttk.Label(self, text="Phone:")
        self.label_phone.grid(column=0, row=1, padx=10, pady=5)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.grid(column=1, row=1, padx=10, pady=5)

        self.label_email = ttk.Label(self, text="Email:")
        self.label_email.grid(column=0, row=2, padx=10, pady=5)
        self.entry_email = ttk.Entry(self)
        self.entry_email.grid(column=1, row=2, padx=10, pady=5)

        self.button_add = ttk.Button(self, text="Add Contact", command=self.add_contact)
        self.button_add.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

        self.contacts_list = ttk.Treeview(self, columns=("Name", "Phone", "Email"), show='headings')
        self.contacts_list.heading("Name", text="Name")
        self.contacts_list.heading("Phone", text="Phone")
        self.contacts_list.heading("Email", text="Email")
        self.contacts_list.grid(column=0, row=4, padx=10, pady=10, columnspan=2)
        self.contacts_list.bind('<Double-1>', self.on_edit)

        self.button_delete = ttk.Button(self, text="Delete Selected", command=self.delete_contact)
        self.button_delete.grid(column=0, row=5, padx=10, pady=10, columnspan=2)

        self.load_contacts_into_list()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_contacts(self):
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(self.contacts, f, indent=4)

    def load_contacts_into_list(self):
        for contact in self.contacts:
            self.contacts_list.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

    def add_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        if name and phone and email:
            contact = {"name": name, "phone": phone, "email": email}
            self.contacts.append(contact)
            self.save_contacts()
            self.contacts_list.insert("", tk.END, values=(name, phone, email))
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")

    def on_edit(self, event):
        selected_item = self.contacts_list.selection()[0]
        selected_contact = self.contacts_list.item(selected_item, "values")
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, selected_contact[0])
        self.entry_phone.delete(0, tk.END)
        self.entry_phone.insert(0, selected_contact[1])
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, selected_contact[2])

        self.button_add.config(text="Update Contact", command=lambda: self.update_contact(selected_item))

    def update_contact(self, item_id):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        if name and phone and email:
            updated_contact = {"name": name, "phone": phone, "email": email}
            self.contacts_list.item(item_id, values=(name, phone, email))
            self.contacts[int(item_id)] = updated_contact
            self.save_contacts()
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.button_add.config(text="Add Contact", command=self.add_contact)
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")

    def delete_contact(self):
        selected_items = self.contacts_list.selection()
        if selected_items:
            for selected_item in selected_items:
                self.contacts_list.delete(selected_item)
                del self.contacts[int(selected_item)]
            self.save_contacts()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete")

if __name__ == "__main__":
    app = ContactManager()
    app.mainloop()
