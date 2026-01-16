"""
Tourism Data Collector
Tkinter-based Windows application with auto AI download
"""
import tkinter as tk
from ui.main_window import TourismApp

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = TourismApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
