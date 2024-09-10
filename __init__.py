import tkinter as tk

from Controller.controller import Controller
from Model.view_model import ViewModel
from View.ui import View

def main():
    root = tk.Tk()

    model = ViewModel()
    controller = Controller(model, None)
    view = View(root, controller)
    controller.view = view

    root.mainloop()

if __name__ == "__main__":
    main()