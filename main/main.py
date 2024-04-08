import tkinter as tk
from PIL import Image, ImageTk
from move import Move
from utils import *

class Game():

    def __init__(self):

        #Window
        self.turn = "white"
        self.opposite_turn = "black"
        self.title = "ChessGame"
        self.root = tk.Tk()
        self.init_root()
        self.actual_move = Move(root=self.root)
        self.bind()
        self.root.mainloop()

    def init_root(self):
        self.root.title(self.title)
        self.root.geometry("800x800")
        self.root.minsize(400, 400)
        self.root.update_idletasks()
        self.root.bind("<Configure>", self.resize)

    def bind(self):
        situation = self.actual_move.check_checkmate()
        if situation == "CheckMate":
            print(f'{self.opposite_turn} wins')
            self.root.quit()
        if situation == "StaleMate":
            print(f'StaleMate, Draw')
            self.root.quit()
        self.actual_move.show_board()
        self.actual_move.board.canvas.bind("<Button-1>", self.on_click)
        self.actual_move.board.canvas.bind("<B1-Motion>", self.actual_move.on_drag)
        self.actual_move.board.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_release(self, event):
        new_move = self.actual_move.on_release(event)
        if new_move != self.actual_move:
            self.actual_move = new_move
            self.bind()

    def on_click(self, event):
        new_move = self.actual_move.on_click(event)
        if new_move != self.actual_move:
            self.actual_move = new_move
            self.bind()


    def resize(self, event):
        self.actual_move.show_board()
        size = min(event.width, event.height)

Game()
