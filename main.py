from tkinter import *
from tkinter import ttk
import data
import datetime


def calculate(*args):
    global wpm, index
    current_time = datetime.datetime.now()
    completed_words = correct_words(index)
    time_span = (current_time - start_time).total_seconds()
    words_per_minute = completed_words / (time_span / 60)
    if index + 1 == words_total:
        top_label_var.set("Test over.")
        t_user.config(state='disabled')
        wpm_var.set(f'You had {completed_words} words out of {words_total} correct, giving you {words_per_minute.__floor__()} Words Per Minute.')
    else:
        wpm_var.set(f'{words_per_minute.__floor__()} Words Per Minute')
    index += 1


def correct_words(index):
    typed_words = t_user.get("1.0", END).split(" ")
    correct_words_total = 0
    for i in range(index):
        if typed_words[i] == words_list[i]:
            correct_words_total += 1
    return correct_words_total


data = data.Data()
words_string = ""
words_list = []
start_time: any
index = 0
words_total = 0

root = Tk()
root.title("Typing Test!")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

top_label_var = StringVar()
top_label_var.set("Type the words shown below as fast as you can!")
top_label = ttk.Label(mainframe, textvariable=top_label_var).grid(column=0, row=0)

t = Text(mainframe, width=100, height=10)
t.grid(column=0, row=1)

t_user = Text(mainframe, width=100, height=10)
t_user.grid(column=0, row=2)

wpm_var = StringVar()
wpm = ttk.Label(mainframe, textvariable=wpm_var).grid(column=0, row=3)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

t_user.focus()
root.bind("<space>", calculate)
t_user.bind('<BackSpace>', lambda _: 'break')
root.bind('<BackSpace>', lambda _: 'break')


def dismiss(words):
    global start_time, words_list, words_string, words_total
    words_total = words
    words_string, words_list = data.get_words(words)
    dlg.grab_release()
    dlg.destroy()
    t.insert(END, words_string)
    t.config(state='disabled')
    start_time = datetime.datetime.now()


dlg = Toplevel(root)
ttk.Label(dlg, text="How Many Words?").grid(column=2, row=1)
ttk.Button(dlg, text="30", command=lambda: dismiss(30)).grid(column=1, row=2)
ttk.Button(dlg, text="50", command=lambda: dismiss(50)).grid(column=2, row=2)
ttk.Button(dlg, text="100", command=lambda: dismiss(100)).grid(column=3, row=2)
dlg.protocol("WM_DELETE_WINDOW", lambda: dismiss(30)) # intercept close button
dlg.transient(root)   # dialog window is related to main
dlg.wait_visibility() # can't grab until window appears, so we wait
dlg.grab_set()        # ensure all input goes to our window
dlg.wait_window()     # block until window is destroyed

root.mainloop()
