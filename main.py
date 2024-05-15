import tkinter as tk
from tkinter import ttk
import csv

class CSVApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("CSV old App")
        #test

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

        # Load CSV Data
        self.load_csv_data()

        # Displayed Rows
        self.displayed_rows = []

        # Configure Canvas Scrolling
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def load_csv_data(self):
        self.data = []
        with open("test-csv.csv", newline='', encoding='latin1') as csvfile:  # Specify encoding if needed
            csv_reader = csv.reader(csvfile, delimiter=';')  # Use semicolon as the delimiter
            headers = next(csv_reader)  # Read the first row as headers
            self.data.append(headers)  # Add headers to the data
            for row in csv_reader:
                self.data.append(row)

    def display_csv_data(self):
        headers = self.data[0]  # Get the headers from the data
        for row_data in self.data[1:]:  # Skip the first row (headers)
            self.display_row(row_data, headers=headers)

    def search(self, event=None):
        query = self.search_entry.get().lower()  # Get the search query from the entry field
        self.clear_displayed_rows()
        for row in self.data:
            for value in row:
                if query in value.lower():
                    self.display_row(row)
                    break

    def clear_displayed_rows(self):
        for row_widgets in self.displayed_rows:
            for widget in row_widgets:
                widget.destroy()
        self.displayed_rows.clear()

    def display_row(self, row_data, headers=None):
        if len(self.displayed_rows) >= 10:  # Limit to 10 displayed rows
            return
        num_columns = min(len(row_data), 200 // 100)  # Calculate the number of columns based on the canvas width
        row = len(self.displayed_rows)  # Increment the row for each row of data
        for i, value in enumerate(row_data):
            items = value.split(';')  # Split the value by commas
            for j, item in enumerate(items):
                column = j % num_columns  # Calculate the column index, wrapping around if needed
                
                # Add text label
                if headers and j < len(headers):
                    label = ttk.Label(self.main_frame, text=headers[j])
                    label.grid(row=row, column=column*2, sticky="e")  # Place label in even-numbered columns
                
                # Add input field
                entry = ttk.Entry(self.main_frame)
                entry.insert(0, item)
                entry.grid(row=row, column=column*2+1, sticky="we")  # Place input field in odd-numbered columns
            row += 1  # Move to the next row for the next set of data



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
    app.display_csv_data()
    root.mainloop()

    