"""
This module create a scrollable canvas in-between 
a given frame and a new frame, making the new child frame scrollable.
"""
import tkinter as tk


def sandwich(mother_frame:'tk.Frame') -> tuple['tk.Frame', 'tk.Canvas', 'tk.Frame']:
    """
    Create a scrollable canvas in-between the given frame and
    a new frame, making the new child frame scrollable.\n 
    Returns the sandwich: `mother_frame`, `canvas`, `new_frame`
    The caller should pack the returned canvas.

    # Don't Pack the returned frame. It will disable
    # the scrolling fucntionality of the canvas somehow.

    """
    # Create a canvas
    canvas = tk.Canvas(mother_frame,)
    

    # Create the scrollbars
    vscrollbar = tk.Scrollbar(canvas, orient='vertical', command=canvas.yview)
    vscrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=vscrollbar.set)

    hscrollbar = tk.Scrollbar(canvas, orient='horizontal', command=canvas.xview)
    hscrollbar.pack(side='bottom', fill='x')
    canvas.configure(xscrollcommand=hscrollbar.set)


    # Create a frame to hold the widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind('<Configure>', on_configure)
    canvas.bind_all("<MouseWheel>", lambda event: 
                canvas.yview_scroll(-1 * (event.delta // 210), "units"))

    # A VERY STRONG HINT: Don't Pack the frame. It disable
    # the scrolling fucntionality of the canvas somehow.

    return mother_frame, canvas, frame
