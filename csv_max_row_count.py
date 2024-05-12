import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Label, Button

class MaxColumnValueCountApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Find Maximum Repetition in a Specified Column")

        self.label = Label(root, text="Select a CSV file and specify a column to see the value and its maximum count.")
        self.label.pack(pady=20)

        self.select_button = Button(root, text="Select CSV File", command=self.load_csv)
        self.select_button.pack(pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        self.df = pd.read_csv(file_path)
        column_name = simpledialog.askstring("Input", "Enter the column name to check for repetitions:")
        
        if column_name not in self.df.columns:
            messagebox.showerror("Error", "Column not found in the CSV file.")
            return
        
        value_counts = self.df[column_name].value_counts()
        max_count = value_counts.max()
        most_frequent_values = ""
        if max_count > 2:
            most_frequent_values = value_counts[value_counts == max_count].index.tolist()

        info_message = f"The value(s) '{', '.join(most_frequent_values)}' in '{column_name}' is/are repeated {max_count} times."
        messagebox.showinfo("Result", info_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MaxColumnValueCountApp(root)
    root.mainloop()
