import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class Item:
    def __init__(self, title, category, author, cover_image=None):
        self.title = title
        self.category = category
        self.author = author
        self.cover_image = cover_image
        self.checked_out = False
        self.due_date = None

    def __str__(self):
        status = "Checked Out" if self.checked_out else "Available"
        return f"{self.title} - {self.category} by {self.author} ({status})"

class Library:
    def __init__(self):
        self.items = []
        self.fine_per_day = 1

    def add_item(self, title, category, author, cover_image=None):
        new_item = Item(title, category, author, cover_image)
        self.items.append(new_item)

    def checkout_item(self, title):
        for item in self.items:
            if item.title.lower() == title.lower() and not item.checked_out:
                item.checked_out = True
                item.due_date = datetime.now() + timedelta(days=14)
                return item
        return None

    def return_item(self, title):
        for item in self.items:
            if item.title.lower() == title.lower() and item.checked_out:
                item.checked_out = False
                overdue_days = (datetime.now() - item.due_date).days
                fine = max(0, overdue_days) * self.fine_per_day
                item.due_date = None
                return fine
        return None

    def search_items(self, query):
        return [item for item in self.items if query.lower() in item.title.lower() or
                query.lower() in item.author.lower() or query.lower() in item.category.lower()]

    def get_all_items(self):
        return self.items

class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the dashboard
        self.dashboard_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.dashboard_frame.pack(fill='both', expand=True)

        # Dashboard title
        tk.Label(self.dashboard_frame, text="Library Dashboard", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

        # Add buttons for functionalities
        button_frame = tk.Frame(self.dashboard_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Add Item", command=self.open_add_item_window, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Checkout Item", command=self.open_checkout_window, width=15, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Return Item", command=self.open_return_window, width=15, bg="#FF5722", fg="white").grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Search Items", command=self.open_search_window, width=15, bg="#FFC107", fg="white").grid(row=0, column=3, padx=10)
        tk.Button(button_frame, text="View All Items", command=self.open_view_all_window, width=15, bg="#673AB7", fg="white").grid(row=0, column=4, padx=10)

    def open_add_item_window(self):
        self.add_item_window = tk.Toplevel(self.root)
        self.add_item_window.title("Add New Item")
        self.add_item_window.geometry("400x300")

        tk.Label(self.add_item_window, text="Title").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.add_item_window, text="Category").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.add_item_window, text="Author").grid(row=2, column=0, padx=10, pady=10)

        self.add_title_entry = tk.Entry(self.add_item_window, width=30)
        self.add_category_entry = tk.Entry(self.add_item_window, width=30)
        self.add_author_entry = tk.Entry(self.add_item_window, width=30)

        self.add_title_entry.grid(row=0, column=1)
        self.add_category_entry.grid(row=1, column=1)
        self.add_author_entry.grid(row=2, column=1)

        tk.Button(self.add_item_window, text="Add Item", command=self.add_item, width=20, bg="#4CAF50", fg="white").grid(row=3, columnspan=2, pady=10)

    def open_checkout_window(self):
        self.checkout_window = tk.Toplevel(self.root)
        self.checkout_window.title("Checkout Item")
        self.checkout_window.geometry("400x200")

        tk.Label(self.checkout_window, text="Title").grid(row=0, column=0, padx=10, pady=10)

        self.checkout_title_entry = tk.Entry(self.checkout_window, width=30)
        self.checkout_title_entry.grid(row=0, column=1)

        tk.Button(self.checkout_window, text="Checkout", command=self.checkout_item, width=20, bg="#2196F3", fg="white").grid(row=1, columnspan=2, pady=10)

    def open_return_window(self):
        self.return_window = tk.Toplevel(self.root)
        self.return_window.title("Return Item")
        self.return_window.geometry("400x200")

        tk.Label(self.return_window, text="Title").grid(row=0, column=0, padx=10, pady=10)

        self.return_title_entry = tk.Entry(self.return_window, width=30)
        self.return_title_entry.grid(row=0, column=1)

        tk.Button(self.return_window, text="Return", command=self.return_item, width=20, bg="#FF5722", fg="white").grid(row=1, columnspan=2, pady=10)

    def open_search_window(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search Items")
        self.search_window.geometry("400x300")

        tk.Label(self.search_window, text="Search").grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(self.search_window, width=30)
        self.search_entry.grid(row=0, column=1)

        tk.Button(self.search_window, text="Search", command=self.search_items, width=15, bg="#FFC107", fg="white").grid(row=0, column=2)

        self.results_listbox = tk.Listbox(self.search_window, width=50, height=10)
        self.results_listbox.grid(row=1, columnspan=3, pady=10)

    def open_view_all_window(self):
        self.view_all_window = tk.Toplevel(self.root)
        self.view_all_window.title("View All Items")
        self.view_all_window.geometry("400x300")

        self.all_items_listbox = tk.Listbox(self.view_all_window, width=50, height=10)
        self.all_items_listbox.pack(pady=10)

        tk.Button(self.view_all_window, text="Refresh", command=self.refresh_all_items, width=20, bg="#673AB7", fg="white").pack(pady=5)

    def add_item(self):
        title = self.add_title_entry.get()
        category = self.add_category_entry.get()
        author = self.add_author_entry.get()

        if title and category and author:
            self.library.add_item(title, category, author)
            messagebox.showinfo("Success", "Item added successfully!")
            self.add_title_entry.delete(0, tk.END)
            self.add_category_entry.delete(0, tk.END)
            self.add_author_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def checkout_item(self):
        title = self.checkout_title_entry.get()
        item = self.library.checkout_item(title)
        if item:
            messagebox.showinfo("Success", f"Checked out {item.title} until {item.due_date.strftime('%Y-%m-%d')}.")
            self.checkout_title_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Checkout Error", "Item not available or does not exist.")

    def return_item(self):
        title = self.return_title_entry.get()
        fine = self.library.return_item(title)
        if fine is not None:
            if fine > 0:
                messagebox.showinfo("Return Success", f"Item returned. Fine: ${fine}.")
            else:
                messagebox.showinfo("Return Success", "Item returned successfully with no fine.")
            self.return_title_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Return Error", "Item not checked out or does not exist.")

    def search_items(self):
        query = self.search_entry.get()
        results = self.library.search_items(query)
        self.results_listbox.delete(0, tk.END)
        if results:
            for item in results:
                self.results_listbox.insert(tk.END, str(item))
        else:
            messagebox.showinfo("Search Results", "No items found.")

    def refresh_all_items(self):
        self.all_items_listbox.delete(0, tk.END)
        for item in self.library.get_all_items():
            self.all_items_listbox.insert(tk.END, str(item))

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
