from tkinter import Tk, Label, Button, messagebox, Frame
from minesweeper import Minesweeper  # Import your Minesweeper class from the GUI file
import time

global game, flag_mode


def on_key_press(event):
    if event.char == 'f' or event.char == 'F':
        toggle_flag_mode()


def toggle_flag_mode():
    global flag_mode
    flag_mode = not flag_mode


def click_cell(row, col):
    global game, flag_mode
    if flag_mode:
        game.flag(col, row)
        update_gui()
    else:
        if game.ref_board[col][row] == 'B':
            game.in_game = False
            game.check_win()
            update_gui()  # Update GUI to show the bomb that was clicked
            messagebox.showinfo("Oops!", "You clicked on a bomb! Game Over!")
            if restart_game():
                window.destroy()
                main_gui()
            window.destroy()
        else:
            game.fill_in_board()
            game.propagate_click(col, row)
            game.fill_in_board()
            game.win = game.check_win()
            update_gui()  # Update GUI after cell click


def update_gui():
    color_map = {
        '1': 'blue',
        '2': 'green',
        '3': 'red',
        '4': 'purple',
        '5': 'maroon',
        '6': 'turquoise',
        '7': 'black',
        '8': 'grey',
    }
    for row in range(game.size):
        for col in range(game.size):
            cell_state = game.board[col][row]
            if cell_state == 'F':
                buttons[row][col].config(text="F", fg="red")  # Red color for flagged cells
            elif cell_state == '*':
                buttons[row][col].config(text="*", fg="black")  # Black color for hidden cells
            else:
                if cell_state == '0':
                    buttons[row][col].config(text=" ", fg="grey")  # Grey color for empty revealed cells
                else:
                    text_color = color_map.get(cell_state, "blue")  # Default to blue for unknown numbers
                    buttons[row][col].config(text=cell_state, fg=text_color)  # Assign color based on number


def restart_game():
    result = messagebox.askyesno("Restart Game", "Do you want to restart the game?")
    if result:
        window.destroy()
        main_gui()
        print("Restarting game...")
    else:
        messagebox.showinfo("Sad to see you go!", "See you next time!")
        window.destroy()


def main_gui():
    global game, buttons, flag_mode, window
    game = Minesweeper(difficulty=1)
    flag_mode = False

    window = Tk()
    window.title("Minesweeper")
    window.resizable(False, False)
    window.bind("<Key>", on_key_press)

    frame = Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")

    timer_label = Label(window, text="Time: 0 seconds", font=("Arial", 12))
    timer_label.grid(row=game.size, columnspan=game.size)

    buttons = []
    start_time = time.time()  # Start time when the game begins

    def update_timer():
        elapsed_time = int(time.time() - start_time)
        timer_label.config(text=f"Time: {elapsed_time} seconds")
        window.after(1000, update_timer)  # Update the timer label every 1 second

    update_timer()

    bomb_label = Label(window, text=f"Bombs: {game.nbombs}")
    bomb_label.grid(row=game.size + 1, column=0, columnspan=game.size)

    for row in range(game.size):
        button_row = []
        for col in range(game.size):
            button = Button(window, width=3, height=1, command=lambda r=row, c=col: click_cell(r, c))
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons.append(button_row)

    update_gui()
    window.mainloop()


if __name__ == '__main__':
    main_gui()
