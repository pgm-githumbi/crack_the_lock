import __init__
import problem_entry_ui
from tkinter import *


root = Tk()
root.geometry('500x500+100+100')
root.resizable(True, True)

current_page = Frame(root)

next_page = problem_entry_ui.createNewFrame(root, current_page)

B_to_next_page = Button(current_page, width=15, height=7, text="Enter problem")
B_to_next_page.configure(command=lambda: [current_page.pack_forget(), next_page.pack()])

B_to_next_page.pack()
current_page.pack()


root.mainloop()