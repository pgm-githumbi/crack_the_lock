"""
This module contains the frame that allows the user
to insert the answer to the problem. It contains a 
button to allow the user to see the cpu generated 
answer to the problem.
"""
import dataclasses
from typing import Any


import solver


import tkinter as tk
import tkinter.font as tk_font
import tkinter.ttk as ttk


import ui.solution_ui as soln_ui
import sandwich


@dataclasses.dataclass
class _Settings:
    txt_width: int = 2
    txt_height: int = 2
    txt_font: str = "Arial 12"
    txt_padx: int = 2
    txt_pady: int = 10

    lb_width_cpu: int = 10
    lb_height_cpu: int = 4

    fr_answ_user_created: "bool" = False
    canv_answ_cpu_created: "bool" = False

    bt_widths: int = 13
    bt_heights: int = 3

    code_length: "int|None" = None
    solutions: "tuple[tuple]" = None

    user_answer_frame_pack_settings:'dict[str, Any]' = None
    lb_answer_feedback_grid_settings:'dict[str, Any]' = None
    lb_answer_feedback_height:'int' = 1
    lb_answer_feedback_width:'int' = 16

    typed_solutions:'list[tuple]' = None


@dataclasses.dataclass
class _LocalWidgets:
    fr_answ: tk.Frame = None
    fr_answ_user: tk.Frame = None
    fr_answ_user_txts: tk.Frame = None
    fr_answ_user_found_answers:'tk.Frame' = None
    bt_see_answ: tk.Button = None
    bt_see_if_correct:'tk.Button' = None
    lb_answer_feedback: tk.Label = None
    lb_found_answers: tk.Label = None

    canv_answ_cpu:'tk.Canvas' = None
    vertical_bar_answ_cpu: 'tk.Scrollbar' = None
    horizontal_bar_answ_cpu: 'tk.Scrollbar' = None
    fr_answ_cpu: tk.Frame = None
    lb_purpose: tk.Label = None
    lbs_answ_cpu: "list[tk.Label]" = None
    bt_user: "tk.Button" = None

    lb_answers_count:'tk.Label' = None

    txts: "list[tk.Text]" = None

    settings: _Settings = None


# ----------------------------------------------------------------
# Public API
# ----------------------------------------------------------------
def createAnswerFrame(
    widgets: "soln_ui._Widgets",
    master: "tk.Frame",
):
    """Create the answer frame without packing it. Caller should pack/'render' returned frame.\n
    Before you use this api, make sure the `solution` to the problem in `widgets.data_problem` is set
    """
    loc_widgets = _LocalWidgets(settings=_Settings())
    # _, mother_canvas, answer_frame = sandwich.sandwich(master)
    loc_widgets.fr_answ = tk.Frame(master)

    loc_widgets.fr_answ_user = tk.Frame(loc_widgets.fr_answ, bg='light green')
    loc_widgets.fr_answ_cpu = tk.Frame(loc_widgets.fr_answ)

    _show_user_answer(widgets, loc_widgets)
    return loc_widgets.fr_answ


# ----------------------------------------------------------------
# PRIVATE APIS
# ----------------------------------------------------------------


def _show_user_answer(widgets: "soln_ui._Widgets", loc_widgets: "_LocalWidgets"):
    """Create and render the frame allowing the user to attempt to answer
    the question and submit their answers
    """
    if loc_widgets.settings.fr_answ_user_created is True: # Create only once
        loc_widgets.fr_answ_cpu.pack_forget()
        loc_widgets.fr_answ_user.pack(
            **loc_widgets.settings.user_answer_frame_pack_settings
        )
        return

    #Get the cpu's solutions to the problem
    loc_widgets.settings.solutions = solver.get_solutions( 
        widgets.data_problem, widgets.data_problem.code_alphabet
    )
    loc_widgets.settings.solutions = tuple(loc_widgets.settings.solutions)
    loc_widgets.settings.code_length = len(loc_widgets.settings.solutions[0])

    # Create the label to display the number of correct solutions
    label_header:'tk.Label' = loc_widgets.lb_answers_count
    label_header = tk.Label(
        master=loc_widgets.fr_answ_user, bg='light green',
        text=f"There are {len(loc_widgets.settings.solutions)} unique solutions",
        font=loc_widgets.settings.txt_font,
        justify="center",
    )
    label_header.pack(side=tk.TOP, fill=tk.X)
    
    
    # Create the text widgets to accept the user's answers
    loc_widgets.fr_answ_user_txts = tk.Frame(loc_widgets.fr_answ_user)
    txts_frame:'tk.Frame' = loc_widgets.fr_answ_user_txts
    txts_frame.pack(side=tk.TOP)
    loc_widgets.txts = [None] * loc_widgets.settings.code_length
    for i in range(loc_widgets.settings.code_length):
        _create_n_insert_text_widgets(widgets, loc_widgets, i)

    # Create button to allow user to see if their answer is correct
    btn_check_correctness:'tk.Button' = loc_widgets.bt_see_if_correct
    btn_check_correctness = tk.Button(
        txts_frame,
        text="Check If Correct",
        width=loc_widgets.settings.bt_widths,
        height=loc_widgets.settings.bt_heights,
        font=loc_widgets.settings.txt_font,
        command=lambda: _check_answer(widgets, loc_widgets),
    )
    btn_check_correctness.pack(side=tk.LEFT, padx=3)

    # Create button to allow user to see the cpu generated answers
    btn_see_answer:'tk.Button' = loc_widgets.bt_see_answ
    btn_see_answer = tk.Button(
        loc_widgets.fr_answ_user,
        text="See Answer(s)",
        width=len("See Answer")*4,
        height=loc_widgets.settings.bt_heights,
        font=loc_widgets.settings.txt_font,
        bg='light green',
        command=lambda: _show_cpu_answer(widgets, loc_widgets),
    )
    btn_see_answer.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Render the frame we've been creating
    loc_widgets.settings.user_answer_frame_pack_settings = {'expand': True,
                                                            'fill': "both"}
    loc_widgets.fr_answ_user.pack(
        **loc_widgets.settings.user_answer_frame_pack_settings
    )
    loc_widgets.settings.fr_answ_user_created = True








