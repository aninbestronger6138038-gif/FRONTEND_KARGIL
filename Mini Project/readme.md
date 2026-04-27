
# Sudoku Solver with Backtracking Algorithm

A professional desktop Sudoku solver built with **Python** and **Tkinter** that implements the **backtracking algorithm** for efficient puzzle solving.
Features both instant solving and **step-by-step visual solving** to demonstrate the algorithm execution.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/github/license/yourusername/sudoku-solver.svg)](LICENSE)

## ✨ **Key Features**

- **✅ Instant Sudoku Solving** - Solves any valid puzzle immediately
- **🎬 Visual Step-by-Step Solving** - Watch backtracking algorithm in action
- **🔒 Real-time Input Validation** - Invalid cells highlighted instantly  
- **⏱️ Built-in Timer** - Tracks solving time
- **🎨 Light/Dark Theme Toggle** - Professional UI theming
- **🔄 Reset & Clear Functions** - Complete puzzle management
- **📱 Locked Clue Cells** - Original puzzle numbers protected
- **🎯 Preloaded Classic Puzzle** - Ready to use immediately

## 🎮 **Demo**

| Light Theme | Dark Theme | Visual Solving |
|-------------|------------|---------------|
| ![Light Theme](screenshots/light-theme.png) | ![Dark Theme](screenshots/dark-theme.png) | ![Visual Solve](screenshots/visual-solving.gif) |

## 🛠️ **Tech Stack**
Core: Python 3.8+
GUI: Tkinter
Algorithm: Recursive Backtracking
Validation: Constraint Satisfaction
Animation: Generator + Tkinter.after()

## 🚀 **Quick Start**

```bash
# Clone the repository
git clone https://github.com/aninbestronger6138038-gif/Sudoku-Game-.git
cd sudoku-solver

# Run the application
python main.py
```

**Requirements:** Python 3.8+ (Tkinter included by default)

## 📋 **How It Works**

### **Backtracking Algorithm Flow**

Find empty cell (0)
Try numbers 1-9 in that cell
Check row/column/3x3 box validity
If valid → Place number → Recurse to next cell
If stuck → Backtrack (remove number) → Try next
Repeat until solved or no solution exists

### **Visual Mode**
Uses Python **generators** (`yield`) to emit each step:
- `"place"` - Number inserted in cell
- `"remove"` - Wrong number removed  
- `"done"` - Puzzle solved

## 🏗️ **Project Structure**
sudoku-solver/

├── main.py # Entry point & Tkinter root

├── ui.py # Complete GUI implementation

├── sudoku.py # Backtracking solver core

└── README.md # This file

<img width="828" height="350" alt="File Structure" src="https://github.com/user-attachments/assets/4efac526-8d1e-40fd-ac80-d1b50a3d548a" />



## 🎯 **Learning Outcomes**

- **Data Structures**: 2D arrays, state management
- **Algorithms**: Recursive backtracking, constraint satisfaction
- **GUI Programming**: Tkinter event handling, validation
- **Advanced Python**: Generators, `after()` animation
- **Software Design**: Modular architecture, separation of concerns

## 📊 **Algorithm Complexity**

| Operation    |     Time Complexity       |     Space Complexity |
|--------------|-------------------------  |----------------------|
| Single Solve |     O(9^n) worst case     | O(n) recursion depth |
| Validation   | O(1) per check            | O(1)                 |
| Visual Solve | Same + animation overhead | Same                 |

## 💡 **Use Cases**

- **Educational**: Visualize backtracking algorithm execution
- **Interview Prep**: Classic algorithm implementation demo
- **Portfolio**: Clean, professional GUI + algorithm project
- **Personal**: Solve Sudoku puzzles efficiently

## 🔮 **Future Enhancements**

- [ ] Sudoku puzzle generator
- [ ] More difficulty levels
- [ ] Save/Load puzzle functionality
- [ ] Leaderboard with solving times
- [ ] Advanced solvers (Dancing Links)

## 📝 **Academic Credits**

**Project Type**: Algorithm Visualization + GUI Application  
**Skills Demonstrated**: DSA, OOP, GUI Programming, Event-Driven Architecture  
**Semester**: MCA / B.Tech CSE Final Year Project

## 📄 **License**

This project is open source and available under the MIT License.

## 🙏 **Acknowledgements**

Built with ❤️ using Python's powerful standard library. Special thanks to Tkinter for reliable cross-platform GUI development.

---

⭐ **Star this repository if you found it helpful!**  
📧 **Contact**: anindita.dhar.official@gmail.com

---
