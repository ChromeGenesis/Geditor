#!/usr/bin/python3

import os
import sys
import tkinter as tk
import tkinter.messagebox as tmb
import tkinter.scrolledtext as tks
import tkinter.filedialog as tkf


class Geditor:
    def __init__(self):
        self._root = tk.Tk()

        self._text = tks.ScrolledText(self._root, wrap='word')
        self._text.configure(font=("Consolas", 12, "italic"))
        self._text.grid(row=1, column=0, sticky='nsew')
        self._text.focus_set()
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        shortcut_bar = tk.Frame(self._root, height=25, background='DeepSkyBlue2')
        shortcut_bar.grid(row=0, column=0, sticky='nsew')
        shortcut_bar.grid_columnconfigure(0, weight=0)
        shortcut_bar.grid_rowconfigure(0, weight=0)

        self.__file_name = None#'Untitled'
        self._title = 'Geditor'
        self._root.title('{} - {}'.format('Untitled', self._title))
        self._menu_bar = tk.Menu(self._root)

        self._root.config(menu=self._menu_bar)
        #self._root.wm_iconbitmap("./geditor.ico")

    def _new_file(self, event=None):
        if not self.__file_name:
            if self._text.edit_modified():
                ask1 = tmb.askyesnocancel("Start New File", "Do you want to save your previous work")
                if ask1:
                    self._save()
                    self._text.delete(1.0, 'end')
                    self._root.title('{} - {}'.format(os.path.basename(self.__file_name), self._title))
                elif ask1 == None:
                    pass
                else:
                    self._text.delete(1.0, 'end')
                    self.__file_name = None
                    self._root.title('{} - {}'.format('Untitled', self._title))
            else:
                ask2 = tmb.askyesnocancel("Start New File", "Do you want to save your previous work")
                if ask2:
                    self._save()
                    self._root.title('{} - {}'.format('Untitled', self._title))
                    self.__file_name = None
                    self._text.delete(1.0, 'end')
                else:
                    pass
        else:
            if self._text.edit_modified():
                ask3 = tmb.askyesnocancel("Start New File", "Do you want to save your previous work")
                if ask3:
                    self._save()
                    self._text.delete(1.0, 'end')
                    self._root.title('{} - {}'.format('Untitled', self._title))
                elif ask3 == None:
                    pass
                
                else:
                    self._text.delete(1.0, 'end')
                    self._root.title('{} - {}'.format('Untitled', self._title))

    def _save(self, event=None):
        if not self.__file_name or self.__file_name == 'Untitled':
            self._save_as()
            return 'break'
        else:
            self._write_to_file(self.__file_name)
            return 'break'

    def _save_as(self, event=None):
        in_file = tkf.asksaveasfilename(initialfile='Untitled.txt',
                                        defaultextension=".txt", filetypes=[("Text Documents", ".txt"),
                                                                            ("All Files", "*.*")])
        if in_file and in_file != '':
            self.__file_name = in_file
            self._write_to_file(in_file)
            self._root.title('{} - {}'.format(os.path.basename(in_file), self._title))
            self._text.edit_modified(False)
            return 'break'

    def _open_file(self, event=None):
        in_file = tkf.askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"),
                                                                          ("All Files", "*.*")])
        if in_file and in_file != '':
            self.__file_name = in_file
            self._root.title('{} - {}'.format(os.path.basename(in_file), self._title))
            self._text.delete(1.0, 'end')
            with open(in_file) as _file:
                self._text.insert(1.0, _file.read())

    def _write_to_file(self, file_name, event=None):
        try:
            text = self._text.get(1.0, 'end')
            with open(file_name, 'w') as _file:
                _file.write(text)
                self._text.edit_modified(False)
        except IOError as e:
            tmb.showwarning("Save", "Could not save the file" + '\n' + str(e))

    def _exit_editor(self, event=None):
        if self._text.edit_modified():
            ask = tmb.askyesnocancel("Exit", "Do you want to save your previous work")
            if ask:
                self._save()
                self._root.destroy()
            elif ask == None:
                pass
            else:
                self._root.destroy()
        else:
            self._root.destroy()

    def _check_file(self, event=None):
        if self.__file_name:
            if self._text.edit_modified():
                self._root.title('*' + '{} - {}'.format(os.path.basename(self.__file_name), self._title))
            else:
                self._root.title('{} - {}'.format(os.path.basename(self.__file_name), self._title))
            
        elif not self.__file_name:
            if self._text.edit_modified():
                self._root.title('*' + '{} - {}'.format('Untitled', self._title))
            else:
                self._root.title('{} - {}'.format('Untitled', self._title))

    def _cut(self, event=None):
        self._text.event_generate("<<Cut>>")
        return 'break'

    def _copy(self, event=None):
        self._text.event_generate("<<Copy>>")
        return 'break'

    def _redo(self, event=None):
        self._text.event_generate("<<Redo>>")
        return 'break'

    def _undo(self, event=None):
        self._text.event_generate("<<Undo>>")
        return 'break'

    def _select_all(self, event=None):
        self._text.tag_add('sel', '1.0', 'end')
        return 'break'

    def _paste(self, event=None):
        self._text.event_generate("<<Paste>>")

    def _bindings(self):
        self._text.bind("<Control-y>", self._redo)
        self._text.bind('<Control-a>', self._select_all)
        self._text.bind("<Control-v>", self._paste)
        self._text.bind("<Control-c>", self._copy)
        self._text.bind("<Control-x>", self._cut)
        self._text.bind("<Control-z>", self._undo)
        self._text.bind("<Control-s>", self._save)
        self._text.bind("<Control-o>", self._open_file)
        self._text.bind("<Control-n>", self._new_file)
        self._text.bind("<Control-Shift-s>", self._save_as)
        self._text.bind("<Button-3>", self._show_popup_menu)
        self._text.bind("<Any-KeyPress>", self._check_file)
        self._root.protocol('WM_DELETE_WINDOW', self._exit_editor)

    def _menu(self):
        file_menu = tk.Menu(self._menu_bar, tearoff=0)
        self._menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", accelerator="Ctrl+N", compound="left", underline=0, command=self._new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", compound="left", underline=0, command=self._open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", compound="left", underline=0, command=self._save)
        file_menu.add_command(label="Save as", accelerator="Shift+Ctrl+S", compound="left", command=self._save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4", compound="left", command=self._exit_editor)

        edit_menu = tk.Menu(self._menu_bar, tearoff=0)
        self._menu_bar.add_cascade(label="Edit", menu=edit_menu, underline=0)
        # edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", compound="left", command=self._undo)
        # edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", compound="left", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", compound="left", command=self._cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", compound="left", command=self._copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", compound="left", command=self._paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", compound="left", command=self._select_all)

    def _popup(self):
        self.popup_menu = tk.Menu(self._text, tearoff=0)
        self.popup_menu.add_command(label='cut', command=self._cut, compound='left')
        self.popup_menu.add_command(label='copy', command=self._copy, compound='left')
        self.popup_menu.add_command(label='paste', command=self._paste, compound='left')
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='save', command=self._save, compound='left')
        self.popup_menu.add_command(label='select all', command=self._select_all, compound='left')

    def _show_popup_menu(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def _external_file(self):
        print(sys.argv)
        if len(sys.argv) > 1:
            _file = sys.argv[1]
            try:
                with open(_file, 'r') as f:
                    self._text.insert(1.0, f.read())
                self._root.title('{} - {}'.format(os.path.basename(_file), self._title))
                self.__file_name = _file
            except Exception as e:
                print(e)
                pass

    def _mainloop(self):
        self._root.mainloop()


if __name__ == '__main__':
    app = Geditor()
    app._menu()
    app._bindings()
    app._popup()
    app._external_file()
    app._mainloop()