def _create_n_insert_text_widgets(widgets:'soln_ui._Widgets',
                                  local_widgets: "_LocalWidgets", column: "int"):
    """Create and render the text widgets for accepting the
    user's thoughts on the value of the code at each position"""
    txts = local_widgets.txts
    txts[column] = tk.Text(
        master=local_widgets.fr_answ_user_txts,
        width=local_widgets.settings.txt_width,
        height=local_widgets.settings.txt_height,
        font="Arial 18",
        takefocus=True,

    )
    def on_tab(col:'int'=column, local_widgets:'_LocalWidgets'=local_widgets):
        txts = local_widgets.txts
        next_text = txts[(col+1)%len(txts)]
        next_text.tk_focusNext().focus()
        next_text.focus()

    txts[column].bind('<Tab>', lambda _: on_tab())
    txts[column].bind('<Right>', lambda _: on_tab())
    txts[column].bind('<Left>', lambda e: e.widget.tk_focusPrev().focus())
    txts[column].bind("<Key>", lambda _: _character_limit(txts[column], _))
    txts[column].bind("<Return>", lambda _: on_tab())

    txts[column].pack(side=tk.LEFT, padx=3)
    






#----------------------------------------------------------------
# Callback
#----------------------------------------------------------------
def _check_answer(widgets:'soln_ui._Widgets',local_widgets: "_LocalWidgets"):
    """The user submited their answer, give them feedback"""
    typed_answer = [None] * len(local_widgets.txts)
    for i in range(len(typed_answer)):
        text = local_widgets.txts[i].get("1.0", "end")
        for character in text:
            if character in widgets.data_problem.code_alphabet:
                typed_answer[i] = character
    
    label_answer_feedback_settings = local_widgets.settings.lb_answer_feedback_grid_settings
    label_answer_feedback_settings = {
        'row':5, 'column':0, 'columnspan':3, 'padx':5, 'pady':5, 'ipadx':7
    }
    label_answer_feedback_settings = {'side':tk.BOTTOM, 'before':local_widgets.bt_see_answ}
    label_answer_feedback = local_widgets.lb_answer_feedback
    if local_widgets.settings.typed_solutions is None:
        local_widgets.settings.typed_solutions = []

    # If the answer is correct but the user had typed it before
    if (typed_answer in local_widgets.settings.solutions
        and typed_answer in local_widgets.settings.typed_solutions
    ):
        label_answer_feedback = _create_answer_feedback_label(
            local_widgets=local_widgets,
            text="Correct answer but previously seen"
        )
        label_answer_feedback.config(fg='orange')
        label_answer_feedback.pack(**label_answer_feedback_settings)
    # If the entire answer is correct and the user
    # hasn't entered it before
    if (
        typed_answer in local_widgets.settings.solutions 
        and typed_answer not in local_widgets.settings.typed_solutions
    ):
        label_answer_feedback = _create_answer_feedback_label(
            local_widgets,
            text="Correct Answer!!"
        )
        label_answer_feedback.config(fg='green')
        label_answer_feedback.pack(**label_answer_feedback_settings)
        local_widgets.settings.typed_solutions.append(typed_answer)
        _refresh_found_answers_label(local_widgets)
       
    # If the answer is incorrect
    if typed_answer not in local_widgets.settings.solutions:
        label_answer_feedback = _create_answer_feedback_label(
            local_widgets=local_widgets,
            text="Invalid Answer",
        )
        label_answer_feedback.config(fg='red')
        label_answer_feedback.pack(**label_answer_feedback_settings)
        
        


