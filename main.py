import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import date, timedelta
from medicine_db import (
    medicine_exists,
    add_medicine as db_add_medicine,
    get_all_medicines,
    get_medicine,
    update_medicine as db_update_medicine,
    delete_medicine as db_delete_medicine,
    search_medicine_names,
    get_dashboard_stats,get_expiring_medicines
)
from billing_db import (
    get_medicine_stock,
    get_bill_history,
    save_bill_and_update_stock
)
selected_medicine = None
def autocomplete_bill_medicine(event):
    text = bill_medicine_entry.get().strip()

    if not text:
        bill_medicine_entry["values"] = []
        return

    matches = search_medicine_names(text)

    bill_medicine_entry["values"] = matches

    if matches:
        bill_medicine_entry.event_generate("<Alt-Down>")
def autocomplete_delete_medicine(event):
    text = entry_delete.get().strip()

    if not text:
        entry_delete["values"] = []
        return

    matches = search_medicine_names(text)

    entry_delete["values"] = matches

    if matches:
        entry_delete.event_generate("<Alt-Down>")
def add_medicine():
    name = entry_name.get().strip()
    qty = entry_qty.get().strip()
    price = entry_price.get().strip()
    expiry = entry_expiry.get().strip()

    if not name or not qty or not price or not expiry:
        messagebox.showerror(
            "Error",
            "Please fill in all fields"
        )
        return

    
    try:
        qty = int(qty)

        if qty <= 0:
            messagebox.showerror(
                "Error",
                "Quantity must be greater than 0"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a whole number"
        )
        return

    
    try:
        price = float(price)

        if price <= 0:
            messagebox.showerror(
                "Error",
                "Price must be greater than 0"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Price must be a valid number"
        )
        return

    
    if medicine_exists(name):
        messagebox.showerror(
        "Duplicate Medicine",
        f"{name} already exists in the inventory."
    )
        return

    db_add_medicine(name, qty, price, expiry)

    messagebox.showinfo(
        "Success",
        "Medicine Added"
    )

    update_dashboard()
    view_medicines()
    clear_fields()
def view_medicines():
    rows=get_all_medicines()

    
    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        if int(row[1]) < 20:
            tree.insert("", "end", values=row, tags=("low_stock",))
        else:
            tree.insert("", "end", values=row)

def search_medicine():
    name = entry_search.get().strip()

    if not name:
        messagebox.showerror("Error", "Enter a medicine name")
        return

    r = get_medicine(name)

    if not r:
        messagebox.showerror("Error", "Medicine Not Found")
        return
    for item in tree.selection():
        tree.selection_remove(item)

    
    for item in tree.get_children():
        values = tree.item(item, "values")

        if values[0].lower() == name.lower():
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
            break
    entry_name.delete(0, "end")
    entry_qty.delete(0, "end")
    entry_price.delete(0, "end")
    entry_expiry.delete(0, "end")

    entry_name.insert(0, r[0])
    entry_qty.insert(0, r[1])
    entry_price.insert(0, r[2])
    entry_expiry.insert(0, r[3])

def update_medicine():
    name = entry_search.get().strip()
    qty = entry_qty.get().strip()
    price = entry_price.get().strip()
    expiry = entry_expiry.get().strip()

    if not name:
        messagebox.showerror("Error", "Medicine name is required")
        return

    if not qty or not price or not expiry:
        messagebox.showerror(
            "Error",
            "Please fill in Quantity, Price and Expiry Date"
        )
        return
    try:
        qty = int(qty)

        if qty <= 0:
            messagebox.showerror(
                "Error",
                "Quantity must be greater than 0"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity must be a whole number"
        )
        return
    try:
        price = float(price)

        if price <= 0:
            messagebox.showerror(
                "Error",
                "Price must be greater than 0"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Price must be a valid number"
        )
        return
    rows_updated = db_update_medicine(
    name,
    qty,
    price,
    expiry
)

    if rows_updated:

        messagebox.showinfo(
            "Updated",
            "Medicine Updated Successfully"
        )

        view_medicines()
        update_dashboard()

    else:
        messagebox.showerror(
            "Error",
            "Medicine Not Found"
        )

