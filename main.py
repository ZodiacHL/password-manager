import tkinter as tk
from tkinter import messagebox
import json
import os
from crypto_utils import generate_key, encrypt_data, decrypt_data

DATA_FILE = "data.json"

# --- Step 1: Ask for master password ---
def verify_master_password():
    def submit_password():
        password = entry.get()
        key = generate_key(password)
        root.destroy()
        build_main_gui(key)

    root = tk.Tk()
    root.title("Enter Master Password")

    tk.Label(root, text="Enter Master Password:").pack(pady=10)
    entry = tk.Entry(root, show="*", width=30)
    entry.pack(pady=5)
    tk.Button(root, text="Submit", command=submit_password).pack(pady=10)

    root.mainloop()

# --- Step 2: Build main GUI ---
def build_main_gui(key):
    def save_credential():
        site = entry_site.get()
        username = entry_user.get()
        password = entry_pass.get()

        if not site or not username or not password:
            messagebox.showwarning("Missing Fields", "Please fill out all fields.")
            return

        data = {
            "site": site,
            "username": username,
            "password": password
        }

        encrypted = encrypt_data(json.dumps(data), key)

        with open(DATA_FILE, "a") as f:
            f.write(encrypted + "\n")

        messagebox.showinfo("Saved", f"Credentials for {site} saved.")
        entry_site.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_pass.delete(0, tk.END)

    app = tk.Tk()
    app.title("Password Manager")

    tk.Label(app, text="Website:").grid(row=0, column=0)
    tk.Label(app, text="Username:").grid(row=1, column=0)
    tk.Label(app, text="Password:").grid(row=2, column=0)

    entry_site = tk.Entry(app)
    entry_user = tk.Entry(app)
    entry_pass = tk.Entry(app, show="*")

    entry_site.grid(row=0, column=1)
    entry_user.grid(row=1, column=1)
    entry_pass.grid(row=2, column=1)

    tk.Button(app, text="Save", command=save_credential).grid(row=3, column=0, columnspan=2, pady=10)

    app.mainloop()

# --- Start app ---
if __name__ == "__main__":
    verify_master_password()

