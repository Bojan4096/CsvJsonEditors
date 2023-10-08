import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd

class CSVtoJSONConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV to JSON Converter")

        # Create and set up widgets
        self.root.geometry("1280x720")  # Set the initial window size

        self.file_label = tk.Label(root, text="Select CSV File:", font=("Arial", 12))
        self.file_label.pack(pady=(10, 0))

        self.file_button = tk.Button(root, text="Browse", command=self.browse_file, font=("Arial", 12))
        self.file_button.pack(pady=(0, 10))

        self.headers_label = tk.Label(root, text="Select Headers to convert:", font=("Arial", 12))
        self.headers_label.pack(pady=(0, 5))

        self.headers_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 11))
        self.headers_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        self.add_header_label = tk.Label(root, text="Add New Header:", font=("Arial", 12))
        self.add_header_label.pack(pady=(0, 5))

        self.new_header_entry = tk.Entry(root, font=("Arial", 11))
        self.new_header_entry.pack(pady=(0, 5))

        self.new_header_default_label = tk.Label(root, text="Default Value for New Header:", font=("Arial", 12))
        self.new_header_default_label.pack(pady=(0, 5))

        self.new_header_default_entry = tk.Entry(root, font=("Arial", 11))
        self.new_header_default_entry.pack(pady=(0, 5))

        self.add_header_button = tk.Button(root, text="Add Header", command=self.add_new_header, font=("Arial", 12))
        self.add_header_button.pack(pady=(0, 10))

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_to_json, font=("Arial", 12))
        self.convert_button.pack(pady=(0, 10))

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_file_path = file_path
            self.load_headers()

    def load_headers(self):
        df = pd.read_csv(self.csv_file_path, encoding='utf-8')
        headers = df.columns
        self.headers_listbox.delete(0, tk.END)
        for header in headers:
            self.headers_listbox.insert(tk.END, header)

        # Preselect all headers
        self.headers_listbox.selection_set(0, tk.END)

    def add_new_header(self):
        new_header = self.new_header_entry.get()
        new_header_default_value = self.new_header_default_entry.get()

        if new_header:
            # Add new header to the list of existing headers
            self.headers_listbox.insert(tk.END, new_header)

            # Update the DataFrame with the new header and default value
            df = pd.read_csv(self.csv_file_path, encoding='utf-8')
            df[new_header] = new_header_default_value

            # Save the updated DataFrame to the CSV file
            df.to_csv(self.csv_file_path, index=False, encoding='utf-8')

            # Show the updated DataFrame
            print(df)

            # Clear the input fields
            self.new_header_entry.delete(0, tk.END)
            self.new_header_default_entry.delete(0, tk.END)

    def convert_to_json(self):
        selected_headers = self.headers_listbox.curselection()
        selected_headers = [self.headers_listbox.get(index) for index in selected_headers]

        # Include any newly added custom headers
        new_header = self.new_header_entry.get()
        if new_header:
            selected_headers.append(new_header)

        df = pd.read_csv(self.csv_file_path, usecols=selected_headers, encoding='utf-8')

        # Convert DataFrame to JSON and save to file
        json_file_path = self.csv_file_path.replace(".csv", ".json")
        df.to_json(json_file_path, orient='records', lines=True, force_ascii=False)

        # Read the JSON file and write it back with proper formatting
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = file.read()

        # Replace newline characters with commas
        json_data = json_data.replace('\n', ',')

        # Add square brackets to make it a JSON array
        json_data = f'[{json_data[:-1]}]'

        # Write the updated JSON data back to the file
        with open(json_file_path, 'w', encoding='utf-8') as file:
            file.write(json_data)

        messagebox.showinfo("Conversion Complete", f"JSON file saved to:\n{json_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVtoJSONConverter(root)
    root.mainloop()
