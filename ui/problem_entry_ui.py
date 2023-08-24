from typing import Any, Generator, Literal


import __init__
from ui.problem import ProblemBuilder, Rule, RuleBuilder

from utils.string_helpers import kmp

from tkinter import *

_this_page:'Frame'
_BTTN_ADD_COL:'Button' = None

def getFrame():
    return _this_page

def createNewFrame(root_window:'Tk', previous_page:'Frame'):
    global _this_page, _ROOT_WINDOW, _BTTN_ADD_COL
    global _WIDTH_BTTN_ADD_ROW, _HEIGHT_BTTN_ADD_ROW

    _ROOT_WINDOW = root_window
    _this_page = Frame(root_window, name="this entire page")

    # Create a button on this page that switches to the previous page
    return_to_prev_page_button = Button(_this_page, text="Go to previous page", 
                     command=lambda: [_this_page.pack_forget(), previous_page.pack()])
    return_to_prev_page_button.pack()

    frame = Frame(_this_page, name="problem Frame")
    frame.pack()
    buttons_frame = Frame(_this_page, name="buttons frame")
    buttons_frame.pack()
    # Button to create a new row
    badd_row = Button(buttons_frame, text="Add Row", bg="blue")
    # Button to add new column
    badd_col = Button(buttons_frame, text="Add Column", bg="blue")
    _BTTN_ADD_COL = badd_col
    # Button to submit problem
    bsubmit = Button(buttons_frame, text="Submit", bg="green")


    badd_row.configure(width=_WIDTH_BTTN_ADD_ROW, height=_HEIGHT_BTTN_ADD_ROW, 
                               command=lambda: _add_row(frame))
    badd_col.configure(width=_WIDTH_BTTN_ADD_COL, height=_HEIGHT_BTTN_ADD_COL, 
                        command=lambda: _add_column(frame))
    _change_add_column_button_state(badd_col)
    bsubmit.configure(width=_WIDTH_BTTN_SUBMIT, height=_HEIGHT_BTTN_SUBMIT)

    badd_row.pack(side=LEFT)
    badd_col.pack(side=LEFT)
    bsubmit.pack(side=LEFT)

    return _this_page



_grid:'list[list[BaseWidget]]' = []
_SQUARE_HEIGHT:'int' = 2
_SQUARE_WIDTH:'int' = 8
_PADX:'int' = 3
_PADY:'int' = 0
_PADX_LAST_4:'int' = 1
_PADY_LAST_4:'int' = 0

_WIDTH_BTTN_ADD_ROW:'int' = 10
_HEIGHT_BTTN_ADD_ROW:'int' = 3
_WIDTH_BTTN_ADD_COL:'int' = 10
_HEIGHT_BTTN_ADD_COL:'int' = 3
_WIDTH_BTTN_SUBMIT:'int' = 9
_HEIGHT_BTTN_SUBMIT:'int'=  4



_NO_OF_WIDGETS_IN_ROW_BELONGING_TO_RULE:'int' = 4
_ROOT_WINDOW:'Tk'

_LAST_2_ENTRY_WIDGETS:'dict[int,tuple[Entry, Literal[0, 1], int]]' = dict()
_CORRECT_ENTRY_WIDG:'int' = 0
_CORRECTLY_PLACED_ENTRY_WIDG:'int' = 1

def _add_row(parent_frame:'Frame'):
    global _grid
    # Get the current number of rows and columns
    rows = len(_grid)
    columns = len(_grid[0]) if rows > 0 else 0; print(f'There are {columns} columns and {rows} rows')
    columns = max(0, columns - _NO_OF_WIDGETS_IN_ROW_BELONGING_TO_RULE)
    curr_col = 0
    if rows == 0: #TODO Make the first row to be the delete column row
        pass

    # Create a new list for the new row
    new_row = []
    # Create a red X button for deleting the row
    x_button = Button(parent_frame, text="delete\n row", bg="red", width=_SQUARE_WIDTH,
                       height=_SQUARE_HEIGHT, command=lambda r=rows: _delete_row(r))
    x_button.grid(row=rows+1, column=curr_col, padx=_PADX, pady=_PADY, sticky='NW')
    curr_col += 1
    new_row.append(x_button)

    t = curr_col
    for c in range(1, columns):
        # Create an entry widget for user input
        entry = Entry(parent_frame, width=_SQUARE_WIDTH)
        entry.grid(row=rows+1, column=c, padx=_PADX, pady=_PADY)
        new_row.append(entry)
        curr_col += 1
    print(f'loop created {curr_col - t} new entries(columns)')

    _last_4_widgets(parent_frame, entire_row=new_row, last_row=rows, curr_col=curr_col+1)
    _change_add_column_button_state(_BTTN_ADD_COL)
    
    for col in range(len(_grid) - 1):
        widget:'Widget' = _grid[len(_grid) - 1][col]
        widget.grid(row=len(_grid) - 1, column=col, padx=_PADX, pady=_PADY)

   
