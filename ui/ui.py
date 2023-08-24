import tkinter as tk
import random

# Function to handle square click event
def square_clicked(row, column):
    print(f"Square clicked: {row}, {column}")

def code_square_clicked(column):
    print(f"code square: {column} clicked")

def submit_clicked():
    print(f"submit clicked")

def square_focused(sq_id:'dict[str,str]', event):
    square_group = sq_id['square_group']
    row = sq_id['row']
    column = sq_id['column']

    print(f'square in {square_group}, row: {row},\
           column: {column}  {event.widget} focused')

# Create the main window
window = tk.Tk()
window.title("Crack the Code")
window.geometry("450x500")

# Create the grid of squares
squares_frame = tk.Frame(window)
squares_frame.pack()

squares = []
tot_rows, tot_columns = 5, 3
for i in range(tot_rows):
    row = []
    rule_labl = tk.Label(squares_frame, width=20, height=2)
    rule_labl.configure(text='3 correct 1 correctly placed')

    for j in range(tot_columns):
        square = tk.Button(squares_frame, width=5, height=2, bg="white")
        square.grid(row=i, column=j, padx=5, pady=5)
        square["text"] = random.randint(1, 9)  # Set random number
        square["command"] = lambda r=i, c=j: square_clicked(r, c)  # Bind click event
        square_id = {'square_group':'problem_squares',
                     'row' : i,
                     'column' : j}
        square.bind("<FocusIn>", lambda event, sq_id=square_id: \
                                    square_focused(sq_id, event))
        row.append(square)
    rule_labl.grid(row=i, column=tot_columns + 1, columnspan=4, padx=5, pady=5)
    squares.append(row)


def pack_separator_frame(window,):
    # Separate the grids
    separator_frame = tk.Frame(window)
    separator_frame.pack(pady=10)
    grid_separator = tk.Label(separator_frame, height=3, pady=10)
    grid_separator.configure(text="Code")
    grid_separator.grid(column=0, columnspan=3)
    return separator_frame

separator_frame = pack_separator_frame(window)


def pack_code_soln_frame(window):
    # Create the row of empty squares
    empty_row_frame = tk.Frame(window)
    empty_row_frame.pack(pady=10)

    empty_squares = []
    for j in range(3):
        empty_square = tk.Entry(empty_row_frame, width=5,
                                bg="white", validate='focusin')
        empty_square.grid(row=0, column=j, padx=5)
        #empty_square["command"] = lambda c=j: code_square_clicked(c)  # Bind click event
        empty_square.bind("<FocusIn>", lambda event, sq_id=square_id: \
                                        square_focused(sq_id, event))
        empty_squares.append(empty_square)
    return empty_row_frame, empty_squares


def pack_submit_button(window):
    # Create the submit button
    submit_button = tk.Button(window, text="Submit", width=10,
                            height=10, bg="green", command=submit_clicked)
    submit_button.pack(side="right", pady=10)
    







# Start the GUI event loop
window.mainloop()
