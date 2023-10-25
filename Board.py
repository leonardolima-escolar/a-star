import tkinter as tk


class Board:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title("A Star")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.change_square_state)
        self.run_button = tk.Button(self.root, text="Run", command=self.run_star)
        self.run_button.pack(side="right")
        self.goal_button = tk.Button(self.root, text="Goal", command=self.set_goal)
        self.goal_button.pack(side="left")
        self.start_button = tk.Button(self.root, text="Start", command=self.set_start)
        self.start_button.pack(side="left")
        self.default_button = tk.Button(
            self.root, text="Wall", command=self.set_default
        )
        self.default_button.pack(side="left")
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        self.reset_button.pack(side="right")
        self.grid_size = 10
        self.update_grid()
        self.selected_state = None
        self.start = None
        self.goal = None

    def set_goal(self):
        self.selected_state = "goal"

    def set_start(self):
        self.selected_state = "start"

    def set_default(self):
        self.selected_state = None

    def update_grid(self):
        self.canvas.delete("grid")
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                square = self.board.get_square((x, y))
                if square:
                    if square.state == "goal":
                        color = "green"
                    elif square.state == "start":
                        color = "red"
                    elif square.state == "wall":
                        color = "black"
                    elif square.state == "path":
                        color = "blue"
                    else:
                        color = "white"
                    self.canvas.create_rectangle(
                        x * 40,
                        y * 40,
                        (x + 1) * 40,
                        (y + 1) * 40,
                        fill=color,
                        outline="black",
                        tags="grid",
                    )
                    if square.f > 0:
                        font_size = 10
                        self.canvas.create_text(
                            (x + 0.5) * 40,
                            (y + 0.25) * 40,
                            text=f"F:{square.f}",
                            fill="black",
                            font=("Helvetica", font_size),
                        )
                        self.canvas.create_text(
                            (x + 0.5) * 40,
                            (y + 0.55) * 40,
                            text=f"G:{square.g}",
                            fill="black",
                            font=("Helvetica", font_size),
                        )
                        self.canvas.create_text(
                            (x + 0.5) * 40,
                            (y + 0.9) * 40,
                            text=f"H:{square.h}",
                            fill="black",
                            font=("Helvetica", font_size),
                        )

    def change_square_state(self, event):
        x, y = event.x // 40, event.y // 40
        square = self.board.get_square((x, y))
        if square:
            if self.selected_state == "goal":
                if self.goal:
                    old_square = self.board.get_square(self.goal)
                    old_square.state = "empty"
                    old_square.f = 0
                    old_square.g = 0
                    old_square.h = 0
                    old_square.parent = None
                    # self.board.get_square(self.goal).state = "empty"
                self.goal = (x, y)
                square.state = "goal"
                if square.f > 0:
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
            elif self.selected_state == "start":
                if self.start:
                    old_square = self.board.get_square(self.start)
                    old_square.state = "empty"
                    old_square.f = 0
                    old_square.g = 0
                    old_square.h = 0
                    old_square.parent = None
                    # self.board.get_square(self.start).state = "empty"
                self.start = (x, y)
                square.state = "start"
                if square.f > 0:
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
            else:
                if square.state == "wall":
                    square.state = "empty"
                elif square.state == "empty":
                    square.state = "wall"
                elif square.state == "path":
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
                elif square.state == "goal":
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
                    self.goal = None
                elif square.state == "start":
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
                    self.start = None
                # if square.state == "wall" or square.state == "path":
                #     square.state = "empty"
                # else:
                #     square.state = "wall"
            self.update_grid()

    def run_star(self):
        self.clear_grid_except_start_goal()

        self.update_grid()
        if self.start is not None and self.goal is not None:
            path_found = self.board.execute_a_star(self.start, self.goal)

            if path_found:
                path = self.board.build_path_from_goal(self.goal)
                self.highlight_path_on_grid(path)
            else:
                self.update_grid()
                print("Nenhum caminho encontrado.")

    def clear_grid_except_start_goal(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                square = self.board.get_square((x, y))
                if (
                    square
                    and square.state != "start"
                    and square.state != "goal"
                    and square.state != "wall"
                ):
                    square.state = "empty"
                    square.f = 0
                    square.g = 0
                    square.h = 0
                    square.parent = None
        self.update_grid()

    def highlight_path_on_grid(self, path):
        for x, y in path:
            square = self.board.get_square((x, y))
            if square and square.state != "goal" and square.state != "start":
                square.state = "path"
        self.update_grid()

    def reset_board(self):
        self.board.reset_to_initial_state()
        self.goal = None
        self.start = None
        self.selected_state = None
        self.update_grid()

    def render(self):
        self.root.mainloop()
