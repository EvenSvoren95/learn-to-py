import tkinter as tk
from tkinter import ttk
import csv

class CSVApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("The big search engine")

        # Displayed Rows
        self.displayed_rows = []

        # Create Canvas with Scrollbar
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create Frame inside Canvas
        self.main_frame = ttk.Frame(self.canvas, padding="10")
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Search Entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.root, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.search_entry.bind("<Return>", self.search)

        # Load and display CSV data
        self.load_and_display_csv_data()

        # Configure Canvas Scrolling
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def load_and_display_csv_data(self):
        # Load CSV data
        self.data = []
        with open("test-csv.csv", newline='', encoding='latin1') as csvfile:  # Specify encoding if needed
            csv_reader = csv.reader(csvfile, delimiter=';')  # Use semicolon as the delimiter
            self.column_titles = next(csv_reader)  # Read the first row containing the column titles
            for row in csv_reader:
                self.data.append(row)

        # Display CSV data
        self.display_first_row()

    def display_csv_data(self):
        for row_data in self.data:
            self.display_row(self.column_titles, row_data)

    def search(self, event=None):
        query = self.search_entry.get().lower()
        self.clear_displayed_rows()
        for row in self.data:
            for value in row:
                if query in value.lower():
                    self.display_row(self.column_titles, row)  # Pass column titles and row data to display_row
                    break


    def clear_displayed_rows(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.displayed_rows = []

    def display_first_row(self):
        if not self.column_titles:  # If column titles are not loaded yet
            return

        if len(self.column_titles) < 5:  # If there are fewer than 5 column titles
            print("CSV file does not have enough columns for 5 fields")
            return

        for i in range(5):  # Create 5 input fields
            label = ttk.Label(self.main_frame, text=self.column_titles[i], relief="ridge", borderwidth=2)
            label.grid(row=i, column=0, sticky="we")

            entry = ttk.Entry(self.main_frame, width=25)
            entry.insert(tk.END, self.data[0][i])  # Fill entry with value from first row of CSV
            entry.grid(row=i, column=1, sticky="we")

    def display_row(self, titles, row_data):
        if len(self.displayed_rows) >= 10:  # Limit to 10 displayed rows
            return
        row = len(self.displayed_rows)  # Increment the row for each row of data

        # Add title labels
        for i, title in enumerate(titles):
            label = ttk.Label(self.main_frame, text=title, relief="ridge", borderwidth=2)
            label.grid(row=i, column=0, sticky="we")

        # Display row data
        for i, value in enumerate(row_data):
            entry = ttk.Entry(self.main_frame, width=25)
            label = ttk.Label(self.main_frame, text=value, relief="ridge", borderwidth=2)
            entry.insert(tk.END, value)
            entry.grid(row=i, column=1, sticky="we")  # Adjust column index to start from 1

        self.displayed_rows.append(row)  # Track the displayed row




    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):
        canvas_width = min(300, event.width)
        canvas_height = min(150, event.height)
        self.canvas.config(width=canvas_width)
        self.canvas.config(height=canvas_height)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVApp(root)
    root.mainloop()

    