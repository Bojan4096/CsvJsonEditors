import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Label, Button

class AverageCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculate Average for Duplicate Entries")

        self.label = Label(root, text="Select a CSV file, specify a matching column and a property to calculate the average.")
        self.label.pack(pady=20)

        self.select_button = Button(root, text="Select CSV File", command=self.load_csv)
        self.select_button.pack(pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        df = pd.read_csv(file_path)
        match_column = simpledialog.askstring("Input", "Enter the column name for matching:")
        if match_column not in df.columns:
            messagebox.showerror("Error", "Matching column not found in the CSV file.")
            return
        
        calculate_column = simpledialog.askstring("Input", "Enter the column name to calculate average:")
        if calculate_column not in df.columns:
            messagebox.showerror("Error", "Property column not found in the CSV file.")
            return

        # Group by the matching column and calculate the average for the calculate column
        result_df = df.groupby(match_column, as_index=False)[calculate_column].mean()

        # Save the result to a new CSV file
        save_path = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv")], defaultextension=".csv")
        if not save_path:
            return
        
        result_df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"File saved successfully to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AverageCalculatorApp(root)
    root.mainloop()
