from tkinter import *
from tkinter import ttk
import serial
import time
import Funcs
import Protocols

class Path:
    def __init__(self, id, numPoints, max, min, vertices, group, numInside):
        self.id = id
        self.numPoints = numPoints
        self.max = max
        self.min = min
        self.vertices = vertices
        self.group = group
        self.numInside = numInside

#create class to hold all global variables 
class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_size = 700

        #initialize final Gcode string telling machine to turn on spindle and inches as units
        self.gCode = "M3\nG20\n"
        #set feed rate 
        self.feed = 1000
        #bind click function to mouse left-click
        self.bind("<ButtonRelease-1>", self.release)
        self.bind("<B1-Motion>", self.preview)
        self.bind("<Button-1>", self.click)

        #counter for indexing
        self.cnt = 0
        self.pathCnt = 0
        #initialize array to hold all tool paths
        self.toolPaths = []
        #initialize array to hold each path as it is being made
        self.path = []
        #boolean to tell us when a path is closed
        self.closed = False
        #last pos
        self.lastx, self.lasty = None, None
        self.line = None

        #draw grid
        self.draw_grid()

    #interface functions:
    def draw_grid(self):

        l = range(0,14)
        for i in l:
            x1 = i * self.grid_size / 12
            y1 = self.grid_size
            x2 = self.grid_size
            y2 = i * self.grid_size / 12
            self.create_line(x1, 0, x1, y1, fill="gray40")
            self.create_line(0, y2, x2, y2, fill="gray40")
        
        halfx_y = self.grid_size/2
        len = self.grid_size
        self.create_line(halfx_y, 0, halfx_y, len, fill="gray15",width=4)
        self.create_line(0, halfx_y, len, halfx_y, fill="gray15",width=4)
        self.create_text(halfx_y+5, 0, text='6', anchor='nw', font='TkMenuFont', fill='gray15')
        self.create_text(len, halfx_y, text='6', anchor='se', font='TkMenuFont', fill='gray15')

    def click(self, event):
        if self.cnt == 0:
            self.lastx, self.lasty = event.x, event.y
            pos = event.x, event.y
            self.path.append(pos)

    def preview(self, event):
        if self.lastx and self.lasty:
            self.delete(self.line)
            self.line = self.create_line(self.lastx, self.lasty, event.x, event.y)

    def release(self, event):
        #store location of click
        pos = [event.x, event.y]

        #check to see if click location is close to exisitng point in tool path
        #if it is then we will call the path closed and set the final point equal to exisitng 
        if self.path != []:
            x = self.path[0]
            xdif = abs(x[0] - pos[0])
            ydif = abs(x[1] - pos[1])
            if xdif < 10 and ydif < 10:
                if self.cnt == 0:
                    self.cnt += 1
                    return
                self.closed = True 
                pos = x

        #draw line, append new location to path array, and set lastx/y for next line
        self.add_line(pos)
        self.path.append(pos)
        self.cnt += 1
        self.lastx, self.lasty = event.x, event.y

        #if closed then we transform all values to our dimenional coordiante frame
        #store the path in our toolPath array 
        #reset all of our values to make way for a new path
        if self.closed:
            l = range(len(self.path))
            i = 0
            for i in l:
                newLoc = []
                loc = self.path[i]
                newLoc.append((loc[0] - (self.grid_size/2)) * (12/self.grid_size))
                newLoc.append(((loc[1] - (self.grid_size/2)) * -1) * (12/self.grid_size))
                self.path[i] = newLoc
            minX = self.path[0][0]
            minY = self.path[1][1]
            maxX = self.path[0][0]
            maxY = self.path[1][1]
            for vertex1 in self.path:
                vertex = vertex1
                if vertex[0] > maxX:
                    maxX = vertex[0]
                elif vertex[0] < minX:
                    minX = vertex[0]
                if vertex[1] > maxY:
                    maxY = vertex[1]
                elif vertex[1] < minY:
                    minY = vertex[1]
        
            max = [maxX, maxY]
            min = [minX, minY]
            self.toolPaths.append(Path(self.pathCnt, self.cnt, max, min, self.path, 0, 0))
            self.path = []
            self.cnt = 0
            self.line = None
            self.closed = False 

    def add_line(self, pos):
        self.create_line(self.lastx, self.lasty, pos[0], pos[1])


root = Tk()
root.geometry("800x700")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root,width=700,height=700,background="gray30")
convertBut = ttk.Button(root, text='Convert', command=Funcs.gCodeConv(sketch))
saveBut = ttk.Button(root, text='Save', command=Funcs.fileSave(sketch))
streamBut = ttk.Button(root, text='Stream', command=Funcs.stream)
sketch.grid(column=0, row=0, sticky=(N, W))
convertBut.grid(column=1,row=0,sticky = NE)
saveBut.grid(column=1,row=0,sticky = E)
streamBut.grid(column=1,row=0,sticky = SE)

root.mainloop()

