import tkinter as tk

class CustomApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom App")
        self.geometry("400x300")
        
        # Add your custom widgets and logic here
        
        self.mainloop()

if __name__ == "__main__":
    app = CustomApp()
