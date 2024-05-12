import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Label, Button

class RemoveDuplicatesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Remove Duplicates from CSV")

        self.label = Label(root, text="Select a CSV file and remove duplicates based on a chosen column.")
        self.label.pack(pady=20)

        self.select_button = Button(root, text="Select CSV File", command=self.load_csv)
        self.select_button.pack(pady=10)

        self.save_button = Button(root, text="Save Cleaned CSV", command=self.save_csv)
        self.save_button.pack(pady=10)
        self.save_button.config(state=tk.DISABLED)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        self.df = pd.read_csv(file_path)
        column = simpledialog.askstring("Input", "Enter the column name for unique identifier:")
        
        if column not in self.df.columns:
            messagebox.showerror("Error", "Column not found in the CSV file.")
            return
        
        self.df = self.df.drop_duplicates(subset=[column], keep='first')
        self.save_button.config(state=tk.NORMAL)
        messagebox.showinfo("Info", "Duplicates removed. Ready to save the cleaned file.")

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv")], defaultextension=".csv")
        if not file_path:
            return

        self.df.to_csv(file_path, index=False)
        messagebox.showinfo("Info", "File saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoveDuplicatesApp(root)
    root.mainloop()
