

from math import exp
import tkinter as tk

from dataclasses import dataclass
from typing import Callable


import random_prob


import ui.problem
import  ui.soln_ui_frames.buttons_frame
import ui.soln_ui_frames.soln_ui_solution_frame
import ui.soln_ui_frames.soln_ui_info_frame
import ui.soln_ui_frames.answer_frame
import ui.sandwich

@dataclass
class _Settings:
    width_solution_block:'int' = 600
    height_solution_block:'int' = 400
    width_code_block:'int' = 600
    height_code_block:'int' = 400
    width_info_block:'int' = 600
    height_info_block:'int' = 40



@dataclass
class _Widgets:
    settings:'_Settings' = None

    fr_this_page:'tk.Frame' = None
    fr_previous_page:'tk.Frame' = None
    

    fr_bt_block_1:'tk.Frame' = None
    bt_previous_page:'tk.Button' = None
    bt_random_problem:'tk.Button' = None
    padx_bt_block_1:'int' = 5
    pady_bt_block_1:'int' = 5
    meta_bt_block_1_columns_count:'int' = 3
    
    fr_code_length:'tk.Frame' = None
    label_scale_code_length:'tk.Label' = None
    scale_code_length:'tk.Scale' = None
    bt_submit_length:'tk.Button' = None
    data_problem:'ui.problem.Problem' = None

    fr_info_block:'tk.Frame' = None


    fr_solution_block:'tk.Frame' = None
    canv_solution:'tk.Canvas' = None
    hbar_solution:'tk.Scrollbar' = None
    vbar_solution:'tk.Scrollbar' = None
    rects_solution:'set[int]' = None
    texts_solution:'set[int]' = None
    recolored_shapes_solution:'set[int]' = None
    meta_solution_square_size:'int' = 60
    meta_solution_rule_rect_width:'int' = 390


    fr_code_block:'tk.Frame' = None

    
    
#-------------------------Public API------------------------------------------------------------------------------------------------

def createSolutionPage(master:'tk.Tk', previous_page:'tk.Frame',
                        problem:'ui.problem.Problem'=None, 
                        on_new_problem:'Callable[[ui.problem.Problem],None]'=None) -> tk.Frame:
    widgets = _Widgets(settings=_Settings())
    
    widgets.fr_previous_page = previous_page
    widgets.data_problem = problem
    if widgets.data_problem is None:
        widgets.data_problem = random_prob.generateRandomProblem(3)

    _, canvas, entire_page = ui.sandwich.sandwich(master)
    widgets.fr_this_page = entire_page
    
    # Create the info frame
    info_block = (ui.soln_ui_frames.soln_ui_info_frame
                             .create_info_frame(widgets, widgets.fr_this_page))
    widgets.fr_info_block = info_block
    widgets.fr_info_block.config(bg='yellow')
    widgets.fr_info_block.pack(fill='x')

    # Create the buttons frame
    buttons_frame = ui.soln_ui_frames.buttons_frame.create_buttons_frame(
        widgets=widgets,
        parent_frame=entire_page,
        parent_frame_packing_method='pack',
        parent_frame_packing_options={'expand':True, 'fill':'x'},
        previous_frame=previous_page,
        previous_frame_packing_method='pack',
        previous_frame_packing_options={'side':True, 'fill':'x'},
        on_new_problem=on_new_problem,
    )
    buttons_frame.pack(expand=True, fill='x', after=widgets.fr_info_block)

    # Create the solution frame
    widgets.fr_solution_block = (ui.soln_ui_frames.soln_ui_solution_frame
                                 .create_solution_frame(widgets))
    solution_block = widgets.fr_solution_block
    solution_block.pack(expand=True, fill='both', after=buttons_frame)
    

    # Create the code frame
    answer_block = (ui.soln_ui_frames.answer_frame
                        .createAnswerFrame(widgets=widgets, 
                                        master=widgets.fr_this_page))
    widgets.fr_code_block = answer_block
    answer_block.config(bg='yellow')
    answer_block.pack(expand=True, fill='both')
    
    _set_window_size(master, info_block, buttons_frame, solution_block, answer_block)
    return canvas

    

    
#--------------------------------------------------------------------------------------------------------------------------------


def _set_window_size(root:'tk.Tk', *widgets:'tk.Widget') -> None:
    # Calculate total required width and height
    total_width, total_height = 0, 0
    for w in widgets:
        total_height += w.winfo_reqheight()
    total_width = max([w.winfo_reqwidth() for w in widgets])

    # Add some padding
    padding = 20
    total_width += padding
    total_height += padding

    # Set the window size
    root.geometry(f"{total_width}x{total_height}")



