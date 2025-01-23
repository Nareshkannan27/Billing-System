import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk
from datetime import datetime
from fpdf import FPDF

ADMIN_PASSWORD = "2345"

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Britez Footwear Billing System")
        self.root.geometry("1600x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.init_database()
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(self.main_frame, text="Britez Footwear Billing System", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Billing Page", command=self.billing_page).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Admin Page", command=self.admin_page_login).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def init_database(self):
        conn = sqlite3.connect("britez_footwear.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Price REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transactions (
                TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerName TEXT,
                Phone TEXT,
                Products TEXT,
                Quantity INTEGER,
                TotalPrice REAL,
                CustomerCashGiven REAL,
                Balance REAL,
                PaymentMode TEXT,
                Date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def billing_page(self):
        self.main_frame.pack_forget()
        BillingPage(self.root)

    def admin_page_login(self):
        password = ctk.CTkInputDialog(text="Enter Admin Password:", title="Admin Login").get_input()
        if password == ADMIN_PASSWORD:
            self.main_frame.pack_forget()
            AdminPanel(self.root)
        else:
            messagebox.showerror("Error", "Invalid Password")

class BillingPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Page")
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.items = []  # List to store invoice items

        # Customer Details
        ctk.CTkLabel(self.frame, text="Customer Name:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.frame, text="Mobile No:").grid(row=0, column=2, padx=10, pady=10)

        self.customer_name = ctk.CTkEntry(self.frame, width=250)
        self.customer_name.grid(row=0, column=1, padx=10, pady=10)

        self.mobile_no = ctk.CTkEntry(self.frame, width=250)
        self.mobile_no.grid(row=0, column=3, padx=10, pady=10)

        # Product and Quantity
        ctk.CTkLabel(self.frame, text="Product:").grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Quantity:").grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Price:").grid(row=1, column=4, padx=5, pady=5)

        self.product_name = ttk.Combobox(self.frame, state="readonly")
        self.product_name.grid(row=1, column=1, padx=5, pady=5)
        self.product_name.bind("<<ComboboxSelected>>", self.update_price)

        self.quantity = ctk.CTkEntry(self.frame, width=100)
        self.quantity.grid(row=1, column=3, padx=5, pady=5)

        self.price = ctk.CTkEntry(self.frame, width=100, state="readonly")
        self.price.grid(row=1, column=5, padx=5, pady=5)

        # Populate product dropdown
        self.populate_products()

        # Buttons
        ctk.CTkButton(self.frame, text="Add to Invoice", command=self.add_to_invoice).grid(row=1, column=6, padx=5, pady=5)
        ctk.CTkButton(self.frame, text="Generate Invoice", command=self.generate_invoice).grid(row=3, column=6, padx=5, pady=5)
        ctk.CTkButton(self.frame, text="Go Back", command=self.go_back).grid(row=3, column=0, padx=5, pady=5)

        # Invoice List
        self.invoice_list = ttk.Treeview(self.frame, columns=("Product", "Quantity", "Price", "Total"), show="headings")
        self.invoice_list.heading("Product", text="Product")
        self.invoice_list.heading("Quantity", text="Quantity")
        self.invoice_list.heading("Price", text="Price")
        self.invoice_list.heading("Total", text="Total")
        self.invoice_list.grid(row=2, column=0, columnspan=7, pady=10)

    def populate_products(self):
        conn = sqlite3.connect('britez_footwear.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Products")
        products = cursor.fetchall()
        self.product_name['values'] = [product[0] for product in products]
        conn.close()

    def update_price(self, event):
        product = self.product_name.get()
        conn = sqlite3.connect('britez_footwear.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Price FROM Products WHERE Name = ?", (product,))
        price = cursor.fetchone()
        if price:
            self.price.configure(state="normal")
            self.price.delete(0, ctk.END)
            self.price.insert(0, str(price[0]))
            self.price.configure(state="readonly")
        conn.close()

    def add_to_invoice(self):
        product = self.product_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if not product or not quantity or not price:
            messagebox.showerror("Error", "Please fill all product details!")
            return

        try:
            total = int(quantity) * float(price)
            self.items.append((product, quantity, price, total))
            self.invoice_list.insert("", "end", values=(product, quantity, price, total))

            self.product_name.set("")
            self.quantity.delete(0, ctk.END)
            self.price.configure(state="normal")
            self.price.delete(0, ctk.END)
            self.price.configure(state="readonly")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price entered!")

    def get_payment_details(self, total_amount):
        # Create a dialog to get payment details
        payment_window = ctk.CTkToplevel(self.root)
        payment_window.title("Payment Details")
        payment_window.geometry("400x300")
        
        ctk.CTkLabel(payment_window, text=f"Total Amount: ${total_amount}", font=("Arial", 16)).pack(pady=10)
        
        ctk.CTkLabel(payment_window, text="Payment Mode:").pack(pady=5)
        payment_mode = ttk.Combobox(payment_window, values=["Cash", "Card", "UPI"])
        payment_mode.pack(pady=5)
        payment_mode.set("Cash")
        
        ctk.CTkLabel(payment_window, text="Cash Given:").pack(pady=5)
        cash_given = ctk.CTkEntry(payment_window)
        cash_given.pack(pady=5)
        
        payment_details = {}
        
        def submit_payment():
            try:
                cash_input = float(cash_given.get())
                if cash_input < total_amount:
                    messagebox.showerror("Error", "Insufficient cash!")
                    return
                
                payment_details['cash_given'] = cash_input
                payment_details['balance'] = round(cash_input - total_amount, 2)
                payment_details['payment_mode'] = payment_mode.get()
                payment_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid cash amount!")
        
        ctk.CTkButton(payment_window, text="Submit", command=submit_payment).pack(pady=10)
        
        payment_window.wait_window()
        return payment_details

    def generate_invoice(self):
        if not self.items:
            messagebox.showerror("Error", "No items in the invoice!")
            return

        # Check if customer details are entered
        customer_name = self.customer_name.get().strip()
        phone = self.mobile_no.get().strip()
        if not customer_name or not phone:
            messagebox.showerror("Error", "Please enter customer details!")
            return

        # Calculate total amount
        total_amount = sum(item[3] for item in self.items)

        # Get payment details
        payment_details = self.get_payment_details(total_amount)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Britez Footwear Invoice", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Customer: {customer_name} | Phone: {phone}", ln=True, align="L")
        pdf.cell(200, 10, txt="Items Purchased:", ln=True, align="L")

        product_list = []  # To store product names

        for item in self.items:
            product, quantity, price, total = item
            pdf.cell(200, 10, txt=f"{product} - {quantity} pcs @ ${price} = ${total}", ln=True, align="L")
            product_list.append(f"{product} ({quantity})")

        pdf.cell(200, 10, txt=f"Total: ${total_amount}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Payment Mode: {payment_details['payment_mode']}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Cash Given: ${payment_details['cash_given']}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Balance: ${payment_details['balance']}", ln=True, align="L")
        pdf.output("invoice.pdf")

        # Save transaction to database
        conn = sqlite3.connect('britez_footwear.db')
        cursor = conn.cursor()
        products_str = ", ".join(product_list)

        try:
            cursor.execute("""
                INSERT INTO Transactions 
                (CustomerName, Phone, Products, Quantity, TotalPrice, CustomerCashGiven, Balance, PaymentMode, Date) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_name, 
                phone, 
                products_str, 
                sum(int(item[1]) for item in self.items),  # Total quantity
                total_amount, 
                payment_details['cash_given'], 
                payment_details['balance'], 
                payment_details['payment_mode'], 
                datetime.now().strftime('%Y-%m-%d')
            ))
            conn.commit()
            messagebox.showinfo("Success", "Invoice generated and saved!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to save transaction: {e}")
        finally:
            conn.close()

        # Clear invoice data
        self.items.clear()
        self.invoice_list.delete(*self.invoice_list.get_children())

    def go_back(self):
        self.frame.pack_forget()
        BillingSystem(self.root)
class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Add Product", command=self.add_product).pack(pady=10)
        ctk.CTkButton(self.frame, text="View Database", command=self.view_database).pack(pady=10)
        ctk.CTkButton(self.frame, text="Back to Home", command=self.back_to_home).pack(pady=10)

    def add_product(self):
        AddProduct(self.root, self.frame)

    def view_database(self):
        ViewDatabase(self.root, self.frame)

    def back_to_home(self):
        self.frame.pack_forget()
        BillingSystem(self.root)
class AddProduct:
    def __init__(self, root, admin_frame):
        self.root = root
        self.admin_frame = admin_frame
        self.admin_frame.pack_forget()

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Price:").grid(row=0, column=2, padx=5, pady=5)

        self.product_name = ctk.CTkEntry(self.frame, width=200)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)
        self.product_price = ctk.CTkEntry(self.frame, width=200)
        self.product_price.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkButton(self.frame, text="Add Product", command=self.save_product).grid(row=1, column=1, columnspan=2, pady=10)
        ctk.CTkButton(self.frame, text="Back", command=self.back_to_admin).grid(row=1, column=3, pady=10)

    def save_product(self):
        name = self.product_name.get()
        price = self.product_price.get()

        if not name or not price:
            messagebox.showerror("Error", "Please complete all fields!")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid price! Please enter a number.")
            return

        conn = sqlite3.connect('britez_footwear.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (Name, Price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully!")
        self.product_name.delete(0, ctk.END)
        self.product_price.delete(0, ctk.END)

    def back_to_admin(self):
        self.frame.pack_forget()
        self.admin_frame.pack()

class ViewDatabase:
    def __init__(self, root, admin_frame):
        self.root = root
        self.admin_frame = admin_frame
        self.admin_frame.pack_forget()

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Products Tab
        self.products_tab = ttk.Treeview(self.notebook, columns=("ID", "Name", "Price"), show="headings")
        self.products_tab.heading("ID", text="ProductID")
        self.products_tab.heading("Name", text="Name")
        self.products_tab.heading("Price", text="Price")
        self.notebook.add(self.products_tab, text="Products")

        # Transactions Tab
        self.transactions_tab = ttk.Treeview(self.notebook, columns=("TransactionID", "CustomerName", "Phone", "Products", "Quantity", "TotalPrice", "CustomerCashGiven", "Balance", "PaymentMode", "Date"), show="headings")
        columns = ["TransactionID", "CustomerName", "Phone", "Products", "Quantity", "TotalPrice", "CustomerCashGiven", "Balance", "PaymentMode", "Date"]
        for column in columns:
            self.transactions_tab.heading(column, text=column)
        self.notebook.add(self.transactions_tab, text="Transactions")

        # Add scrollbars
        products_scrollbar = ttk.Scrollbar(self.notebook, orient="vertical", command=self.products_tab.yview)
        self.products_tab.configure(yscroll=products_scrollbar.set)

        transactions_scrollbar = ttk.Scrollbar(self.notebook, orient="vertical", command=self.transactions_tab.yview)
        self.transactions_tab.configure(yscroll=transactions_scrollbar.set)

        self.load_data()

        ctk.CTkButton(self.frame, text="Go Back", command=self.back_to_admin).pack(pady=10)

    def load_data(self):
        
        for i in self.products_tab.get_children():
            self.products_tab.delete(i)
        for i in self.transactions_tab.get_children():
            self.transactions_tab.delete(i)

        
        conn = sqlite3.connect('britez_footwear.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        for row in products:
            self.products_tab.insert("", "end", values=row)


        cursor.execute("SELECT * FROM Transactions")
        transactions = cursor.fetchall()
        for row in transactions:
            self.transactions_tab.insert("", "end", values=row)

        conn.close()

    def back_to_admin(self):
        self.frame.pack_forget()
        self.admin_frame.pack()
if __name__ == "__main__":
    root = ctk.CTk()
    app = BillingSystem(root)
    root.mainloop()