def _last_4_widgets(parent_frame:'Frame', entire_row:'list[Widget]', last_row:'int', curr_col:'int'):
    # Widget 1
    # User enters how many items in the row are correct
    # aka belong to the code
    correct_entry = Entry(parent_frame, width=_SQUARE_WIDTH,
                          name= f'correct entry in row: {last_row + 1}')
    _LAST_2_ENTRY_WIDGETS[hash(correct_entry)] = (correct_entry, _CORRECT_ENTRY_WIDG, last_row + 1)
    validate_cmd = lambda h=hash(correct_entry): _last_2_entries_validator(h)
    correct_entry.configure(validate='key', validatecommand=validate_cmd)
    correct_entry.grid(row=last_row+1, column=curr_col, padx=_PADX_LAST_4, pady=_PADY_LAST_4)
    curr_col += 1
    entire_row.append(correct_entry)


    # Widget 2
    correct_label = Label(parent_frame, height=_SQUARE_HEIGHT, text='are correct and')
    correct_label.grid(row=last_row + 1, column=curr_col, padx=_PADX_LAST_4, pady=_PADY_LAST_4)
    curr_col += 1
    entire_row.append(correct_label)
    
    # Widget 3
    # User enters how many items in the row are correctly placed
    # aka are currently positioned in the position they would be in, in the code
    correctly_placed_entry = Entry(parent_frame, width=_SQUARE_WIDTH, textvariable=IntVar())
    _LAST_2_ENTRY_WIDGETS[hash(correctly_placed_entry)] = (correctly_placed_entry, 
                                                           _CORRECTLY_PLACED_ENTRY_WIDG, last_row + 1)
    validate_cmd = lambda h=hash(correctly_placed_entry): _last_2_entries_validator(h)
    correctly_placed_entry.configure(validate='key', validatecommand=validate_cmd)
    correctly_placed_entry.grid(row=last_row+1, column=curr_col, padx=_PADX_LAST_4, pady=_PADY_LAST_4)
    curr_col += 1
    entire_row.append(correctly_placed_entry)


    # Widget 4
    correctly_placed_label = Label(parent_frame, height=_SQUARE_HEIGHT,
                                    text='of them are correctly placed.')
    correctly_placed_label.grid(row=last_row + 1, column=curr_col, padx=_PADX_LAST_4, pady=_PADY_LAST_4)
    entire_row.append(correctly_placed_label)
    # Add the new row list to the _grid list
    _grid.append(entire_row)


def _last_2_entries_validator(widget_hash:'int'):
    entry, whether_corr_or_corr_placed, row = _LAST_2_ENTRY_WIDGETS[widget_hash]
    try:
        int(entry.get())
    except ValueError:
        return False
    
    print(f'last_2_entries_validator called; value entered: {int(entry.get())}')
    
    expected_max = len(_grid[row]) - (4 + 1) # minus last 4 widgets and the first one
    return -1 < int(entry.get()) < expected_max

def _delete_column(column:'int'):
    print(f'delete column called on col: {column}')
    # For every row
    for row in range(1, len(_grid)):
        columnth_widget:'Widget' = _grid[row][column]
        columnth_widget.grid_forget()
        for col in range(column):
            widget:'Widget' = _grid[row][col]
            widget.grid(row=row, column=col, padx=_PADX, pady=_PADY)
        # Move remaining widgets left
        for col in range(column, len(_grid)):
            widget:'Widget' = _grid[row][col]
            widget.grid(row=row, column=col - 1, padx=_PADX, pady=_PADY)

        _grid[row].pop(column)

def _delete_row(row:'int'):
    print(f'delete row called on row {row}')
    # TODO make it so it can't be called on row 0
    # Loop through each widget in the row
    for widget in _grid[row]:
        # Remove it from the grid
        widget.grid_forget()
    
    # Loop through the remaining rows below the deleted row
    for r in range(row + 1, len(_grid)):
        # Update the command for the delete row button for that row
        x_button:'Button' = _grid[r][0]
        x_button.configure(command=lambda this_row=r - 1: _delete_row(this_row))
            
        # Loop through each widget in the row
        for c in range(len(_grid[r])):
            # Move it up one row in the grid
            print(f'moving row: {r} items to row: {r-1}')
            _grid[r][c].grid(row=r-1, column=c)
            # If in last 2 entry widgets update the new row value
            _LAST_2_ENTRY_WIDGETS[hash(_grid[r][c])][2] = r - 1
    # Delete the row from the _grid list
    del _grid[row]
    _change_add_column_button_state(_BTTN_ADD_COL)