def _create_answer_feedback_label(local_widgets:'_LocalWidgets', text:'str'):
    """Create a label to tell the user if their submitted answer is correct"""
    if local_widgets.lb_answer_feedback is not None:
        local_widgets.lb_answer_feedback.grid_forget()
    
    local_widgets.lb_answer_feedback = tk.Label(
        master=local_widgets.fr_answ_user,
        text=text,
        width=local_widgets.settings.lb_answer_feedback_width,
        height=local_widgets.settings.lb_answer_feedback_height,
        font="Arial 12 bold",
        justify='center',
    )
    return local_widgets.lb_answer_feedback




def _refresh_found_answers_label(local_widgets:'_LocalWidgets'):
    """Refresh the label detailing all the answers the user has 
    previously submitted"""
    found_answers_text = "Found Solutions:\n"
    for soln in local_widgets.settings.typed_solutions:
        for i in range(len(soln)):
            if i == len(soln)-1:
                found_answers_text += f"{soln[i]}"
            else:
                found_answers_text += f"{soln[i]}, "
        found_answers_text += "\n"

    label:'tk.Label' = local_widgets.lb_found_answers
    master:'tk.Frame' = local_widgets.fr_answ_user_found_answers
    if master is None:
        master = tk.Frame(local_widgets.fr_answ_user)
        master.pack(side=tk.TOP, after=local_widgets.lb_answers_count, pady=7)
        master.pack_propagate(False)
    if label is None:
        label = tk.Label(
            master=master,
            text=found_answers_text,
            width=local_widgets.settings.lb_width_cpu*4,
            height=local_widgets.settings.lb_height_cpu,
            font=local_widgets.settings.txt_font,
        )
        label.grid(row=0, column=0, padx=5, pady=5, ipady=10)
    else:
        curr_ipady = label.grid_info()['ipady']
        label.config(text=found_answers_text, ipady=curr_ipady + 10)
        return
    
    
    
    










#------------------------------------------------------------------------------

def _show_cpu_answer(widgets: "soln_ui._Widgets", local_widgets: "_LocalWidgets"):
    if local_widgets.settings.canv_answ_cpu_created is True: # Create only once
        local_widgets.fr_answ_cpu.pack(expand=True, fill="both")
        return

    # Create label telling the user that this are the 
    # cpu answers to the problem
    local_widgets.fr_answ_cpu.config(bg="green")
    if local_widgets.lb_purpose is None:
        local_widgets.lb_purpose = tk.Label(
            local_widgets.fr_answ_cpu, text="Correct Answers:",
            font=local_widgets.settings.txt_font,
        )
    local_widgets.lb_purpose.grid(row=0, column=0, columnspan=3, padx=5, pady=5)


    local_widgets.lbs_answ_cpu = [None] * len(local_widgets.settings.solutions)
    # create a label for each solution
    for i in range(len(local_widgets.settings.solutions)):
        local_widgets.lbs_answ_cpu[i] = tk.Label(
            local_widgets.fr_answ_cpu,
            text=_stringify_solution(local_widgets.settings.solutions[i]),
            width=local_widgets.settings.lb_width_cpu,
            height=local_widgets.settings.lb_height_cpu,
            font=local_widgets.settings.txt_font,
            bg="blue",
        )
        local_widgets.lbs_answ_cpu[i].grid(
            row=i + 1, column=0, 
            ipadx=len(f'solution {i+1}: {local_widgets.settings.solutions[i]}')*3, 
            padx=6, pady=6,
            columnspan=local_widgets.settings.code_length*3,
        )

    # create a button to go back to the frame allowing user
    # to attempt to solve the problem
    local_widgets.bt_user = tk.Button(
        local_widgets.fr_answ_cpu,
        width=local_widgets.settings.lb_width_cpu,
        height=local_widgets.settings.lb_height_cpu,
        text="Back",
        font=local_widgets.settings.txt_font,
        command=lambda: _show_user_answer(widgets, local_widgets),
    )
    local_widgets.bt_user.grid(
        row=1, column=local_widgets.settings.code_length*4, 
        padx=15, ipadx=15
    )

    #Pack the frame showing the cpu answers
    local_widgets.fr_answ_cpu.pack(expand=True, fill="both")
    local_widgets.settings.canv_answ_cpu_created = True




def _character_limit(text_widg: "tk.Text", _):
    if len(text_widg.get("1.0", "end")) > 1:
        text_widg.bell()
        text_widg.delete("1.0", "end")


def _stringify_solution(solution:'list[str]'):
    soln_string = ""
    for letter in solution:
        soln_string += f"{letter} "
    return soln_string