def delete_medicine():
    name = entry_delete.get().strip()

    rows_deleted = db_delete_medicine(name)

    if rows_deleted:
        messagebox.showinfo("Deleted", "Medicine Removed")
        view_medicines()
        update_dashboard()

    else:
        messagebox.showerror("Error", "Medicine Not Found")

def generate_bill():
    bill_window = ttk.Toplevel(root)
    bill_window.title("Generate Bill")
    bill_window.geometry("400x400")

    bill_items = []

    ttk.Label(
    bill_window,
    text="Medicine Name"
).pack()

    bill_medicine_entry = ttk.Combobox(
    bill_window,
    width=27
)

    bill_medicine_entry.pack(pady=5)
    def autocomplete_bill_medicine(event):
        text = bill_medicine_entry.get().strip()

        if not text:
            bill_medicine_entry["values"] = []
            return

        matches = search_medicine_names(text)

        bill_medicine_entry["values"] = matches

        if matches:
            bill_medicine_entry.event_generate("<Alt-Down>")
    bill_medicine_entry.bind(
    "<KeyRelease>",
    autocomplete_bill_medicine
)

    ttk.Label(bill_window, text="Quantity").pack()
    entry_qty = ttk.Entry(bill_window)
    entry_qty.pack()

    result_box = ttk.Text(bill_window, height=10, width=40)
    result_box.pack(pady=10)

    total_label = ttk.Label(bill_window, text="Total: ₹0")
    total_label.pack()

    def add_to_bill():
        name = bill_medicine_entry.get().strip()
        qty = entry_qty.get().strip()

        if not name or not qty:
            messagebox.showerror(
            "Error",
            "Enter medicine name and quantity"
        )
            return

        try:
            qty = int(qty)

            if qty <= 0:
                messagebox.showerror(
                "Error",
                "Quantity must be greater than 0"
            )
                return

        except ValueError:
            messagebox.showerror(
            "Error",
            "Quantity must be a whole number"
        )
            return

        r=get_medicine_stock(name)

        if not r:
            messagebox.showerror(
            "Error",
            "Medicine not found"
        )
            return

        stock = int(r[0])
        price = float(r[1])

    
        if qty > stock:
            messagebox.showerror(
            "Error",
            f"Only {stock} available"
        )
            return

    
        subtotal = qty * price

        bill_items.append(
        (name, qty, price, subtotal)
    )

        result_box.insert(
        "end",
        f"{name} x{qty} = ₹{subtotal:.2f}\n"
    )

        
        update_total()

        bill_medicine_entry.delete(0, "end")
        entry_qty.delete(0, "end")

    def update_total():
        total = sum(item[3] for item in bill_items)
        total_label.config(text=f"Total: ₹{total}")
    def finish_bill():
        if not bill_items:
            messagebox.showerror(
            "Error",
            "No items in the bill"
        )
            return

        total = sum(item[3] for item in bill_items)

        try:
            bill_id = save_bill_and_update_stock(
            total,
            bill_items
        )

        except ValueError as e:
            messagebox.showerror(
            "Billing Error",
            str(e)
        )
            return

        except Exception as e:
            messagebox.showerror(
            "Billing Error",
            "Unable to save the bill.\n\n"
            "Please try again."
        )
            return

        view_medicines()
        update_dashboard()

        messagebox.showinfo(
        "Bill Saved",
        f"Bill #{bill_id}\nTotal Amount: ₹{total:.2f}"
    )

        bill_window.destroy()

    

    ttk.Button(bill_window, text="Add Item",command=add_to_bill).pack(pady=5)
    ttk.Button(bill_window, text="Finish Bill", command=finish_bill).pack(pady=5)

def clear_fields():
    entry_name.delete(0, "end")
    entry_qty.delete(0,"end")
    entry_price.delete(0,"end")
    entry_expiry.delete(0,"end")
def update_dashboard():
    total, low_stock, value = get_dashboard_stats()

    total_label.config(
        text=f"Total Medicines : {total}"
    )

    low_stock_label.config(
        text=f"Low Stock : {low_stock}"
    )

    value_label.config(
        text=f"Inventory Value : ₹{value:.2f}"
    )
