
import dataclasses
import tkinter as tk
from typing import Callable

import ui.problem
import ui.solution_ui
import ui.soln_ui_frames.soln_ui_solution_frame

import random_prob

@dataclasses.dataclass
class _Settings:
    max_code_length:'int' = 18
    previous_frame_packing_method:'str' = None
    previous_frame_packing_options:'dict' = None

@dataclasses.dataclass
class _LocalWidgets:
    fr_bt_block_1: tk.Frame = None
    scale_code_length: tk.Scale = None
    label_scale_code_length:'tk.Label' = None

    fr_code_length:tk.Frame = None
    bt_submit_prob_params:'tk.Button' = None

    btn_another_problem:'tk.Button' = None
    btn_cancel:'tk.Button' = None


    settings:'_Settings' = None

#----------------------------------------------------------------
# Public API
#----------------------------------------------------------------

def create_buttons_frame(widgets:'ui.solution_ui._Widgets',
                         parent_frame,
                         parent_frame_packing_method:'str',
                         parent_frame_packing_options:'dict',
                         previous_frame:'tk.Frame',
                         previous_frame_packing_method:'str',
                         previous_frame_packing_options:'dict',
                         on_new_problem:'Callable[[ui.problem.Problem], None]') -> tk.Frame:
    local_widgets =  _LocalWidgets(settings=_Settings())
    standard_args = {'widgets':widgets, 
                     'local_widgets':local_widgets,
                     'parent_frame':parent_frame,
                     'previous_page':previous_frame,
                     'on_new_problem':on_new_problem}
    
    # Reusables
    padx, pady, padxy = {'padx':5}, {'pady':5}, {'padx':5, 'pady':5}
    top, left, bottom = {'side':'top'}, {'side':'left'}, {'side':'bottom'}
    fillx, filly, fillxy = {'fill':'x'}, {'fill':'y'}, {'fill':'both'}
    n, s, e, w = {'anchor':'n'}, {'anchor':'s'}, {'anchor':'e'}, {'anchor':'w'}
    ne, nw, se, sw = {'anchor':'ne'}, {'anchor':'nw'}, {'anchor':'se'}, {'anchor':'sw'}
    font = {'font':('Arial', 12,)}

    packing_options = {}
    packing_options[str(id(parent_frame))] = "MainPage"
    packing_options[str(id(previous_frame))] = "PreviousPage"
    packing_options['kwargs'] = {}
    packing_options['packing_method'] = {
        'PreviousPage': previous_frame_packing_method,
        'MainPage': parent_frame_packing_method,
        'MainPage.ButtonsFrame': 'pack',
        'MainPage.ButtonsFrame.ButtonPreviousPage': 'pack',
        'MainPage.ButtonsFrame.ButtonAnotherProblem': 'pack',
        'MainPage.ButtonsFrame.ProblemParamsFrame': 'pack',
        'MainPage.ButtonsFrame.ProblemParamsFrame.LabelCodeLength': 'pack',
        'MainPage.ButtonsFrame.ProblemParamsFrame.ScaleCodeLength': 'pack',
        'MainPage.ButtonsFrame.ProblemParamsFrame.ButtonSubmit': 'pack',
        'MainPage.ButtonsFrame.ProblemParamsFrame.ButtonCancel': 'pack',
    }

    kwargs = packing_options['kwargs']
    kwargs['PreviousPage'] = previous_frame_packing_options
    kwargs['MainPage'] = parent_frame_packing_options
    kwargs['MainPage.ButtonsFrame'] = {'expand':True, 'fill':'both'}
    kwargs['MainPage.ButtonsFrame.ButtonPreviousPage'] = {**w, **left, **padxy}
    kwargs['MainPage.ButtonsFrame.ButtonAnotherProblem'] = {**w, **left, **padxy}
    kwargs['MainPage.ButtonsFrame.ProblemParamsFrame'] = {**w, **left, **padxy}
    kwargs['MainPage.ButtonsFrame.ProblemParamsFrame.LabelCodeLength'] = {**top, **fillx,
                                                                           **pady}
    kwargs['MainPage.ButtonsFrame.ProblemParamsFrame.ScaleCodeLength'] = {**top, **padxy}
    kwargs['MainPage.ButtonsFrame.ProblemParamsFrame.ButtonSubmit'] = {**bottom, **fillx}
    kwargs['MainPage.ButtonsFrame.ProblemParamsFrame.ButtonCancel'] = {**bottom, **fillx}

    packing_options['configs'] = {}
    configs = packing_options['configs']
    configs['MainPage'] = {}
    configs['MainPage.ButtonsFrame'] = {'bg':'yellow'}
    configs['MainPage.ButtonsFrame.ButtonPreviousPage'] = {'bg':'red', **font}
    configs['MainPage.ButtonsFrame.ButtonAnotherProblem'] = {**font}
    configs['MainPage.ButtonsFrame.ProblemParamsFrame'] = {}
    configs['MainPage.ButtonsFrame.ProblemParamsFrame.LabelCodeLength'] = {**font}
    configs['MainPage.ButtonsFrame.ProblemParamsFrame.ScaleCodeLength'] = {**font}
    configs['MainPage.ButtonsFrame.ProblemParamsFrame.ButtonSubmit'] = {**font}
    configs['MainPage.ButtonsFrame.ProblemParamsFrame.ButtonCancel'] = {**font}

    return _create_frame(standard_args, packing_options)
    
    

    
