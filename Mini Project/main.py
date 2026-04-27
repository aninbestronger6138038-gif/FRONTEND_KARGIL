from tkinter import Tk
from ui import SudokuUI

def main():
    root = Tk()
    SudokuUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()