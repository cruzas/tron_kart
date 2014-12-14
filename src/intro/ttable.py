"""Table class used with tkinter GUI applications.
@author: Nelson Dos Santos
"""

import tkinter


class TTable(tkinter.Frame):
    def __init__(self, root, rows=3, cols=3, headers=[], data=[]):
        super(TTable, self).__init__()
        #
        if type(root) != tkinter.Tk:
            raise TypeError('root is not a tkinter.Tk')
        if type(rows) != int:
            raise TypeError('rows is not an int')
        if type(cols) != int:
            raise TypeError('cols is not an int')
        if type(headers) != list:
            raise TypeError('headers is not list')
        if type(data) != list:
            raise TypeError('data is not a list')

        if rows < 1:
            rows = 1
        if cols < 1:
            cols = 1
        if len(headers) != cols:
            headers.clear()
            for i in range(cols):
                headers.append('Header '+str(i))

        if len(data) != rows:
            raise ValueError('data does not contain the right number of rows')
        for row in data:
            if len(row) != cols:
                raise ValueError('row in data contains wrong number of elements')
        #
        self.root = root
        self.data = data
        self.headers = headers
        self.rows = rows
        self.cols = cols

        self.font = 'arial'
        self.headers_font = (self.font, 16, 'bold')
        self.data_font = (self.font, 14)
        
        self.headers_labs = []
        self.data_labs = []
        self.lab_fg_color = 'white'
        self.lab_bg_color = 'black'
        self.padx = 15
        self.pady = 8
        self.border_width = 1
        self.text_align = tkinter.E
        
        for i in range(len(self.headers)):
            lab = tkinter.Label(self.root, font=self.headers_font, borderwidth=self.border_width,
                                relief=tkinter.SUNKEN, text=str(self.headers[i]), bg=self.lab_bg_color,
                                fg=self.lab_fg_color, anchor=self.text_align, pady=self.pady, padx=self.padx)
            lab.grid(row=0, column=i, sticky='ew')
            self.headers_labs.append(lab)

        for row in range(len(self.data)):
            for cell in range(len(self.data[row])):
                lab = tkinter.Label(self.root, font=self.data_font, text=str(self.data[row][cell]),
                                    borderwidth=self.border_width, relief=tkinter.SUNKEN, bg=self.lab_bg_color,
                                    fg=self.lab_fg_color, pady=self.pady, padx=self.padx, anchor=self.text_align)
                lab.grid(row=row+1, column=cell, sticky='ew')            
    #

# end TTable


def test():
    root = tkinter.Tk()

    headers = ['This', 'That',  'Those']
    data = [[12, 14, 28]]
    ttable = TTable(root, 1, 3, headers, data)

    root.mainloop()
#
#test()