#---------------------------------------------------------------

    
def _create_frame(standard_args, packing_options:'dict') -> tk.Frame: 
    widgets:'ui.solution_ui._Widgets' = standard_args['widgets']
    local_widgets:'_LocalWidgets' = standard_args['local_widgets']
    parent = standard_args['parent_frame']
    previous_page = standard_args['previous_page']
    

    frame = tk.Frame(parent, 
                     **packing_options['configs']['MainPage.ButtonsFrame'])
    local_widgets.fr_bt_block_1 = frame
    btn_previous_page = tk.Button(
        frame, 
        text='Previous Page',
        command=lambda: [_pack_widget(parent, packing_options, unpack=True), 
                        _pack_widget(previous_page, packing_options)],
        **packing_options['configs']['MainPage.ButtonsFrame.ButtonPreviousPage']
    )
    widgets.bt_previous_page = btn_previous_page
    another_problem = tk.Button(
        frame, 
        text='Another Problem',
        command=lambda: _another_problem_clicked(standard_args, packing_options),
        **packing_options['configs']['MainPage.ButtonsFrame.ButtonAnotherProblem']
    )
    local_widgets.btn_another_problem = another_problem
    
    # Name the widgets
    leading_name = packing_options.get(str(id(widgets.fr_this_page)), None)
    packing_options[str(id(frame))] = f"{leading_name}.ButtonsFrame"
    leading_name = packing_options[str(id(frame))]
    packing_options[str(id(btn_previous_page))] = f"{leading_name}.ButtonPreviousPage"
    packing_options[str(id(another_problem))] = f"{leading_name}.ButtonAnotherProblem"

    #_pack_widget(btn_previous_page, packing_options)
    _pack_widget(another_problem, packing_options)
    return frame
    
    
def _another_problem_clicked(standard_args, packing_options):
    local_widgets:'_LocalWidgets' = standard_args['local_widgets']

    local_widgets.btn_another_problem.configure(state='disabled')

    params_frame = _problem_params_frame(
        standard_args,
        parent_frame=local_widgets.fr_bt_block_1,
        packing_options=packing_options
    )
    _pack_widget(params_frame, packing_options)

