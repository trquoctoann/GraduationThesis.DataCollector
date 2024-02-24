import tkinter as tk

from labeller.label_checker import LabelChecker

root = tk.Tk()
root.title("Data Checker")
app = LabelChecker(
    root,
    "conversations\\order\\ideal_order.json",
    "conversations\\order\\final_label.json",
)
root.mainloop()
