import tkinter as tk
import os
import pkgutil
from core.calculator import Calculator, InvalidNumberOrOperator


class CalculatorGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.bind('<Return>', self.evaluate)

        try:
            self.root.iconbitmap(os.path.join(os.getcwd(), "desktop_gui/media/icon.ico"))
        except tk.TclError as e:
            if not os.path.exists("media/"):
                os.mkdir("media")
            icon_data = pkgutil.get_data(__name__, '/media/icon.ico')
            with open('media/icon.ico', 'wb') as temp_icon_file:
                temp_icon_file.write(icon_data)
            icon_path = os.path.join(os.getcwd(), 'media/icon.ico')
            self.root.iconbitmap(icon_path)

        self.input_zone = tk.Entry(self.root, width=40, borderwidth=5, font=2)
        self.input_zone.bind("<KeyRelease>", lambda event: self.evaluate() if event.keycode == 187 else "")
        self.input_zone.grid(row=0, column=0, padx=10, pady=10)
        self.input_zone.focus_set()

        self.equal_button = tk.Button(self.root, text="=", padx=10, pady=3, command=self.evaluate, font=2)
        self.equal_button.grid(row=0, column=1)

        self.result_label = tk.Label(self.root, text="", font=2, padx=3)
        self.result_label.grid(row=0, column=2)

    def evaluate(self, event=None):
        input_value = self.input_zone.get().rstrip("=")
        try:
            result = Calculator(input_value).evaluate()
        except InvalidNumberOrOperator:
            result = "Error"
        self.result_label.config(text=str(result))

    def show(self):
        self.root.mainloop()