def _problem_params_frame(
        standard_args, 
        parent_frame:'tk.Frame',
        packing_options
    ):
    """Creates the frame which allows the user to 
    enter the kind of problem they want to solve"""
    widgets:'ui.solution_ui._Widgets' = standard_args['widgets']
    local_widgets:'_LocalWidgets' = standard_args['local_widgets']
    max_code_length = local_widgets.settings.max_code_length

    frame = tk.Frame(parent_frame)
    local_widgets.fr_code_length = frame
    label_code_length = tk.Label(
        frame, text='Drag slider to select code length',
        **packing_options['configs']['MainPage.ButtonsFrame.ProblemParamsFrame.LabelCodeLength']
    )
    local_widgets.label_scale_code_length = label_code_length
    scale = tk.Scale(frame, from_=1, to=max_code_length, orient='horizontal')
    local_widgets.scale_code_length = scale
    on_submit = _submit_prob_params_clicked
    btn_submit = tk.Button(
        frame, text='Submit', command=lambda: on_submit(standard_args, packing_options),
        **packing_options['configs']['MainPage.ButtonsFrame.ProblemParamsFrame.ButtonSubmit']
    )
    local_widgets.bt_submit_prob_params = btn_submit
    btn_cancel = tk.Button(
        frame, text='Cancel', command=lambda: _on_cancel(standard_args, packing_options),
        **packing_options['configs']['MainPage.ButtonsFrame.ProblemParamsFrame.ButtonCancel']
    )
    local_widgets.btn_cancel = btn_cancel
    



    # Name the widgets
    leading_name = packing_options[str(id(parent_frame))]
    packing_options[str(id(frame))] = f"{leading_name}.ProblemParamsFrame"
    leading_name = packing_options[str(id(frame))]
    packing_options[str(id(label_code_length))] = f"{leading_name}.LabelCodeLength"
    packing_options[str(id(scale))] = f"{leading_name}.ScaleCodeLength"
    packing_options[str(id(btn_submit))] = f"{leading_name}.ButtonSubmit"
    packing_options[str(id(btn_cancel))] = f"{leading_name}.ButtonCancel"



    _pack_widget(label_code_length, packing_options)
    _pack_widget(scale, packing_options)
    _pack_widget(btn_cancel, packing_options)
    _pack_widget(btn_submit, packing_options)
    return frame


def _pack_widget(widget:'tk.Widget', packing_options, unpack=False):
    widget_name = packing_options[str(id(widget))]
    packed = False
    if not unpack:
        match packing_options['packing_method'][widget_name]:
            case 'grid':
                widget.grid(**packing_options['kwargs'][widget_name]); packed = True
            case 'pack':
                widget.pack(**packing_options['kwargs'][widget_name]); packed = True
            case 'place':
                widget.place(**packing_options['kwargs'][widget_name]); packed = True
        print(f'just packed {widget_name}; packed={packed}')
    if unpack:
        match packing_options['packing_method'][widget_name]:
            case 'grid':
                widget.grid_forget()
            case 'pack':
                widget.pack_forget()
            case 'place':
                widget.place_forget()
            case 'grid_remove': 
                widget.grid_remove()
            

def _submit_prob_params_clicked(standard_args, packing_options):
    widgets:'ui.solution_ui._Widgets' = standard_args['widgets']
    local_widgets:'_LocalWidgets' = standard_args['local_widgets']
    on_new_problem_callback = standard_args['on_new_problem']

    problem = random_prob.generateRandomProblem(
        code_len=int(local_widgets.scale_code_length.get())
    )
    widgets.data_problem = problem

    _pack_widget(local_widgets.fr_code_length, packing_options, unpack=True)
    local_widgets.btn_another_problem.configure(state='normal')

    on_new_problem_callback(problem)

def _on_cancel(standard_args, packing_options):
    local_widgets:'_LocalWidgets' = standard_args['local_widgets']

    _pack_widget(local_widgets.fr_code_length, packing_options, unpack=True)
    local_widgets.btn_another_problem.configure(state='normal')