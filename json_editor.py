import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import json

class JSONEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Editor")

        # Create and set up widgets
        self.root.geometry("1280x720")  # Set the initial window size

        self.file_label = tk.Label(root, text="Select JSON File:", font=("Arial", 12))
        self.file_label.pack(pady=(10, 0))

        self.file_button = tk.Button(root, text="Browse", command=self.browse_file, font=("Arial", 12))
        self.file_button.pack(pady=(0, 10))

        self.properties_label = tk.Label(root, text="Select Properties:", font=("Arial", 12))
        self.properties_label.pack(pady=(0, 5))

        self.properties_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 11))
        self.properties_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        self.add_property_label = tk.Label(root, text="Add New Property:", font=("Arial", 12))
        self.add_property_label.pack(pady=(0, 5))

        self.new_property_entry = tk.Entry(root, font=("Arial", 11))
        self.new_property_entry.pack(pady=(0, 5))

        self.new_property_default_label = tk.Label(root, text="Default Value for New Property:", font=("Arial", 12))
        self.new_property_default_label.pack(pady=(0, 5))

        self.new_property_default_entry = tk.Entry(root, font=("Arial", 11))
        self.new_property_default_entry.pack(pady=(0, 5))

        self.force_string_var = tk.IntVar()
        self.force_string_checkbox = tk.Checkbutton(root, text="Force String", variable=self.force_string_var, font=("Arial", 11))
        self.force_string_checkbox.pack(pady=(0, 10))

        self.add_property_button = tk.Button(root, text="Add Property", command=self.add_new_property, font=("Arial", 12))
        self.add_property_button.pack(pady=(0, 10))

        self.delete_property_button = tk.Button(root, text="Delete Property", command=self.delete_property, font=("Arial", 12))
        self.delete_property_button.pack(pady=(0, 10))

        self.save_button = tk.Button(root, text="Save Changes", command=self.save_changes, font=("Arial", 12))
        self.save_button.pack(pady=(0, 10))

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.json_file_path = file_path
            self.load_properties()

    def load_properties(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        properties = list(data[0].keys()) if data else []
        self.properties_listbox.delete(0, tk.END)
        for prop in properties:
            self.properties_listbox.insert(tk.END, prop)

    def add_new_property(self):
        new_property = self.new_property_entry.get()
        new_property_default_value = self.new_property_default_entry.get()
        force_string = self.force_string_var.get()

        if new_property:
            # Add new property to the list of existing properties
            self.properties_listbox.insert(tk.END, new_property)

            # Update the JSON data with the new property and default value
            with open(self.json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            for entry in data:
                # Convert default value to the appropriate data type
                if force_string:
                    entry[new_property] = new_property_default_value
                elif new_property_default_value.lower() == 'true':
                    entry[new_property] = True
                elif new_property_default_value.lower() == 'false':
                    entry[new_property] = False
                elif new_property_default_value.isdigit():
                    entry[new_property] = int(new_property_default_value)
                elif new_property_default_value.replace('.', '', 1).isdigit():
                    entry[new_property] = float(new_property_default_value)
                else:
                    entry[new_property] = new_property_default_value

            # Save the updated JSON data to the file
            with open(self.json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            # Show the updated JSON data
            print(data)

            # Clear the input fields
            self.new_property_entry.delete(0, tk.END)
            self.new_property_default_entry.delete(0, tk.END)

    def delete_property(self):
        selected_properties = self.properties_listbox.curselection()
        selected_properties = [self.properties_listbox.get(index) for index in selected_properties]

        if not selected_properties:
            messagebox.showwarning("No Selection", "Please select a property to delete.")
            return

        confirmation = messagebox.askyesno("Confirm Deletion", f"Do you want to delete the selected properties: {', '.join(selected_properties)}?")
        if confirmation:
            # Update the JSON data by removing the selected properties
            with open(self.json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            for entry in data:
                for prop in selected_properties:
                    entry.pop(prop, None)

            # Save the updated JSON data to the file
            with open(self.json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            # Show the updated JSON data
            print(data)

            # Refresh the list of properties
            self.load_properties()

    def save_changes(self):
        messagebox.showinfo("Save Changes", "Changes saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditor(root)
    root.mainloop()
