import random
import tkinter as tk
from tkinter import messagebox, font


class TicTacToe:

    def __init__(self, main_menu_instance, difficulty):
        self.difficulty = difficulty
        self.main_menu_instance = main_menu_instance
        self.game = tk.Tk()
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player = ''
        self.pc = ''
        self.turn = ''
        self.coin_toss()
        self.main_menu()

    def main_menu(self):
        self.game.title("Start Menu")
        width = 600
        height = 600
        screenwidth = self.game.winfo_screenwidth()
        screenheight = self.game.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.game.geometry(alignstr)
        self.game.resizable(width=False, height=False)

        self.start_button = tk.Button(self.game, width=100, height=100, text="Start", font=("Arial Black", 25),
                                      command=self.ui)
        self.start_button.pack(pady=20)
        self.game.mainloop()

    def coin_toss(self):
        """Function that determines what player goes first as X and what player gets 0"""
        tmp = random.randint(1, 2)
        if self.difficulty == 0:
            if tmp == 1:
                self.player = 'X'
            else:
                self.player = 'O'
        else:
            if tmp == 1:
                self.player = 'X'
                self.pc = 'O'
                self.turn = 'player'
            else:
                self.player = 'O'
                self.pc = 'X'
                self.turn = 'pc'

    def ui(self):
        """Function that creates the board and UI"""
        self.game.destroy()
        self.game = tk.Tk()
        width = 600
        height = 600
        screenwidth = self.game.winfo_screenwidth()
        screenheight = self.game.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.game.geometry(alignstr)
        self.game.resizable(width=False, height=False)

        for row in range(3):
            self.game.rowconfigure(row, weight=1, minsize=50)
            self.game.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                self.board[row][col] = tk.Button(self.game,
                                                 justify="center",
                                                 text=" ",
                                                 width=30,
                                                 font=("Arial Black", 25),
                                                 fg="red",
                                                 height=30,
                                                 command=lambda x=row, y=col: self.button(x, y))
                self.board[row][col].grid(row=row, column=col)
        if self.difficulty != 0:
            self.label = tk.Label(text="It's " + self.turn + " turn ", font=('arial', 20, 'bold'))
        else:
            self.label = tk.Label(text="It's " + self.player + " turn ", font=('arial', 20, 'bold'))
        self.label.grid(row=3, column=0, columnspan=3)
        if self.turn == 'pc':
            if self.difficulty == 1:
                self.pc1_turn()
            elif self.difficulty == 2:
                pass
            elif self.difficulty == 3:
                pass
        self.game.mainloop()

    def button(self, x, y):
        if self.board[x][y]['text'] == " " and self.difficulty == 0:
            self.board[x][y]['text'] = self.player
            if self.player == 'X':
                self.board[x][y]['fg'] = "red"
            else:
                self.board[x][y]['fg'] = "blue"
            if self.win_msg():
                pass
            else:
                self.next_player()
                self.label['text'] = ("It's " + self.player + " turn ")

        elif self.board[x][y]['text'] == " " and self.difficulty == 1:
            if self.turn == 'player':
                self.board[x][y]['text'] = self.player
                if self.win_msg():
                    pass
                else:
                    self.next_turn()
                    self.label['text'] = ("It's " + self.turn + " turn ")
            if self.player == 'X':
                self.board[x][y]['fg'] = "red"
            else:
                self.board[x][y]['fg'] = "blue"
            if self.turn == 'pc':
                self.pc1_turn()


        elif self.board[x][y]['text'] == " " and self.difficulty == 2:
            pass

        elif self.board[x][y]['text'] == " " and self.difficulty == 3:
            pass

    def pc1_turn(self):
        tmp = False
        while not tmp:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if self.board[x][y]['text'] == ' ':
                self.board[x][y]['text'] = self.pc
                if self.pc == 'X':
                    self.board[x][y]['fg'] = "red"
                else:
                    self.board[x][y]['fg'] = "blue"
                tmp = True
        if not self.win_msg():
            self.next_turn()
            self.label['text'] = ("It's " + self.turn + " turn ")

    def check_winner(self):
        """Function that checks the board for a winner. It checks colons, rows and diagonals and returns False if
        there are still moves to make and no winners, True if there is a winner"""
        # Check Rows
        for row in self.board:
            if row[0]['text'] == row[1]['text'] == row[2]['text'] != " ":
                return True

        # Check Cols
        for col in range(3):
            if self.board[0][col]['text'] == self.board[1][col]['text'] == self.board[2][col]['text'] != " ":
                return True

        # Check Diagonals
        if (
                self.board[0][0]['text'] == self.board[1][1]['text'] == self.board[2][2]['text'] != " "
                or self.board[0][2]['text'] == self.board[1][1]['text'] == self.board[2][0]['text'] != " "
        ):
            return True

        # No Winners
        return False

    def check_draw(self):
        """Function that checks for a draw"""
        for row in self.board:
            for btn in row:
                if " " in btn['text']:
                    return False
        return True

    def win_msg(self):
        if self.check_winner():
            if self.difficulty == 0:
                messagebox.showinfo("Tic Tac Toe ", "Player {} wins!".format(self.player))
            else:
                messagebox.showinfo("Tic Tac Toe ", "{} wins!".format(self.turn))
            self.game.quit()
            self.game.destroy()
            self.main_menu_instance.menu()
        elif self.check_draw():
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            self.game.quit()
            self.game.destroy()
            self.main_menu_instance.menu()
        else:
            return False

    def next_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

    def next_turn(self):
        if self.turn == 'pc':
            self.turn = 'player'
        else:
            self.turn = 'pc'
