

from dataclasses import dataclass
import tkinter as tk
import ui.solution_ui


@dataclass
class _Config:
    width_square:'int' = 50
    width_rule:'int' = 460
    offset_x:'int' = 10
    offset_y:'int' = 10


@dataclass
class _LocalWidgets:
    fr_solution_frame:'tk.Frame' = None
    canv_solution:'tk.Canvas' = None
    hbar_solution:'tk.Scrollbar' = None
    vbar_solution:'tk.Scrollbar' = None

    rects_solution:'set[int]' = None
    texts_solution:'set[int]' = None

    config:'_Config' = None


def create_solution_frame(widgets:'ui.solution_ui._Widgets'):
    local_widgets = _LocalWidgets(config=_Config(), rects_solution=set(), 
                                  texts_solution=set())
    
    local_widgets.fr_solution_frame = tk.Frame(widgets.fr_this_page)
    

    local_widgets.canv_solution = tk.Canvas(local_widgets.fr_solution_frame)
    local_widgets.canv_solution.configure(bg='yellow')
    local_widgets.canv_solution.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    
    rows = len(widgets.data_problem.grid) 
    columns = len(widgets.data_problem.grid[0]) - 1 # Last column is a rule
    offset_x = local_widgets.config.offset_x
    offset_y = local_widgets.config.offset_y
    for row in range(rows):
        for col in range(columns):
            x0 = (col * local_widgets.config.width_square) + offset_x
            y0 = (row * local_widgets.config.width_square) + offset_y
            x1 = x0 + local_widgets.config.width_square
            y1 = y0 + local_widgets.config.width_square
            _create_soln_rects_and_text(widgets, local_widgets, x0, y0,
                                         x1, y1, row, col)
    
    for row in range(rows): # Make the last column wider than the previous ones
        x0 = (columns * local_widgets.config.width_square) + offset_x
        y0 = (row * local_widgets.config.width_square) + offset_y
        x1 = x0 + local_widgets.config.width_rule
        y1 = y0 + local_widgets.config.width_square
        _create_soln_rects_and_text(widgets, local_widgets, x0, y0, 
                                    x1, y1, row, columns)

    local_widgets.canv_solution.update_idletasks()
    
    _resize_frame(None, local_widgets)
    return local_widgets.fr_solution_frame
        
        

def _create_soln_rects_and_text(widgets:'ui.solution_ui._Widgets', 
                                local_widgets:'_LocalWidgets',
                                x0:float, y0:float, x1:float, y1:float,
                   problem_row:int=None, problem_column:int=None):

    rect = local_widgets.canv_solution.create_rectangle(x0, y0, x1, y1, outline='black')
    local_widgets.rects_solution.add(rect)

    text = str(widgets.data_problem.grid[problem_row][problem_column])
    text_obj = local_widgets.canv_solution.create_text((x0 + x1)/2, (y0 + y1)/2, 
                                                   justify='center', font="Arial 12",
                                                    text=text)
    local_widgets.texts_solution.add(text_obj)


def _resize_frame(event, local_widgets:'_LocalWidgets'):
    canvas = local_widgets.canv_solution
    frame = local_widgets.fr_solution_frame
    # Calculate the required width and height based on canvas contents
    canvas_width = (canvas.bbox("all")[2] - canvas.bbox("all")[0])+10
    canvas_height = (canvas.bbox("all")[3] - canvas.bbox("all")[1])+10
    
    # Set the frame's size based on the calculated dimensions
    canvas.config(width=canvas_width, height=canvas_height)
    frame.config(width=canvas_width, height=canvas_height)
    local_widgets.canv_solution.update_idletasks()
    
