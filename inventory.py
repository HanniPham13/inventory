import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class InventoryApp:
    def __init__(self, root, inventory):
        self.root = root
        self.inventory = inventory

        # Set window properties
        self.root.title("Inventory Management")
        self.root.geometry("800x500")
        self.root.config(bg="#f4f4f9")  # Set background color for modern feel

        # Category Label and Dropdown
        self.category_label = tk.Label(self.root, text="Select Category:", font=("Arial", 12, "bold"), bg="#f4f4f9")
        self.category_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var, state="readonly", font=("Arial", 12))
        self.category_dropdown['values'] = list(self.inventory.get_categories())  # Dropdown options for categories
        self.category_dropdown.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_item_dropdown)

        # Search Label and Entry
        self.search_label = tk.Label(self.root, text="Search Item:", font=("Arial", 12, "bold"), bg="#f4f4f9")
        self.search_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.search_entry = tk.Entry(self.root, font=("Arial", 12))
        self.search_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.refresh_inventory)

        # Item Name Label and Dropdown
        self.item_label = tk.Label(self.root, text="Enter Item Name:", font=("Arial", 12, "bold"), bg="#f4f4f9")
        self.item_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.item_name = ttk.Combobox(self.root, state="readonly", font=("Arial", 12))
        self.item_name.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        # Quantity Label and Entry
        self.quantity_label = tk.Label(self.root, text="Quantity:", font=("Arial", 12, "bold"), bg="#f4f4f9")
        self.quantity_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.quantity = tk.Entry(self.root, font=("Arial", 12))
        self.quantity.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        # Price Label and Entry
        self.price_label = tk.Label(self.root, text="Price (₱):", font=("Arial", 12, "bold"), bg="#f4f4f9")
        self.price_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.price = tk.Entry(self.root, font=("Arial", 12))
        self.price.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        # Buttons for actions
        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", width=20)
        self.add_button.grid(row=5, column=0, padx=20, pady=10)

        self.remove_button = tk.Button(self.root, text="Remove Item", command=self.remove_item, font=("Arial", 12, "bold"), bg="#FF5722", fg="white", relief="flat", width=20)
        self.remove_button.grid(row=5, column=1, padx=20, pady=10)

        self.update_button = tk.Button(self.root, text="Update Item", command=self.update_item, font=("Arial", 12, "bold"), bg="#FFC107", fg="white", relief="flat", width=20)
        self.update_button.grid(row=6, column=0, padx=20, pady=10)

        self.remove_all_button = tk.Button(self.root, text="Remove All Items", command=self.remove_all, font=("Arial", 12, "bold"), bg="#9E9E9E", fg="white", relief="flat", width=20)
        self.remove_all_button.grid(row=6, column=1, padx=20, pady=10)
        
        # Import and Export Buttons
        self.import_button = tk.Button(self.root, text="Import from JSON", command=self.import_from_json, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", width=20)
        self.import_button.grid(row=7, column=0, padx=20, pady=10)

        self.export_button = tk.Button(self.root, text="Export to JSON", command=self.export_to_json, font=("Arial", 12, "bold"), bg="#FF9800", fg="white", relief="flat", width=20)
        self.export_button.grid(row=7, column=1, padx=20, pady=10)

        # Create a frame for the item list with a scrollable canvas
        self.item_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.item_frame.grid(row=0, column=2, rowspan=7, padx=20, pady=10, sticky="nsew")

        self.canvas = tk.Canvas(self.item_frame, bg="#f4f4f9")
        self.scrollbar = tk.Scrollbar(self.item_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas_frame = tk.Frame(self.canvas, bg="#f4f4f9")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.canvas_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Refresh inventory view
        self.refresh_inventory()

    def refresh_inventory(self, event=None):
        """Refresh the inventory display based on search input."""
        for widget in self.canvas_frame.winfo_children():
            widget.grid_forget()

        row = 0
        inventory = self.inventory.get_inventory()
        search_query = self.search_entry.get().lower()

        for category, items in inventory.items():
            if self.category_var.get() == category or not self.category_var.get():
                category_label = tk.Label(self.canvas_frame, text=category, font=("Arial", 14, "bold"), bg="#f4f4f9", fg="#4CAF50")
                category_label.grid(row=row, column=0, columnspan=2, pady=5, sticky="w")
                row += 1
                for item in items:
                    if search_query in item['name'].lower():
                        item_label = tk.Label(self.canvas_frame, text=f"{item['name']} - Quantity: {item['quantity']} - Price: ₱{item['price']}", font=("Arial", 12), bg="#f4f4f9")
                        item_label.grid(row=row, column=0, columnspan=2, pady=5, sticky="w")
                        row += 1

    def add_item(self):
        """Add an item to the inventory."""
        category = self.category_var.get()
        item_name = self.item_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if item_name and quantity.isdigit() and price.replace(",", "").replace("₱", "").isdigit():
            price = float(price.replace(",", "").replace("₱", ""))
            self.inventory.add_item(category, item_name, int(quantity), price)
            self.refresh_inventory()
        else:
            messagebox.showerror("Invalid Input", "Please enter valid details.")

    def remove_item(self):
        """Remove an item from the inventory."""
        category = self.category_var.get()
        item_name = self.item_name.get()
        quantity = self.quantity.get()

        if item_name and quantity.isdigit():
            self.inventory.remove_item(category, item_name, int(quantity))
            self.refresh_inventory()
        else:
            messagebox.showerror("Invalid Input", "Please enter valid details.")

    def update_item(self):
        """Update item details in the inventory."""
        category = self.category_var.get()
        item_name = self.item_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if item_name and quantity.isdigit() and price.replace(",", "").replace("₱", "").isdigit():
            price = float(price.replace(",", "").replace("₱", ""))
            self.inventory.update_item(category, item_name, int(quantity), price)
            self.refresh_inventory()
        else:
            messagebox.showerror("Invalid Input", "Please enter valid details.")

    def remove_all(self):
        """Remove all items in the inventory."""
        self.inventory.remove_all()
        self.refresh_inventory()

    def update_item_dropdown(self, event):
        """Update item dropdown based on selected category."""
        category = self.category_var.get()
        items = self.inventory.get_items_by_category(category)
        self.item_name['values'] = [item['name'] for item in items]  # Update the item dropdown
        self.item_name.set('')  # Clear item dropdown selection
        self.refresh_inventory()  # Refresh inventory to show items of the selected category
        
    def import_from_json(self):
        """Import inventory data from a JSON file."""
        try:
            file_path = tk.filedialog.askopenfilename(
                defaultextension=".json", filetypes=[("JSON files", "*.json")]
            )
            if file_path:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    self.inventory.data = data
                    self.refresh_inventory()
                    messagebox.showinfo("Import Successful", "Inventory data imported successfully.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def export_to_json(self):
        """Export inventory data to a JSON file."""
        try:
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".json", filetypes=[("JSON files", "*.json")]
            )
            if file_path:
                with open(file_path, "w") as f:
                    json.dump(self.inventory.data, f, indent=4)
                    messagebox.showinfo("Export Successful", "Inventory data exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


class Inventory:
    def __init__(self):
        self.data = {
            "Technology": [
                {"name": "Laptop", "quantity": 10, "price": 45000},
                {"name": "Smartphone", "quantity": 50, "price": 20000},
                {"name": "Wireless Headphones", "quantity": 30, "price": 5000},
                {"name": "Smartwatch", "quantity": 15, "price": 12000},
                {"name": "Tablet", "quantity": 25, "price": 15000},
                {"name": "Desktop Computer", "quantity": 5, "price": 35000},
                {"name": "Bluetooth Speaker", "quantity": 20, "price": 3000},
                {"name": "Power Bank", "quantity": 40, "price": 1500},
                {"name": "Camera", "quantity": 10, "price": 25000},
                {"name": "Smart TV", "quantity": 8, "price": 35000}
            ],
            "Groceries": [
                {"name": "Rice", "quantity": 100, "price": 50},
                {"name": "Sugar", "quantity": 200, "price": 35},
                {"name": "Flour", "quantity": 150, "price": 40},
                {"name": "Cooking Oil", "quantity": 80, "price": 100},
                {"name": "Salt", "quantity": 120, "price": 20},
                {"name": "Pepper", "quantity": 180, "price": 25},
                {"name": "Onions", "quantity": 120, "price": 40},
                {"name": "Garlic", "quantity": 200, "price": 60}
            ],
            "Canned Goods": [
                {"name": "Canned Beans", "quantity": 150, "price": 30},
                {"name": "Canned Corn", "quantity": 120, "price": 35},
                {"name": "Canned Soup", "quantity": 100, "price": 45},
                {"name": "Canned Peas", "quantity": 80, "price": 25},
                {"name": "Canned Pineapple", "quantity": 90, "price": 55},
                {"name": "Canned Mushroom", "quantity": 70, "price": 60},
                {"name": "Canned Chilli", "quantity": 60, "price": 50},
                {"name": "Canned Tomato", "quantity": 150, "price": 30},
                {"name": "Canned Vegetable", "quantity": 110, "price": 40}
            ],
            "Household Items": [
                {"name": "Dishwashing Liquid", "quantity": 100, "price": 50},
                {"name": "Laundry Detergent", "quantity": 120, "price": 45},
                {"name": "Toilet Paper", "quantity": 150, "price": 35},
                {"name": "Cleaning Spray", "quantity": 80, "price": 25},
                {"name": "Sponges", "quantity": 200, "price": 10}
            ]
        }

    def get_categories(self):
        return self.data.keys()

    def get_inventory(self):
        return self.data

    def get_items_by_category(self, category):
        return self.data.get(category, [])

    def add_item(self, category, name, quantity, price):
        self.data[category].append({"name": name, "quantity": quantity, "price": price})

    def remove_item(self, category, name, quantity):
        for item in self.data[category]:
            if item["name"] == name:
                if item["quantity"] >= quantity:
                    item["quantity"] -= quantity
                    break
                else:
                    messagebox.showerror("Insufficient Quantity", "Not enough quantity to remove.")
                    break

    def update_item(self, category, name, quantity, price):
        for item in self.data[category]:
            if item["name"] == name:
                item["quantity"] = quantity
                item["price"] = price
                break

    def remove_all(self):
        for category in self.data:
            self.data[category] = []

# Initialize the Inventory and the Application
inventory = Inventory()

# Set up the root window and the application
root = tk.Tk()
app = InventoryApp(root, inventory)
root.mainloop()