def autocomplete_medicine(event):
    text = entry_search.get().strip()

    if not text:
        entry_search["values"] = []
        return

    matches = search_medicine_names(text)

    entry_search["values"] = matches

    if matches:
        entry_search.event_generate("<Alt-Down>")
root = ttk.Window(themename="flatly")
root.title("Pharmaceutical Management System")
root.geometry("1100x900")
style = ttk.Style()

style.configure(
    "Treeview",
    font=("Segoe UI", 13),
    rowheight=28
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 13, "bold")
)
# ================= HEADER =================

ttk.Label(
    root,
    text="Pharmaceutical Management System",
    font=("Segoe UI", 22, "bold")
).pack(padx=10, pady=15, fill="x")


# ================= DASHBOARD =================

total_label = ttk.Label(
    root,
    text="Total Medicines : 0",
    font=("Arial", 20)
)
total_label.pack(padx=10, pady=5)

low_stock_label = ttk.Label(
    root,
    text="Low Stock : 0",
    font=("Arial", 20)
)
low_stock_label.pack(padx=10, pady=5)

value_label = ttk.Label(
    root,
    text="Inventory Value : ₹0.00",
    font=("Arial", 20)
)
value_label.pack(padx=10, pady=5)

# Main container
main_frame = ttk.Frame(root, padding=15)
main_frame.pack(fill="both", expand=True)

# Left and right sections
left_frame = ttk.Frame(main_frame, padding=(15,5))
left_frame.pack(
    side="left",
    fill="y",
    anchor="n",
    pady=0
)
right_frame = ttk.Frame(main_frame, padding=15)
right_frame.pack(side="right", fill="both", expand=True)

ttk.Label(
    right_frame,
    text="Medicine Inventory",
    font=("Segoe UI", 20, "bold")
).pack(pady=10)

tree = ttk.Treeview(
    right_frame,
    columns=("Name", "Qty", "Price", "Expiry"),
    show="headings"
)
tree.tag_configure(
    "low_stock",
    background="#ffe0e0"
)
def select_item(event):
    global selected_medicine

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    selected_medicine = values[0]

    entry_name.delete(0, "end")
    entry_qty.delete(0, "end")
    entry_price.delete(0, "end")
    entry_expiry.delete(0, "end")

    entry_name.insert(0, values[0])
    entry_qty.insert(0, values[1])
    entry_price.insert(0, values[2])
    entry_expiry.insert(0, values[3])

    entry_search.delete(0, "end")
    entry_search.insert(0, values[0])

    entry_delete.delete(0, "end")
    entry_delete.insert(0, values[0])


tree.bind("<<TreeviewSelect>>", select_item)
tree.heading("Name", text="Medicine Name",anchor="w")
tree.heading("Qty", text="Quantity",anchor="w")
tree.heading("Price", text="Price",anchor="w")
tree.heading("Expiry", text="Expiry Date",anchor="w")

