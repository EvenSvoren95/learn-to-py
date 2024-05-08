import tkinter as tk
from tkinter import ttk
import csv

class CSVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data App")
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
        self.search_entry.bind("<KeyRelease>", self.search)

        # Load CSV Data
        self.load_csv_data()

        # Displayed Rows
        self.displayed_rows = []

        # Configure Canvas Scrolling
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def load_csv_data(self):
        self.data = []
        with open("kontaktlistexxl.csv", newline='', encoding='latin1') as csvfile:  # Specify encoding if needed
            csv_reader = csv.reader(csvfile, delimiter=',')  # Use semicolon as the delimiter
            for row in csv_reader:
                self.data.append(row)

    def search(self, event=None):
        query = self.search_var.get().lower()
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

    def display_row(self, row_data):
        if len(self.displayed_rows) >= 10:  # Limit to 10 displayed rows
            return
        row_widgets = []
        for i, value in enumerate(row_data):
            items = value.split(',')  # Split the value by commas
            for j, item in enumerate(items):
                label = ttk.Label(self.main_frame, text=item)
                label.grid(row=len(self.displayed_rows) + j, column=i, sticky="w")
                row_widgets.append(label)
        self.displayed_rows.append(row_widgets)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):
        canvas_width = min(600, event.width)
        self.canvas.config(width=canvas_width)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVApp(root)
    root.mainloop()