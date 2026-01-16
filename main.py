"""
Tourism Data Collector
A comprehensive Windows application for collecting and validating tourism data across India
Built with Tkinter UI and lightweight AI model
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
