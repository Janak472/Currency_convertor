
import requests
import tkinter as tk
from tkinter import ttk


class RealTimeCurrencyConverter:
    def __init__(self, url):
        # Fetch currency exchange rate data from API
        self.data = requests.get(url).json()
        # Extract currency exchange rates
        self.currencies = self.data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        # Convert from the source currency to USD if not USD
        if from_currency != "USD":
            amount = amount / self.currencies[from_currency]
        # Convert from USD to the target currency
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


class App(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title("Currency Converter")
        self.currency_converter = converter

        # Set up GUI
        self.geometry("500x200")

        # Label to welcome users
        self.intro_label = tk.Label(
            self,
            text="Welcome to Real Time Currency Converter",
            fg="blue",
            relief=tk.RAISED,
            borderwidth=3,
        )
        self.intro_label.config(font=("Courier", 15, "bold"))

        # Label to display exchange rate information
        self.date_label = tk.Label(
            self,
            text=f"1 Indian Rupee equals = {self.currency_converter.convert('INR', 'USD', 1)} USD \n Date : {self.currency_converter.data['date']}",
            relief=tk.GROOVE,
            borderwidth=5,
        )

        # Place labels in GUI
        self.intro_label.place(x=10, y=5)
        self.date_label.place(x=160, y=50)

        # Validate input in the amount entry field
        valid = (self.register(self.restrictNumberOnly), "%d", "%P")
        self.amount_field = tk.Entry(
            self,
            bd=3,
            relief=tk.RIDGE,
            justify=tk.CENTER,
            validate="key",
            validatecommand=valid,
        )

        # Label to display converted amount
        self.converted_amount_field_label = tk.Label(
            self,
            text="",
            fg="black",
            bg="white",
            relief=tk.RIDGE,
            justify=tk.CENTER,
            width=17,
            borderwidth=3,
        )

        # Set default currencies
        self.from_currency_variable = tk.StringVar(self)
        self.from_currency_variable.set("INR")
        self.to_currency_variable = tk.StringVar(self)
        self.to_currency_variable.set("USD")

        font = ("Courier", 12, "bold")

        # Dropdown for selecting source currency
        self.from_currency_dropdown = ttk.Combobox(
            self,
            textvariable=self.from_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state="readonly",
            width=12,
            justify=tk.CENTER,
        )

        # Dropdown for selecting target currency
        self.to_currency_dropdown = ttk.Combobox(
            self,
            textvariable=self.to_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state="readonly",
            width=12,
            justify=tk.CENTER,
        )

        # Place dropdowns and entry field in GUI
        self.from_currency_dropdown.place(x=30, y=120)
        self.amount_field.place(x=36, y=150)
        self.to_currency_dropdown.place(x=340, y=120)
        self.converted_amount_field_label.place(x=346, y=150)

        # Convert button
        self.convert_button = tk.Button(
            self, text="Convert", fg="black", command=self.perform
        )
        self.convert_button.config(font=("Courier", 10, "bold"))
        self.convert_button.place(x=225, y=135)

    def perform(self):
        # Get input values
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        # Convert and round the amount
        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        # Display converted amount
        self.converted_amount_field_label.config(text=str(converted_amount))

    def restrictNumberOnly(self, action, string):
        # Validate input to allow only numbers and at most one decimal point
        import re
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (string.count(".") <= 1 and result is not None)


if __name__ == "__main__":
    # API endpoint for currency exchange rates
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    converter = RealTimeCurrencyConverter(url)

    # Create and run the GUI application
    app = App(converter)
    app.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
