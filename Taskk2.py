import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

# Database setup
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')

conn.commit()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Authentication
def authenticate(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    return c.fetchone()

# GUI Setup
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("300x350")
        self.username = None
        
        # Login Screen
        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = authenticate(username, password)
        if user:
            self.username = username
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.product_listbox = tk.Listbox(self.root)
        self.product_listbox = tk.Listbox(self.root, width=50, height=20)
        self.product_listbox.grid(row=0, column=0, columnspan=3)

        self.show_products_button = tk.Button(self.root, text="Show All Products", command=self.show_all_products)
        self.show_products_button.grid(row=1, column=0)

        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product_screen)
        self.add_product_button.grid(row=1, column=1)

        self.delete_product_button = tk.Button(self.root, text="Delete Product", command=self.delete_product)
        self.delete_product_button.grid(row=1, column=2)

    def show_all_products(self):
        self.product_listbox.delete(0, tk.END)
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        for product in products:
            self.product_listbox.insert(tk.END, f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: {product[3]}")

    def add_product_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.name_label = tk.Label(self.root, text="Product Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(self.root, text="Quantity")
        self.quantity_label.grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=1, column=1)

        self.price_label = tk.Label(self.root, text="Price")
        self.price_label.grid(row=2, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.back_button = tk.Button(self.root, text="Back", command=self.main_screen)
        self.back_button.grid(row=4, column=0, columnspan=2)

    def add_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number")
            return
        
        c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        self.main_screen()

    def delete_product(self):
        selected_product = self.product_listbox.get(tk.ACTIVE)
        if not selected_product:
            messagebox.showerror("Error", "No product selected")
            return

        product_id = int(selected_product.split(",")[0].split(":")[1].strip())
        c.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
        self.show_all_products()

root = tk.Tk()
app = InventoryApp(root)
root.mainloop()

conn.close()
