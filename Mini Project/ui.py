import tkinter as tk
from tkinter import messagebox
from sudoku import solve, solve_steps, is_valid


class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Sudoku Solver")
        self.root.geometry("700x820")
        self.root.resizable(False, False)

        self.entries = []
        self.original_cells = set()
        self.initial_puzzle = [[0 for _ in range(9)] for _ in range(9)]
        self.timer_seconds = 0
        self.timer_running = False
        self.visualizing = False
        self.step_generator = None

        self.themes = {
            "light": {
                "window_bg": "#eef2ff",
                "panel_bg": "#e0e7ff",
                "board_bg": "#c7d2fe",
                "box1": "#ffffff",
                "box2": "#eaf2ff",
                "text": "#111827",
                "subtext": "#4b5563",
                "title": "#1f2937",
                "invalid": "#ffd6d6",
                "solved_fg": "#1d4ed8",
                "status_bg": "#dbeafe",
                "status_fg": "#1e3a8a",
                "timer_bg": "#ede9fe",
                "timer_fg": "#5b21b6",
                "button_text": "#ffffff",
                "fixed_fg": "#000000"
            },
            "dark": {
                "window_bg": "#111827",
                "panel_bg": "#1f2937",
                "board_bg": "#374151",
                "box1": "#1f2937",
                "box2": "#243244",
                "text": "#f9fafb",
                "subtext": "#d1d5db",
                "title": "#f3f4f6",
                "invalid": "#7f1d1d",
                "solved_fg": "#60a5fa",
                "status_bg": "#1e3a8a",
                "status_fg": "#dbeafe",
                "timer_bg": "#312e81",
                "timer_fg": "#e9d5ff",
                "button_text": "#ffffff",
                "fixed_fg": "#f9fafb"
            }
        }

        self.button_colors = {
            "solve": ("#16a34a", "#15803d"),
            "visual": ("#7c3aed", "#6d28d9"),
            "clear": ("#dc2626", "#b91c1c"),
            "reset": ("#ea580c", "#c2410c"),
            "sample": ("#2563eb", "#1d4ed8"),
            "theme": ("#475569", "#334155")
        }

        self.current_theme = "light"
        self.apply_theme()
        self.build_layout()
        self.start_timer()

        # Load a classic puzzle automatically at startup
        self.load_classic_puzzle()

    def apply_theme(self):
        self.colors = self.themes[self.current_theme]

    def build_layout(self):
        self.root.configure(bg=self.colors["window_bg"])

        self.title_label = tk.Label(
            self.root,
            text="Sudoku Solver using Backtracking",
            font=("Arial", 22, "bold"),
            bg=self.colors["window_bg"],
            fg=self.colors["title"]
        )
        self.title_label.pack(pady=(18, 6))

        self.top_info_frame = tk.Frame(self.root, bg=self.colors["window_bg"])
        self.top_info_frame.pack(pady=6)

        self.timer_label = tk.Label(
            self.top_info_frame,
            text="Time: 00:00",
            font=("Arial", 12, "bold"),
            bg=self.colors["timer_bg"],
            fg=self.colors["timer_fg"],
            padx=14,
            pady=8
        )
        self.timer_label.grid(row=0, column=0, padx=8)

        self.status_label = tk.Label(
            self.top_info_frame,
            text="Status: Ready",
            font=("Arial", 12, "bold"),
            bg=self.colors["status_bg"],
            fg=self.colors["status_fg"],
            padx=14,
            pady=8
        )
        self.status_label.grid(row=0, column=1, padx=8)

        self.theme_button = tk.Button(
            self.top_info_frame,
            text="Toggle Theme",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.toggle_theme
        )
        self.style_button(self.theme_button, *self.button_colors["theme"])
        self.theme_button.grid(row=0, column=2, padx=8)

        self.board_frame = tk.Frame(
            self.root,
            bg=self.colors["board_bg"],
            bd=3,
            relief="ridge"
        )
        self.board_frame.pack(pady=18)

        self.vcmd = (self.root.register(self.validate_input), "%P")
        self.create_grid()

        self.button_frame = tk.Frame(self.root, bg=self.colors["window_bg"])
        self.button_frame.pack(pady=16)

        self.solve_btn = tk.Button(
            self.button_frame,
            text="Solve Instantly",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.solve_sudoku
        )
        self.style_button(self.solve_btn, *self.button_colors["solve"])
        self.solve_btn.grid(row=0, column=0, padx=8, pady=8)

        self.visual_btn = tk.Button(
            self.button_frame,
            text="Visual Solve",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.start_visual_solve
        )
        self.style_button(self.visual_btn, *self.button_colors["visual"])
        self.visual_btn.grid(row=0, column=1, padx=8, pady=8)

        self.sample_btn = tk.Button(
            self.button_frame,
            text="Load Puzzle",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.load_classic_puzzle
        )
        self.style_button(self.sample_btn, *self.button_colors["sample"])
        self.sample_btn.grid(row=0, column=2, padx=8, pady=8)

        self.reset_btn = tk.Button(
            self.button_frame,
            text="Reset",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.reset_puzzle
        )
        self.style_button(self.reset_btn, *self.button_colors["reset"])
        self.reset_btn.grid(row=1, column=0, padx=8, pady=8)

        self.clear_btn = tk.Button(
            self.button_frame,
            text="Clear",
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.clear_grid
        )
        self.style_button(self.clear_btn, *self.button_colors["clear"])
        self.clear_btn.grid(row=1, column=1, padx=8, pady=8)

        self.info_label = tk.Label(
            self.root,
            text="Classic puzzle loads automatically. Fixed clue cells are locked. Invalid cells highlight live. Use Visual Solve to watch backtracking.",
            font=("Arial", 11),
            bg=self.colors["window_bg"],
            fg=self.colors["subtext"],
            wraplength=620,
            justify="center"
        )
        self.info_label.pack(pady=(8, 14))

    def style_button(self, button, normal_color, hover_color):
        button.configure(
            bg=normal_color,
            fg=self.colors["button_text"],
            activebackground=hover_color,
            activeforeground=self.colors["button_text"]
        )
        button.bind("<Enter>", lambda e, b=button, c=hover_color: b.config(bg=c))
        button.bind("<Leave>", lambda e, b=button, c=normal_color: b.config(bg=c))

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.refresh_theme()

    def refresh_theme(self):
        self.root.configure(bg=self.colors["window_bg"])
        self.title_label.config(bg=self.colors["window_bg"], fg=self.colors["title"])
        self.top_info_frame.config(bg=self.colors["window_bg"])
        self.button_frame.config(bg=self.colors["window_bg"])
        self.info_label.config(bg=self.colors["window_bg"], fg=self.colors["subtext"])
        self.board_frame.config(bg=self.colors["board_bg"])

        self.timer_label.config(bg=self.colors["timer_bg"], fg=self.colors["timer_fg"])
        self.status_label.config(bg=self.colors["status_bg"], fg=self.colors["status_fg"])

        self.style_button(self.theme_button, *self.button_colors["theme"])
        self.style_button(self.solve_btn, *self.button_colors["solve"])
        self.style_button(self.visual_btn, *self.button_colors["visual"])
        self.style_button(self.sample_btn, *self.button_colors["sample"])
        self.style_button(self.reset_btn, *self.button_colors["reset"])
        self.style_button(self.clear_btn, *self.button_colors["clear"])

        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.config(
                    bg=self.get_box_color(row, col),
                    fg=self.colors["text"],
                    insertbackground=self.colors["text"],
                    disabledforeground=self.colors["fixed_fg"],
                    disabledbackground=self.get_box_color(row, col)
                )

        self.highlight_invalid_cells()
        self.reapply_text_colors()

    def validate_input(self, value):
        if value == "":
            return True
        return len(value) == 1 and value in "123456789"

    def get_box_color(self, row, col):
        return self.colors["box1"] if (row // 3 + col // 3) % 2 == 0 else self.colors["box2"]

    def create_grid(self):
        for row in range(9):
            row_entries = []
            for col in range(9):
                entry = tk.Entry(
                    self.board_frame,
                    width=2,
                    font=("Arial", 20, "bold"),
                    justify="center",
                    bd=1,
                    relief="solid",
                    bg=self.get_box_color(row, col),
                    fg=self.colors["text"],
                    insertbackground=self.colors["text"],
                    disabledforeground=self.colors["fixed_fg"],
                    disabledbackground=self.get_box_color(row, col),
                    validate="key",
                    validatecommand=self.vcmd
                )

                entry.bind("<KeyRelease>", lambda event: self.on_cell_change())

                padx = (1, 1)
                pady = (1, 1)

                if col in [0, 3, 6]:
                    padx = (3, 1)
                if row in [0, 3, 6]:
                    pady = (3, 1)
                if col == 8:
                    padx = (1, 3)
                if row == 8:
                    pady = (1, 3)

                entry.grid(row=row, column=col, padx=padx, pady=pady, ipadx=10, ipady=10)
                row_entries.append(entry)

            self.entries.append(row_entries)

    def on_cell_change(self):
        self.highlight_invalid_cells()
        self.update_status("Editing puzzle...")

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.entries[row][col].get().strip()
                current_row.append(int(value) if value else 0)
            board.append(current_row)
        return board

    def save_initial_puzzle(self, board):
        self.initial_puzzle = [row[:] for row in board]

    def mark_original_cells(self):
        self.original_cells.clear()
        for row in range(9):
            for col in range(9):
                if self.entries[row][col].get().strip():
                    self.original_cells.add((row, col))

    def lock_prefilled_cells(self):
        for row in range(9):
            for col in range(9):
                if (row, col) in self.original_cells:
                    self.entries[row][col].config(state="disabled")
                else:
                    self.entries[row][col].config(state="normal")

    def unlock_all_cells(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].config(state="normal")

    def reapply_text_colors(self):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                state = entry.cget("state")
                value = entry.get().strip()

                if value:
                    if (row, col) in self.original_cells:
                        if state == "disabled":
                            entry.config(
                                disabledforeground=self.colors["fixed_fg"],
                                disabledbackground=self.get_box_color(row, col)
                            )
                        else:
                            entry.config(fg=self.colors["fixed_fg"])
                    else:
                        entry.config(fg=self.colors["solved_fg"])
                else:
                    if state == "normal":
                        entry.config(fg=self.colors["text"])

    def update_grid(self, board):
        self.unlock_all_cells()

        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)

                if board[row][col] != 0:
                    entry.insert(0, str(board[row][col]))

        self.highlight_invalid_cells()
        self.reapply_text_colors()
        self.lock_prefilled_cells()

    def reset_cell_colors(self):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                current_state = entry.cget("state")
                if current_state == "disabled":
                    entry.config(state="normal")
                    entry.config(bg=self.get_box_color(row, col))
                    entry.config(state="disabled")
                else:
                    entry.config(bg=self.get_box_color(row, col))

    def highlight_invalid_cells(self):
        board = self.get_board()
        self.reset_cell_colors()

        for row in range(9):
            for col in range(9):
                value = board[row][col]
                if value != 0 and not is_valid(board, row, col, value):
                    entry = self.entries[row][col]
                    current_state = entry.cget("state")

                    if current_state == "disabled":
                        entry.config(state="normal")
                        entry.config(bg=self.colors["invalid"])
                        entry.config(state="disabled")
                    else:
                        entry.config(bg=self.colors["invalid"])

    def puzzle_has_invalid_cells(self):
        board = self.get_board()
        for row in range(9):
            for col in range(9):
                value = board[row][col]
                if value != 0 and not is_valid(board, row, col, value):
                    return True
        return False

    def update_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
            self.timer_seconds += 1

        self.root.after(1000, self.update_timer)

    def reset_timer(self):
        self.timer_seconds = 0
        self.timer_label.config(text="Time: 00:00")

    def solve_sudoku(self):
        if self.visualizing:
            return

        self.highlight_invalid_cells()
        if self.puzzle_has_invalid_cells():
            self.update_status("Fix invalid cells first")
            messagebox.showerror("Invalid Puzzle", "Please fix highlighted cells before solving.")
            return

        board = self.get_board()
        self.save_initial_puzzle(board)

        board_copy = [row[:] for row in board]
        self.update_status("Solving instantly...")

        if solve(board_copy):
            self.update_grid(board_copy)
            self.update_status("Solved successfully")
            messagebox.showinfo("Solved", "Sudoku solved successfully!")
        else:
            self.update_status("No solution found")
            messagebox.showerror("No Solution", "No valid solution exists.")

    def start_visual_solve(self):
        if self.visualizing:
            return

        self.highlight_invalid_cells()
        if self.puzzle_has_invalid_cells():
            self.update_status("Fix invalid cells first")
            messagebox.showerror("Invalid Puzzle", "Please fix highlighted cells before visual solve.")
            return

        board = self.get_board()
        self.save_initial_puzzle(board)

        self.visualizing = True
        self.step_generator = solve_steps(board)
        self.update_status("Visual solving in progress...")
        self.run_next_step()

    def run_next_step(self):
        try:
            action, row, col, value = next(self.step_generator)

            if action == "place":
                self.entries[row][col].config(state="normal")
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(value))
                if (row, col) not in self.original_cells:
                    self.entries[row][col].config(fg=self.colors["solved_fg"])

            elif action == "remove":
                self.entries[row][col].config(state="normal")
                self.entries[row][col].delete(0, tk.END)

            elif action == "done":
                self.visualizing = False
                self.highlight_invalid_cells()
                self.reapply_text_colors()
                self.lock_prefilled_cells()
                self.update_status("Visual solve complete")
                messagebox.showinfo("Solved", "Step-by-step solving completed!")
                return

            self.highlight_invalid_cells()
            self.reapply_text_colors()
            self.root.after(50, self.run_next_step)

        except StopIteration:
            self.visualizing = False
            self.highlight_invalid_cells()
            self.reapply_text_colors()
            self.lock_prefilled_cells()
            self.update_status("Visualization finished")

    def clear_grid_without_resetting_timer(self):
        self.unlock_all_cells()

        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)
                entry.config(
                    bg=self.get_box_color(row, col),
                    fg=self.colors["text"],
                    insertbackground=self.colors["text"],
                    disabledforeground=self.colors["fixed_fg"],
                    disabledbackground=self.get_box_color(row, col)
                )

        self.original_cells.clear()

    def clear_grid(self):
        if self.visualizing:
            return

        self.clear_grid_without_resetting_timer()
        self.initial_puzzle = [[0 for _ in range(9)] for _ in range(9)]
        self.reset_timer()
        self.update_status("Board cleared")

    def reset_puzzle(self):
        if self.visualizing:
            return

        self.clear_grid_without_resetting_timer()

        for row in range(9):
            for col in range(9):
                if self.initial_puzzle[row][col] != 0:
                    self.entries[row][col].insert(0, str(self.initial_puzzle[row][col]))

        self.mark_original_cells()
        self.highlight_invalid_cells()
        self.reapply_text_colors()
        self.lock_prefilled_cells()
        self.update_status("Puzzle reset to initial state")

    def load_classic_puzzle(self):
        if self.visualizing:
            return

        puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        self.clear_grid_without_resetting_timer()

        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                value = puzzle[row][col]

                entry.config(state="normal")
                entry.delete(0, tk.END)

                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(
                        fg=self.colors["fixed_fg"],
                        disabledforeground=self.colors["fixed_fg"],
                        disabledbackground=self.get_box_color(row, col)
                    )

        self.mark_original_cells()
        self.save_initial_puzzle(puzzle)
        self.highlight_invalid_cells()
        self.reapply_text_colors()
        self.lock_prefilled_cells()
        self.reset_timer()
        self.update_status("Classic puzzle loaded")