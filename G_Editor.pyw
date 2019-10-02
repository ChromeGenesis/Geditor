#!/usr/bin/env python3

import os
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox

root = Tk()
root.geometry('700x450')
title = 'G Editor'
root.title('{} - {}'.format('Untitled', title))
global file_name
file_name = None

menu_bar = Menu(root)
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

def new_file(event=None):
    global file_name
    if file_name:
        if tkinter.messagebox.askokcancel("Open New File", "You're about to open a new file make sure you saved your work"):
            root.title('{} - {}'.format('Untitled', title))
            file_name = None
            context_text.delete(1.0, END)
    else:        
        root.title('{} - {}'.format('Untitled', title))
        file_name = None
        context_text.delete(1.0, END)
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), title))
        context_text.delete(1.0, END)
        with open(file_name) as _file:
            context_text.insert(1.0, _file.read())

def write_to_file(file_name):
    try:
        content = context_text.get(1.0, END)
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        tkinter.messagebox.showwarning("Save", "Could not save the file")

def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", ".txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), title))
        return 'break'

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
        return 'break'
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Do you want to QUIT for sure?\n Make sure you've saved your current work"):
        root.destroy()

def font(event=None):
    pass

def cut(event=None):
    context_text.event_generate("<<Cut>>")

def redo(event=None):
    context_text.event_generate("<<Redo>>")
    return 'break'

def select_all(event=None):
    context_text.tag_add('sel', '1.0', 'end')
    return "break"

def copy(event=None):
    context_text.event_generate("<<Copy>>")
    return 'break'
def undo(event=None):
    context_text.event_generate("<<Undo>>")
    return 'break'

def paste(event=None):
    context_text.event_generate("<<Paste>>")
    return 'break'

file_menu = Menu(menu_bar, tearoff=0)
files = menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", accelerator="Ctrl+N", compound="left", underline=0, command=new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", compound="left", underline=0, command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", compound="left", underline=0, command=save)
file_menu.add_command(label="Save as", accelerator="Shift+Ctrl+S", compound="left", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Alt+F4", compound="left", command=exit_editor)

                      
edit_menu = Menu(menu_bar, tearoff=0)
edits = menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", compound="left", command=undo)
edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", compound="left", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", compound="left", command=cut)
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", compound="left", command=copy)
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", compound="left", command=paste)
#edit_menu.add_separator()
#edit_menu.add_command(label="Find", accelerator="Ctrl+F", compound="left", underline=0)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", accelerator="Ctrl+A", compound="left", underline=7, command=select_all)

view_menu = Menu(menu_bar, tearoff=0)
views = menu_bar.add_cascade(label="View", menu=view_menu)

about_menu = Menu(menu_bar, tearoff=0)
abouts = menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", compound="left")
about_menu.add_command(label="Help", compound="left")

format_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Format', menu=format_menu)
format_menu.add_command(label='font', compound='left', accelerator='Ctrl+Q', command=font)
#format_menu.add_command(label='

shortcut_bar = Frame(root, height=25, background='DeepSkyBlue2')
shortcut_bar.pack(expand='no', fill='x')

context_text = Text(root, wrap='word')
context_text.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(context_text)
context_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=context_text.yview)
scroll_bar.pack(side='right', fill='y')
context_text.tag_config('active line', background='red')
context_text.configure(font='{consolas} 11 bold italic')

root.config(menu=menu_bar)


context_text.bind("<Control-y>", redo)
context_text.bind('<Control-a>', select_all)
context_text.bind("<Control-v>", paste)
context_text.bind("<Control-c>", copy)
context_text.bind("<Control-x>", cut)
context_text.bind("<Control-z>", undo)
context_text.bind("<Control-s>", save)
context_text.bind("<Control-o>", open_file)
context_text.bind("<Control-n>", new_file)

root.protocol('WM_DELETE_WINDOW', exit_editor)
mainloop()
