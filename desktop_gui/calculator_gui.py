import tkinter as tk
from core.calculator import Calculator, InvalidNumberOrOperator


class CalculatorGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.bind('<Return>', self.evaluate)

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