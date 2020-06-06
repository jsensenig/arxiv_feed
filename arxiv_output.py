import tkinter as tk
from pylatexenc.latex2text import LatexNodes2Text


def print_results(results_list, keywords):
    i = 1
    for result in results_list:
        print(str(i) + ".  " + result[0])
        i += 1
    i = 1
    for result in results_list:
        for keyword, data in zip(keywords, result):
            if keyword == keywords[0]:
                print(str(i) + ".  " + keyword)
            else:
                print("--> " + keyword)
            print(LatexNodes2Text().latex_to_text(data))
        print("=================================")
        i += 1


def window_results(results_list, keywords):
    root_tk = tk.Tk()
    scrollbar = tk.Scrollbar()
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    window = tk.Text(root_tk,
                     font=24,
                     width=100,
                     height=40,
                     spacing2=4,
                     padx=10,
                     pady=10,
                     wrap=tk.WORD)

    i = 1
    for result in results_list:
        window.insert(tk.END, str(i) + ".  " + result[0] + "\n")
        i += 1
    window.insert(tk.END, "\n")
    i = 1
    for result in results_list:
        for keyword, data in zip(keywords, result):
            if keyword == keywords[0]:
                window.insert(tk.END, str(i) + ".  " + keyword + "\n")
            else:
                window.insert(tk.END, "--> " + keyword + "\n")
            window.insert(tk.END, LatexNodes2Text().latex_to_text(data) + "\n")
        window.insert(tk.END, "================================= \n")
        i += 1

    window.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=window.yview)
    tk.mainloop()