def _add_column(frame:'Frame'):
    # Check if theres at least one row
    if len(_grid) == 0: # TODO make this less than 2
        return

    # For every row
    for row in range(len(_grid)):
        new_middle_entry = Entry(frame, width=_SQUARE_WIDTH)
        last_mid_entry_pos = len(_grid[row]) - 4 
        new_middle_entry.grid(row=row, column=last_mid_entry_pos)
    

        for col in range(0, last_mid_entry_pos):
            widget:'Widget' = _grid[row][col]
            widget.grid(row=row, column=col, padx=_PADX, pady=_PADY)

        # Move remaining widgets to the right
        for col in range(last_mid_entry_pos, len(_grid[row])):
            widget:'Widget' = _grid[row][col]
            widget.grid(row=row, column=col + 1, padx=_PADX, pady=_PADY)

        _grid[row].insert(last_mid_entry_pos, new_middle_entry)
    
    #_refresh_delete_column_row(frame)
    _ROOT_WINDOW.update()
    _ROOT_WINDOW.geometry(str(_ROOT_WINDOW.winfo_width()+_SQUARE_WIDTH)+"x"+str(_ROOT_WINDOW.winfo_height()))


def _change_add_column_button_state(badd_col:'Button'):
    # TODO Make this check if len(_grid) > 1 coz first row is delete column row
    if len(_grid) > 0: 
        badd_col.configure(state=NORMAL)
    else:
        badd_col.configure(state=DISABLED)


_DELETE_COLUMN_ROW:'list[Widget]' = []
_STICKY_DELETE_COLUMN_ROW:'str' = 'NSEW'
def _refresh_delete_column_row(frame:'Frame'):
    """To be called only after the column has been added in other rows"""
    # A key idea here is there's no delete column button
    # for the first column as it contains delete row buttons
    expected_button_count = len(_grid[1]) - 5 if len(_grid) > 1 else 0
    column = len(_DELETE_COLUMN_ROW) + 1
    # Add delete column button for newly added columns
    while len(_DELETE_COLUMN_ROW) < expected_button_count:
        bdelete_col = Button(frame, text="Del\n column", bg="red")
        bdelete_col.configure(command=lambda c=column: _delete_column(c))
        bdelete_col.grid(row=0, column=column, padx=_PADX, pady=_PADY, sticky=_STICKY_DELETE_COLUMN_ROW)
        column += 1
        _DELETE_COLUMN_ROW.append(bdelete_col)
        _grid[0].append(bdelete_col)

    del_col_buttons_in_grid = set(_grid[0])
    # Check if a button is in _DELETE_COLUMN_ROW but not in _grid
    # It means the column was deleted
    for i in range(len(_DELETE_COLUMN_ROW)):
        button = _DELETE_COLUMN_ROW[i]
        if button not in del_col_buttons_in_grid:
            button.grid_forget() # Remove button
            for j in range(i):
                widget:'Widget' = _DELETE_COLUMN_ROW[j]
                widget.configure(command=lambda c=j + 1: _delete_column(c))
                widget.grid(row=0, column=j + 1, padx=_PADX, pady=_PADY, sticky=_STICKY_DELETE_COLUMN_ROW)
            # Move remaining buttons to the left
            for j in range(i + 1, len(_DELETE_COLUMN_ROW)):
                widget:'Widget' = _DELETE_COLUMN_ROW[j]
                widget.configure(command=lambda c=j: _delete_column(c))
                widget.grid(row=0, column=j, padx=_PADX, pady=_PADY, sticky=_STICKY_DELETE_COLUMN_ROW)
                
            _DELETE_COLUMN_ROW.remove(button) # changing loop params while in loop yikes
            

    
def _submit_clicked():
    
    # Walk through all the entries in _grid and insert
    # their values into Problem object
    problem_builder = ProblemBuilder()
    for row, col, entry in _for_every_middle_entry():
        problem_builder.insert_value(value=entry.get(), row=row, column=col)
        problem_builder.rule_for_row(row=row, rule=_get_rule(row))
        

def _for_every_middle_entry() -> 'Generator[tuple[int, int, Entry]]':
    """Helper function to produce the middle entries.
    Yields (row, column, entry) tuples"""
    for row in range(1, len(_grid)):
        end = len(_grid[row]) - _NO_OF_WIDGETS_IN_ROW_BELONGING_TO_RULE
        for col in range(1, end):
            entry = _grid[row][col]
            yield row, col, entry

def _get_rule(row:'int') -> Rule:
    corr_entry_index, corr_placed_entry_index = -4, -2
    corr_entry = int(_grid[row][corr_entry_index].get())
    corr_placed_entry = int(_grid[row][corr_placed_entry_index].get())
    rule = RuleBuilder().are_correct_count(corr_entry)\
                        .are_correctly_placed(corr_placed_entry)\
                        .build()
    return rule
