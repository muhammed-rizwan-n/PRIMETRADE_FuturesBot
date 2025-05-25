import tkinter as tk
from tkinter import ttk,messagebox

class BotGUI:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root
        self.root.title("USDT-M Futures Bot")

        tk.Label(root, text="Symbol (e.g. BTC):").grid(row=0, column=0)
        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.grid(row=0, column=1)

        tk.Label(root, text="Side:").grid(row=1, column=0)
        self.side_var = tk.StringVar(value="BUY")
        ttk.Combobox(root, textvariable=self.side_var, values=["BUY", "SELL"]).grid(row=1, column=1)

        tk.Label(root, text="Order Type:").grid(row=2, column=0)
        self.type_var = tk.StringVar(value="MARKET")
        self.type_box = ttk.Combobox(root, textvariable=self.type_var, values=["MARKET", "LIMIT"])
        self.type_box.grid(row=2, column=1)
        self.type_box.bind("<<ComboboxSelected>>", self.toggle_fields)

        tk.Label(root, text="Quantity:").grid(row=3, column=0)
        self.qty_entry = tk.Entry(root)
        self.qty_entry.grid(row=3, column=1)

        tk.Label(root, text="Limit Price:").grid(row=4, column=0)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=4, column=1)

        #Logging
        self.result = tk.Text(root, height=10, width=50)
        self.result.grid(row=7, columnspan=2)

        tk.Button(root, text="Place Order", command=self.submit_order).grid(row=6, columnspan=2)

        self.toggle_fields()  # Disable unused fields at startup

    def toggle_fields(self, *_):
        type_ = self.type_var.get()
        self.price_entry.config(state="normal" if type_ == "LIMIT" else "disabled")

    def submit_order(self):
        symbol = self.symbol_entry.get().strip().upper()+'USDT'
        side = self.side_var.get()
        order_type = self.type_var.get()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        try:
            if symbol == 'USDT':
                raise Exception("Invalid Symbol")
            quantity = float(qty)
            price_f = float(price) if price else None

            order = self.bot.place_order(symbol, side, order_type, quantity, price_f)
            if order:
                self.result.insert(tk.END, f">> Order Successful:\n{order}\n\n")
            else:
                raise Exception()
        except Exception as e:
            self.result.insert(tk.END, f">> Error: {str(e)}\n\n")
            messagebox.showerror("Order Failed", str(e))