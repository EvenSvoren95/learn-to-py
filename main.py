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
        self.display_data()

    def display_csv_data(self):
        for row_data in self.data:
            self.display_data(self.column_titles, row_data)

    def search(self, event=None):
        query = self.search_entry.get().lower()
        self.clear_displayed_rows()
        for row in self.data:
            for value in row:
                if query in value.lower():
                    self.display_data(self.column_titles, row)  # Pass column titles and row data to display_row
                    break


    def clear_displayed_rows(self):
        for widget in self.main_frame.winfo_children():
            # Get the grid information of the widget
            grid_info = widget.grid_info()

            # Only destroy the widget if it is not in the first column (column 0)
            if grid_info['column'] != 0:
                widget.destroy()
        
        # Clear the displayed_rows list
        self.displayed_rows = []

    def display_data(self, titles=None, row_data=None):
        if titles is not None and row_data is not None:
            # Display row data
            for i, value in enumerate(row_data):
                entry = ttk.Entry(self.main_frame, width=25)
                entry.insert(tk.END, value)
                entry.grid(row=i, column=1, sticky="we")

            self.displayed_rows.append(len(self.displayed_rows))  # Track the displayed row
        else:
            if not self.column_titles:  # If column titles are not loaded yet
                return

            if len(self.column_titles) < 1:  # If there are fewer than 5 column titles
                print("CSV file does not have enough columns for 5 fields")
                return

            # Create input fields for the first row
            for i, title in enumerate(self.column_titles[:10]):
                label = ttk.Label(self.main_frame, text=title, relief="ridge", borderwidth=2)
                label.grid(row=i, column=0, sticky="we")

                entry = ttk.Entry(self.main_frame, width=25)
                entry.insert(tk.END, self.data[0][i])  # Fill entry with value from first row of CSV
                entry.grid(row=i, column=1, sticky="we")



    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):
        canvas_width = min(300, event.width)
        canvas_height = min(200, event.height)
        self.canvas.config(width=canvas_width)
        self.canvas.config(height=canvas_height)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVApp(root)
    root.mainloop()

    