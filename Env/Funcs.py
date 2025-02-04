import serial
import time

def stream(fileName):
        # Open grbl serial port
        s = serial.Serial('/dev/tty.usbserial-10',115200)

        # Open g-code file
        f = open('Files/'+fileName,'r');

        # Wake up grbl
        s.write(b"\r\n\r\n")  # Prefix the string with 'b' for bytes
        time.sleep(2)   # Wait for grbl to initialize 
        s.flushInput()  # Flush startup text in serial input

        # Stream g-code to grbl
        for line in f:
            l = line.strip() # Strip all EOL characters for consistency
            print('Sending: ' + l)
            s.write((l + '\n').encode())  # Encode G-code lines as bytes
            grbl_out = s.readline().decode().strip()
            print(' : ' + grbl_out.strip())

        # Wait here until grbl is finished to close serial port and file.
        input("  Press <Enter> to exit and disable grbl.") 

        # Close file and serial port
        f.close()
        s.close()    

def groupPaths(self):
    group = []
    i = 0
    for path1 in self.toolPaths:
        group.append(path1)
        i += 1
        allAssigned = False
        for path in self.toolPaths:
            if path.group == 0:
                allAssigned = False
                break
            allAssigned = True
        if allAssigned:
            break

        for path2 in self.toolPaths:
            if path1.max[0] > path2.max[0] and path1.max[1] > path2.max[1] and path1.min[0] < path2.min[0] and path1.min[1] < path2.min[1]:
                group.append(path2)
                print("here")
        
        for path in group:
            if path.group == 0:
                path.group = i

        group = []
    
    numGroups = range(1, i, 1)

    '''
    orderedPaths = []
    for j in numGroups:
        pathGroup = []
        for path in self.toolPaths:
            if j == path.group:
                pathGroup.append(path)
        for path1 in pathGroup:
            numInside = 0
            for path2 in pathGroup:
                if path1.max[0] > path2.max[0] and path1.max[1] > path2.max[1] and path1.min[0] < path2.min[0] and path1.min[1] < path2.min[1]:
                    numInside += 1
            path1.numInside = numInside
        
        for path1 in pathGroup:
            for path2 in pathGroup:
                if path1.numInside > 
'''
def gCodeConv(self):
    self.gCode = "M3\nG20\n"
    groupPaths(self)
    numPaths = len(self.toolPaths) - 1
    j = 0
    print("here")
    for path in self.toolPaths:
        i = 0
        numLocs = path.numPoints - 1
        for loc in path.vertices:
            x = str(loc[0])
            y = str(loc[1])
            feed = str(self.feed)
            #if start then rapid position to first location and then plunge 
            if i == 0:
                self.gCode += "G00 X"+x+" Y"+y+" Z1.0000000\n"
                self.gCode += "G01 X"+x+" Y"+y+" Z-.125 F"+feed+"\n"
                i += 1
            #if end then go to location and raise tool
            #if last loc and last path then kill tool, home, and end program
            elif i == numLocs:
                self.gCode += "G01 X"+x+" Y"+y+" Z-.125 F"+feed+"\n"
                self.gCode += "G01 X"+x+" Y"+y+" Z1.00000000 F"+feed+"\n"
                if j == numPaths:
                    self.gCode += "G28 X0 Y0\nM05\nM30"
                i = 0
            #else just add normal path
            else:
                self.gCode += "G01 X"+x+" Y"+y+" Z-.125 F"+feed+"\n"
                i += 1
        j += 1
    print(self.gCode)

def fileSave(self):
    file = open('Files/test.gcode','w')
    file.write(self.gCode)
    file.close

def test():
    x = 5