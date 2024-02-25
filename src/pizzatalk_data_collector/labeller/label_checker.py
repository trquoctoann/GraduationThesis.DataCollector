import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from constants.entity_iob_label import EntityIOBLabel


class LabelChecker:
    def __init__(self, root, data_source_path):
        self.root = root
        self.data_source = self.load_data_from_json(data_source_path)
        self.current_index = self.read_last_position()
        self.start_index = self.read_last_position()
        self.edited_data = {}
        self.checked_states = {}
        self.output_path = self.get_output_filepath()
        self.current_number_of_label_checked = 0

        self.setup_ui()
        self.display_data()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            self.frame, columns=("Word", "Label"), show="headings"
        )
        self.tree.heading("Word", text="Word")
        self.tree.heading("Label", text="Label")
        self.tree.column("Word", width=100)
        self.tree.column("Label", width=200)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.number_checked_label = tk.Label(
            self.frame,
            text=f"Number of checked labels: {self.current_number_of_label_checked}",
            fg="red",
            font=("Arial", 10),
        )
        self.number_checked_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(
            self.frame, text="", fg="green", font=("Arial", 10)
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.save_button = tk.Button(
            self.frame, text="Save Changes", command=self.save_changes
        )
        self.save_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.prev_button = tk.Button(
            self.frame, text="Previous", command=self.load_prev_data
        )
        self.prev_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.next_button = tk.Button(
            self.frame, text="Next", command=self.load_next_data
        )
        self.next_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.finish_button = tk.Button(
            self.frame, text="Finish Label", command=self.finish_labeling
        )
        self.finish_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.label_options = [
            EntityIOBLabel.OTHER.value,
            EntityIOBLabel.B_QUANTITY.value,
            EntityIOBLabel.I_QUANTITY.value,
            EntityIOBLabel.B_PIZZA.value,
            EntityIOBLabel.I_PIZZA.value,
            EntityIOBLabel.B_TOPPING.value,
            EntityIOBLabel.I_TOPPING.value,
            EntityIOBLabel.B_SIZE.value,
            EntityIOBLabel.I_SIZE.value,
            EntityIOBLabel.B_CRUST.value,
            EntityIOBLabel.I_CRUST.value,
            EntityIOBLabel.B_CUSTOMER_NAME.value,
            EntityIOBLabel.I_CUSTOMER_NAME.value,
            EntityIOBLabel.B_PHONE_NUMBER.value,
            EntityIOBLabel.I_PHONE_NUMBER.value,
            EntityIOBLabel.B_ADDRESS.value,
            EntityIOBLabel.I_ADDRESS.value,
            EntityIOBLabel.B_PAYMENT_METHOD.value,
            EntityIOBLabel.I_PAYMENT_METHOD.value,
        ]
        self.combobox = ttk.Combobox(
            self.root, values=self.label_options, state="readonly"
        )
        self.combobox.bind("<<ComboboxSelected>>", self.on_label_selected)

        self.tree.bind("<1>", self.on_row_selected)

    def load_data_from_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def read_last_position(self):
        try:
            with open(
                "src\\pizzatalk_data_collector\\labeller\\last_labeled_position.txt",
                "r",
            ) as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def get_output_filepath(self):
        return (
            "conversations\\order\\final_label_"
            + str(datetime.now().strftime("%Y%m%d"))
            + ".json"
        )

    def display_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        current_data = self.data_source[self.current_index]
        for word, label in zip(current_data["words"], current_data["label"]):
            self.tree.insert("", tk.END, values=(word, label))
        self.tree.selection_remove(self.tree.selection())

    def on_row_selected(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            rowid = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            if column == "#2":
                x, y, width, height = self.tree.bbox(rowid, column)
                self.combobox.place(x=x, y=y, width=width, height=height)
                self.combobox.set(self.tree.item(rowid, "values")[1])
                self.current_item = rowid

    def on_label_selected(self, event):
        if self.current_item:
            new_label = self.combobox.get()
            self.tree.item(
                self.current_item,
                values=(
                    self.tree.item(self.current_item, "values")[0],
                    new_label,
                ),
            )
            word, _ = self.tree.item(self.current_item, "values")
            self.data_source[self.current_index]["label"][
                self.tree.index(self.current_item)
            ] = new_label
            self.combobox.place_forget()

    def save_changes(self):
        current_data = self.data_source[self.current_index]
        if self.current_index not in self.edited_data:
            self.current_number_of_label_checked += 1
        self.edited_data[self.current_index] = current_data
        self.checked_states[self.current_index] = True
        self.update_ui_for_current_object()
        self.load_next_data()

    def update_ui_for_current_object(self):
        self.number_checked_label.config(
            text=f"Number of checked labels: {self.current_number_of_label_checked}"
        )
        if self.current_index in self.checked_states:
            self.status_label.config(text="Checked", fg="green")
        else:
            self.status_label.config(text="", fg="black")

    def load_next_data(self):
        if self.current_index < len(self.data_source) - 1:
            self.current_index += 1
            self.update_ui_for_current_object()
            self.display_data()

        else:
            messagebox.showinfo(
                "Information",
                "No more data to display. This is the last data object.",
            )

    def load_prev_data(self):
        if self.current_index > self.start_index:
            self.current_index -= 1
            self.update_ui_for_current_object()
            self.display_data()
        else:
            messagebox.showinfo(
                "Information",
                "This is the first data object. There is no previous data to display.",
            )

    def saving_result(self, checked_data):
        filename = self.output_path
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r+", encoding="utf-8") as file:
                content = file.read()
                if content.endswith("]"):
                    content = content[:-1] + ","
                else:
                    content += "["

                for item in checked_data:
                    json_str = json.dumps(item, ensure_ascii=False, indent=4)
                    content += json_str + ",\n"

                content = content.rstrip(",\n") + "]"
                file.seek(0)
                file.write(content)
                file.truncate()
        else:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(checked_data, file, ensure_ascii=False, indent=4)

    def finish_labeling(self):
        self.saving_result(
            [self.edited_data[i] for i in sorted(self.edited_data.keys())],
        )

        with open(
            "src\\pizzatalk_data_collector\\labeller\\last_labeled_position.txt",
            "w",
        ) as f:
            f.write(str(self.current_index))

        messagebox.showinfo(
            "Information",
            "All changes have been saved to "
            + self.output_path
            + ". The application will now close.",
        )
        self.root.destroy()
