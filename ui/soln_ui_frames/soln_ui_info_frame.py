"""
Created on 2023-7-28
"""

__author__ = 'perez githumbi'

import dataclasses
import tkinter as tk
from tkinter import ttk

import ui.solution_ui

@dataclasses.dataclass
class _Config:
    lb_problem_info_font = 'Arial 10'
    lb_problem_info_text = """Crack the lock.
                           """

@dataclasses.dataclass
class _LocalWidgets:
    fr_info:'tk.Frame' = None
    lb_problem_info:'tk.Label' = None

    config:'_Config' = None


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------
def create_info_frame(widgets:'ui.solution_ui._Widgets',master:'tk.Frame'):
    """
    Create a new info unpacked frame.
    """
    
    local_widgets = _LocalWidgets()
    local_widgets.config = _Config()
    local_widgets.fr_info = tk.Frame(master)
    
    
    local_widgets.lb_problem_info = ttk.Label(local_widgets.fr_info,
                                        text=local_widgets.config.lb_problem_info_text,
                                        anchor='w', 
                                        font=local_widgets.config.lb_problem_info_font,
                                        justify='left')
    local_widgets.lb_problem_info.pack(side='left', fill='x', expand=True)

    return local_widgets.fr_info

# -----------------------------------------------------------------------------
# Private API
# -----------------------------------------------------------------------------
