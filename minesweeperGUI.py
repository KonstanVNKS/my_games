from tkinter import Tk, Label, Button
from minesweeper import Minesweeper  # Import your Minesweeper class from the GUI file

def main(difficulty):
    global game, flag_mode

    def toggle_flag_mode():
        global flag_mode
        flag_mode = not flag_mode

    def click_cell(row, col):
        global game, flag_mode
        if flag_mode:
            game.flag(col, row)
        else:
            line = chr(ord('A') + row)
            if game.ref_board[col][line] == 'B':
                game.in_game = False
            else:
                game.fill_in_board()
            game.propagate_click(col, line)
            game.fill_in_board()
            game.win = game.check_win()
        update_gui()

    def update_gui():
        for row in range(game.size):
            for col in range(game.size):
                cell_button = Button(window, width=3, height=1)
                cell_button.grid(row=row, column=col)
                cell_state = game.board[col][row]
                if cell_state == 'F':
                    cell_button.config(text="F")
                elif cell_state == '*':
                    cell_button.config(text="*")
                else:
                    if cell_state != 'B':
                        cell_button.config(text=cell_state)
                    else:
                        cell_button.config(text=" ")

    flag_mode = False
    game = Minesweeper(difficulty=difficulty)

    window = Tk()
    window.title("Minesweeper")

    for row in range(game.size):
        for col in range(game.size):
            cell_button = Button(window, text=" ", width=3, height=1,
                                 command=lambda r=row, c=col: click_cell(r, c))
            cell_button.grid(row=row, column=col)

    status_label = Label(window, text="Game Status: In Progress")
    status_label.grid(row=game.size + 1, columnspan=game.size)

    update_gui()

    window.mainloop()


if __name__ == '__main__':
    print("#######################")
    print("Welcome to Minesweeper!")
    print("#######################")
    diff = int(input("Choose your difficulty (0 = easy , 1 = normal, 2 = hard): "))
    main(diff)
