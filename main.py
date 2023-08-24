import tkinter as tk
import ui.solution_ui
import random_prob


root = tk.Tk()
root.title("Crack The Lock Game")
root.geometry("800x600")





_problem = random_prob.generateRandomProblem(code_len=3)
page:'tk.Frame'
def on_refresh(problem):
    global page
    page.pack_forget()
    page.destroy()
    page = ui.solution_ui.createSolutionPage(root, None,
                                              problem, on_new_problem=on_refresh)
    page.pack(expand=True, fill=tk.BOTH)
    page.update_idletasks()

page = ui.solution_ui.createSolutionPage(root, None, _problem, 
                                         on_new_problem=on_refresh)

page.pack(expand=True, fill=tk.BOTH)

root.mainloop()