tree.column("Name", width=300, anchor="w", stretch=True)
tree.column("Qty", width=120, anchor="w", stretch=True)
tree.column("Price", width=150, anchor="w", stretch=True)
tree.column("Expiry", width=180, anchor="w", stretch=True)
scrollbar = ttk.Scrollbar(
    right_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tree.pack(side="left", fill="both", expand=True)


# ================= LEFT SIDE =================

ttk.Label(
    left_frame,
    text="Medicine Name",
    font=("Segoe UI",12)
).pack(pady=5)

entry_name = ttk.Entry(left_frame, width=30)
entry_name.pack(pady=5)


ttk.Label(left_frame, text="Quantity",font=("Segoe UI", 12)).pack(pady=5)

entry_qty = ttk.Entry(left_frame, width=30)
entry_qty.pack(pady=5)


ttk.Label(left_frame, text="Price",font=("Segoe UI", 12)).pack(pady=5)

entry_price = ttk.Entry(left_frame, width=30)
entry_price.pack(pady=5)


ttk.Label(left_frame, text="Expiry Date",font=("Segoe UI", 12)).pack(pady=5)

entry_expiry = ttk.Entry(left_frame, width=30)
entry_expiry.pack(pady=5)


ttk.Button(
    left_frame,
    text="Add Medicine",
    command=add_medicine,
    bootstyle="success"
).pack(pady=8, fill="x")

# ================= SEARCH / UPDATE =================

ttk.Label(
    left_frame,
    text="Search / Update Medicine",
    font=("Segoe UI", 12)
).pack(pady=8)

entry_search = ttk.Combobox(
    left_frame,
    width=27
)

entry_search.pack(pady=5, fill="x")

entry_search.bind(
    "<KeyRelease>",
    autocomplete_medicine
)


ttk.Button(
    left_frame,
    text="Search",
    command=search_medicine,
    bootstyle="info"
).pack(pady=5, fill="x")


ttk.Button(
    left_frame,
    text="Update",
    command=update_medicine,
    bootstyle="warning"
).pack(pady=5, fill="x")


# ================= DELETE =================

ttk.Label(
    left_frame,
    text="Delete Medicine",
    font=("Segoe UI", 12)
).pack(pady=8)


entry_delete = ttk.Combobox(
    left_frame,
    width=27
)

entry_delete.pack(pady=5, fill="x")

entry_delete.bind(
    "<KeyRelease>",
    autocomplete_delete_medicine
)
ttk.Button(
    left_frame,
    text="Delete",
    command=delete_medicine,
    bootstyle="danger"
).pack(pady=5, fill="x")

def view_bill_history():
    rows = get_bill_history()

    if not rows:
        messagebox.showinfo("Bill History", "No bills found")
        return

    window = ttk.Toplevel(root)
    window.title("Bill History")
    window.geometry("1100x500")

    ttk.Label(
        window,
        text="Bill History",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=10)

    bill_tree = ttk.Treeview(
        window,
        columns=("ID", "Date", "Medicines", "Quantity", "Total"),
        show="headings"
    )

    bill_tree.heading("ID", text="Bill ID")
    bill_tree.heading("Date", text="Date")
    bill_tree.heading("Medicines", text="Medicines Bought")
    bill_tree.heading("Quantity", text="Quantity")
    bill_tree.heading("Total", text="Total Amount")

    bill_tree.column("ID", width=80, anchor="center")
    bill_tree.column("Date", width=200, anchor="center")
    bill_tree.column("Medicines", width=300, anchor="w")
    bill_tree.column("Quantity", width=150, anchor="center")
    bill_tree.column("Total", width=150, anchor="center")

    for row in rows:
        bill_tree.insert(
            "",
            "end",
            values=(
                row[0],
                row[1],
                row[2],
                row[3],
                f"₹{row[4]:.2f}"
            )
        )

    bill_tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )
# ================= BILL =================

ttk.Label(
    left_frame,
    text="Generate Bill",
    font=("Segoe UI", 12)
).pack(pady=8)


ttk.Button(
    left_frame,
    text="Generate Bill",
    command=generate_bill,
    bootstyle="success"
).pack(pady=8, fill="x")

ttk.Button(
    left_frame,
    text="Bill History",
    command=view_bill_history,
    bootstyle="info"
).pack(pady=5, fill="x", ipady=3)

# ================= START =================

update_dashboard()
view_medicines()

def check_expiry():
    today = date.today()
    warning_date = today + timedelta(days=30)

    medicines = get_expiring_medicines(warning_date)

    if not medicines:
        return

    expired = []
    expiring_soon = []

    for name, expiry in medicines:
        if expiry < today:
            expired.append(f"{name} - Expired on {expiry}")
        else:
            expiring_soon.append(f"{name} - Expires on {expiry}")

    message = ""

    if expired:
        message += "EXPIRED MEDICINES\n\n"
        message += "\n".join(expired)
        message += "\n\n"

    if expiring_soon:
        message += "EXPIRING WITHIN 30 DAYS\n\n"
        message += "\n".join(expiring_soon)

    messagebox.showwarning("Expiry Alert", message)


update_dashboard()
view_medicines()

# Check expiry once when the application starts
root.after(500, check_expiry)

root.mainloop()
