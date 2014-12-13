"""
Run this script to watch the application.
"""

from src.trongrid import *
import tkinter


"""Why am using if __name__ == '__main__': ?
http://stackoverflow.com/questions/419163/what-does-if-name-main-do
"""
if __name__ == '__main__':
    root = tkinter.Tk()
    twin = TWindow(root, 'Tron Kart')
    root.mainloop()

    tgrid = TronGrid() # Main object
#
