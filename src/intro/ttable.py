"""
Author: Nelson Brochado
Creation: December, 2014
Last Update: 27.01.2015
Description: table for the Tron Kart's UI

TODO:
 - fix eventual errors
 - improve performance
"""

import tkinter as tk


class TTable(tk.Frame):
    """docs"""
    def __init__(self, root, rows, cols, h_row=0, h_col=0, headers=[], data=[]):
        super(TTable, self).__init__(root, background='black')
        if not isinstance(root, tk.Tk) and \
           not isinstance(root, tk.Toplevel) and \
           not isinstance(root, tk.Frame):
            raise TypeError('root is not a Tk or Toplevel object')
        if not isinstance (rows, int):
            raise TypeError('rows is not an int')
        if not isinstance(cols, int):
            raise TypeError('cols is not an int')
        if not isinstance(headers, list):
            raise TypeError('headers is not list')
        if not isinstance(data, list):
            raise TypeError('data is not a list')
        
        if rows < 0:
            rows = 0
        if cols < 0:
            cols = 0
        if len(headers) != cols:
            headers.clear()
            for i in range(cols):
                headers.append('Header '+str(i))

        if len(data) != rows:
            raise ValueError('data does not contain the right number of rows')
        for row in data:
            if len(row) != cols:
                raise ValueError('row in data contains wrong number of elements')

        self.data = data
        self.headers = headers
        self.rows = rows
        self.cols = cols

        self.font = 'arial'
        self.headers_font = (self.font, 16, 'bold italic')
        self.data_font = (self.font, 12, 'bold')
        
        self.headers_labs = []
        self.data_labs = []
        self.lab_fg_color = 'white'
        self.lab_bg_color = 'black'
        self.border_width = 1
        self.text_align = 'w'
        self.padx = 20
        self.pady = 5

        for i in range(len(self.headers)):
            lab = tk.Label(self, font=self.headers_font, borderwidth=self.border_width,
                           relief='sunken', text=str(self.headers[i]), bg=self.lab_bg_color,
                           fg=self.lab_fg_color, padx=self.padx, pady=self.pady)
            lab.grid(row=0, column=i, sticky='nsew')
            self.columnconfigure(i, weight=1)            
            self.headers_labs.append(lab)
            h_col += 1
        self.rowconfigure(0, weight=1)

        for row in range(len(self.data)):
            h_row += 1
            for cell in range(len(self.data[row])):
                lab = tk.Label(self, font=self.data_font, text=str(self.data[row][cell]),
                               borderwidth=self.border_width, relief='sunken', bg=self.lab_bg_color,
                               fg=self.lab_fg_color, padx=self.padx, pady=self.pady)
                lab.grid(row=h_row, column=cell, sticky='nsew')
                self.columnconfigure(cell, weight=1) 
            self.rowconfigure(h_row, weight=1)


def test():
    root = tk.Tk()
    ttable = TTable(root, 1, 3, h_row=0, h_col=0,
                    headers=["header 1", "header 2", "header 3"],
                    data=[["item 1", "item 2", "item 3"]])
    ttable.pack(expand=1, fill='both')
    root.mainloop()

if __name__ == '__main__':
    test()

