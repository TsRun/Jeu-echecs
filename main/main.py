import tkinter as tk
from move import Move

class Game():

    def __init__(self):

        #Window
        self.turn = "white"
        self.opposite_turn = "black"
        self.title = "ChessGame"
        self.root = tk.Tk()
        self.init_root()
        self.board_size = min(self.root.winfo_width(), self.root.winfo_height()) - 40
        self.init_canvas()
        self.actual_move = Move(root=self.root, canvas=self.canvas)
        self.actual_move.show_board()
        self.bind()
        self.root.mainloop()

    def init_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.board_size + 1, height = self.board_size + 1, bg="white")
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        self.change_size()

    def change_size(self):
        colors = ["#EFCA9C", "#B86130"]
        self.board_size = min(self.root.winfo_width(), self.root.winfo_height()) - 40
        self.canvas.config(width=self.board_size + 1, height=self.board_size + 1)
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.canvas.create_rectangle(j*self.board_size / 8, i*self.board_size / 8, (j + 1) * self.board_size / 8, (i + 1) * self.board_size / 8, fill=colors[0], tags="square")
                else:
                    self.canvas.create_rectangle(j*self.board_size / 8, i*self.board_size / 8, (j + 1) * self.board_size / 8, (i + 1) * self.board_size / 8, fill=colors[1], tags="square")

    def init_root(self):
        self.root.title(self.title)
        self.root.geometry("800x800")
        self.root.minsize(400, 400)
        self.root.update_idletasks()
        self.root.bind("<Configure>", self.resize)

    def bind(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def new_move(self, move):
        self.actual_move
        self.actual_move = move
        self.actual_move.show_board()
        situation = self.actual_move.check_checkmate()
        if situation == "CheckMate":
            print(f'{self.opposite_turn} wins')
            self.root.quit()
        if situation == "StaleMate":
            print('StaleMate, Draw')
            self.root.quit()

    def on_release(self, event):
        new_move = self.actual_move.on_release(event)
        if new_move != self.actual_move:
            self.new_move(new_move)

    def on_drag(self, event):
        self.actual_move.on_drag(event)

    def on_right_click(self, event):
        self.actual_move.on_right_click(event)

    def on_click(self, event):
        new_move = self.actual_move.on_click(event)
        if new_move != self.actual_move:
            self.new_move(new_move)

    def resize(self, event):
        self.change_size()
        self.actual_move.show_board()

Game()
