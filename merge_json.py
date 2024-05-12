import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Label, simpledialog, Toplevel, StringVar
import json

class JsonMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Merger Tool")
        self.root.geometry("1280x720")  # Set the initial window size
        self.file1_data = None
        self.file2_data = None
        self.match_property1 = None
        self.match_property2 = None
        self.selected_properties1 = []
        self.selected_properties2 = []

        # Layout
        self.status_label = tk.Label(root, text="No files loaded.")
        self.status_label.pack()

        load_btn1 = tk.Button(root, text="Load JSON File 1", command=self.load_file1)
        load_btn1.pack()
        load_btn2 = tk.Button(root, text="Load JSON File 2", command=self.load_file2)
        load_btn2.pack()
        merge_btn = tk.Button(root, text="Merge JSON Files", command=self.merge_json)
        merge_btn.pack()

    def load_file1(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                self.file1_data = json.load(file)
            self.status_label.config(text="File 1 loaded. Select properties.")
            self.select_properties(self.file1_data, 1)

    def load_file2(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                self.file2_data = json.load(file)
            self.status_label.config(text="File 2 loaded. Select properties.")
            self.select_properties(self.file2_data, 2)

    def select_properties(self, data, file_number):
        window = Toplevel(self.root)
        window.geometry("400x300")
        window.title(f"Select Properties for JSON {file_number}")
        Label(window, text="Select Match Property:").pack()
        listbox = Listbox(window, selectmode='single')
        listbox.pack()

        properties = list(data[0].keys())
        for item in properties:
            listbox.insert(tk.END, item)

        def on_property_selected():
            selected_index = listbox.curselection()
            match_property = listbox.get(selected_index)
            if file_number == 1:
                self.match_property1 = match_property
            else:
                self.match_property2 = match_property

            window.destroy()
            self.select_output_properties(data, file_number)

        select_button = tk.Button(window, text="Select", command=on_property_selected)
        select_button.pack()

    def select_output_properties(self, data, file_number):
        window = Toplevel(self.root)
        window.geometry("400x300")
        window.title(f"Select Output Properties for JSON {file_number}")
        Label(window, text="Select properties to include in output:").pack()
        listbox = Listbox(window, selectmode='multiple')
        listbox.pack()

        properties = list(data[0].keys())
        for item in properties:
            listbox.insert(tk.END, item)

        def on_selection_done():
            selected_indices = listbox.curselection()
            selected_properties = [listbox.get(i) for i in selected_indices]
            if file_number == 1:
                self.selected_properties1 = selected_properties
            else:
                self.selected_properties2 = selected_properties

            window.destroy()

        done_button = tk.Button(window, text="Done", command=on_selection_done)
        done_button.pack()

    def merge_json(self):
        if not all([self.file1_data, self.file2_data, self.match_property1, self.match_property2,
                    self.selected_properties1, self.selected_properties2]):
            messagebox.showerror("Error", "Please load both files and select properties.")
            return

        # Creating a mapping based on the selected match property, taking the first occurrence only
        map2 = {}
        for item in self.file2_data:
            key = item.get(self.match_property2)
            if key not in map2:  # Check if key already exists
                map2[key] = item  # Assign only if key does not exist

        merged_data = []

        for item1 in self.file1_data:
            key = item1.get(self.match_property1)
            if key in map2:
                item2 = map2[key]
                merged_item = {prop: item1[prop] for prop in self.selected_properties1 if prop in item1}
                merged_item.update({prop: item2[prop] for prop in self.selected_properties2 if prop in item2})
                merged_data.append(merged_item)

        # Saving the merged file
        output_file = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(merged_data, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", "JSON file has been created successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonMergerApp(root)
    root.mainloop()
