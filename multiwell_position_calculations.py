import os
from tkinter import LabelFrame, Frame, Checkbutton, Button, Entry, Label, Tk, StringVar, DoubleVar, IntVar, Scale, \
    DISABLED, BOTH, CENTER, HORIZONTAL, NORMAL, END, RIDGE, RAISED, SUNKEN, W, LEFT, messagebox
from tkinter.filedialog import askdirectory

'''
    Dictionaries and Lists
'''

col = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
PlateFormats = {"6": (3, 2), "8": (4, 2), "12": (4, 3), "24": (6, 4), "96": (12, 8), "384": (24, 16)}
PossNumWell = list(PlateFormats.keys())
CameraFormats = {"PCO.Edge": (6.5, 2048, 2048), "CascadeII": (16, 512, 512), "Prime95": (11, 1200, 1200),
                 "iXon 888": (13, 1024, 1024), "Other": ("", "", "")}
Cameras = list(CameraFormats.keys())
CoordinateStart = {"X Start": 0, "Y Start": 0, "Z Start": 0, "All Start": (0, 0, 0)}
StartButtonsText = list(CoordinateStart.keys())
StartButtonsText.sort()
CoordinateEnd = {"X End": 0, "Y End": 0, "Z End": 0, "All End": (0, 0, 0)}
EndButtonsText = list(CoordinateEnd.keys())
EndButtonsText.sort()
PossNumTiles = (1, 2, 3, 4, 5, 6)

'''
    Callback functions
'''


def click(event):
    clickGeneral(event.widget)


def clickGeneral(ObjectClicked):
    if ObjectClicked["state"] == DISABLED:
        pass
    else:
        if ObjectClicked["bg"] == "SystemButtonFace":
            ObjectClicked.config(bg="White", fg="Blue")
        else:
            ObjectClicked.config(bg="SystemButtonFace", fg="SystemButtonText")


def clickNumWell(event):
    global formate
    event.widget.config(bg="White", fg="Blue")
    for i in range(0, len(PossNumWell)):
        if numWell[i] == event.widget:
            formate = PlateFormats[PossNumWell[i]]
            counter = 0
            for i in range(0, 16):
                for j in range(0, 24):
                    if ((i <= formate[1] - 1) and (j <= formate[0] - 1)):
                        WellButtonList[counter].config(state=NORMAL, bg="SystemButtonFace", fg="SystemButtonText")
                    else:
                        WellButtonList[counter].config(state=DISABLED, fg="White", bg="SystemButtonFace")
                    counter = counter + 1
        else:
            numWell[i].config(bg="SystemButtonFace", fg="SystemButtonText")
    for j in range(0, 24): WellColList[j].config(bg="SystemButtonFace", fg="SystemButtonText")
    for j in range(0, 16): WellRowList[j].config(bg="SystemButtonFace", fg="SystemButtonText")
    ALL.config(bg="SystemButtonFace", fg="SystemButtonText")


def SelectCamera(event):
    for i in range(0, len(Cameras)):
        if event.widget == CameraList[i]:
            event.widget.config(bg="White", fg="Blue")
            pixel.delete(0, END)
            pixel.insert(0, CameraFormats[Cameras[i]][0])
            numPixelx.delete(0, END)
            numPixelx.insert(0, CameraFormats[Cameras[i]][1])
            numPixely.delete(0, END)
            numPixely.insert(0, CameraFormats[Cameras[i]][2])
        else:
            CameraList[i].config(bg="SystemButtonFace", fg="SystemButtonText")


def LoadParam(event):
    global X1, Y1, X2, Y2, Z1, Z3, Z2, positions
    params = ["0", "0", "0", "0", "0", "0", "0"]
    paramFile = "C:\\Users\\Public\\Metamorph\\PosInfo.txt"
    if os.path.isfile(paramFile):
        target = open(paramFile, 'r')
        params = target.read()
        target.close()
        params = params[1:-1].split(";")
    X1 = float(params[0])
    Y1 = float(params[1])
    X2 = float(params[2])
    Y2 = float(params[3])
    Z1 = float(params[4])
    Z3 = float(params[5])
    Z2 = float(params[6])
    positions.set("X Start " + str(X1) + "; X End " + str(X2) + "\nY Start " + str(Y1) + "; Y End " + str(
        Y2) + "\nZ Start " + str(Z1) + "; Z End " + str(Z3) + "; Z interm " + str(Z2))


def clickTile(event):
    global Tile
    for i in range(0, len(PossNumTiles)):
        Text = str(i + 1) + "x" + str(i + 1)
        if event.widget["text"] == Text:
            numTile[i].config(bg="White", fg="Blue")
            Tile = i + 1
        else:
            numTile[i].config(bg="SystemButtonFace", fg="SystemButtonText")


def CalcPos(event):
    global Zend

    #   Needs to get all values in all fields at this step
    Xstart = min(X1, X2)
    Xend = max(X1, X2)
    Ystart = min(Y1, Y2)
    Yend = max(Y1, Y2)
    Zstart = Z1
    Zend = Z3

    if optovar.get() == "None":
        OPTOVAR = 1
    else:
        OPTOVAR = float(optovar.get())

    SX = int(numPixelx.get()) * float(pixel.get()) / int(objective.get()) / OPTOVAR
    SY = int(numPixely.get()) * float(pixel.get()) / int(objective.get()) / OPTOVAR
    # Needs to add the zoom....

    XStep = SX * (100 - overlap.get()) / 100
    YStep = SY * (100 - overlap.get()) / 100

    Zend = Zend - (Z2 - Zstart)
    Z1Z2Step = (Z2 - Zstart) / formate[1]
    Z1Z3Step = (Zend - Zstart) / formate[0]

    JumpX = (Xend - Xstart) / (formate[0] - 1)
    JumpY = (Yend - Ystart) / (formate[1] - 1)
    print(("Col : %d, Rows : %d, JumpX : %d, JumpY : %d") % (formate[1], formate[0], JumpX, JumpY))

    X = Xstart
    Y = Ystart
    Z = Zstart

    CountPos = 0
    for j in range(0, formate[1]):
        for i in range(0, formate[0]):
            Text = WellButtonList[j * 24 + i]
            if Text["bg"] == "White":
                CountPos = CountPos + Tile * Tile
    PositionList = open("C:\\Users\\Public\\Metamorph\\PositionList.stg", 'w')
    PositionList.write(
        "\"Stage Memory List\", Version 6.0 \n0, 0, 0, 0, 0, 0, 0, \"um\", \"um\" \n0 \n" + str(CountPos) + "\n")
    CountPos = 0
    for j in range(0, formate[1]):
        for i in range(0, formate[0]):
            Text = WellButtonList[j * 24 + i]
            if Text["bg"] == "White":
                print(Text["text"])
                XTile = X - ((Tile - 1) * XStep) / 2
                YTile = Y - ((Tile - 1) * YStep) / 2
                for k in range(0, Tile):
                    for l in range(0, Tile):
                        CountPos = CountPos + 1
                        PositionList.write(
                            "\"Position " + Text["text"] + "_" + str(k + 1) + "_" + str(l + 1) + "\", " + (
                                        "%.3f" % XTile) + ", " + ("%.3f" % YTile) + ", " + (
                                        "%.3f" % Z) + ", 0, 0, FALSE, -9999, TRUE, TRUE, 0, -1, \"\"\n")
                        print(("Position\t%d:\tX: %d.4\tY:%d.4") % (CountPos, XTile, YTile))
                        XTile = XTile + XStep
                    YTile = YTile + YStep
                    XTile = X - ((Tile - 1) * XStep) / 2
            X = X + JumpX
            Z = Z + Z1Z2Step
        Y = Y + JumpY
        X = Xstart
        Z = Zstart + Z1Z3Step * j
    print(("\nNumber of positions : %d") % (CountPos))
    PositionList.close()


def clickRow(event):
    clickGeneral(event.widget)
    for i in range(0, 24):
        tempo = WellButtonList[col.index(event.widget["text"]) * 24 + i]
        if tempo["state"] == NORMAL: WellButtonList[col.index(event.widget["text"]) * 24 + i].config(
            bg=event.widget["bg"], fg=event.widget["fg"])


def clickCol(event):
    clickGeneral(event.widget)
    for i in range(0, 16):
        tempo = WellButtonList[i * 24 + int(event.widget["text"]) - 1]
        if tempo["state"] == NORMAL: WellButtonList[i * 24 + int(event.widget["text"]) - 1].config(
            bg=event.widget["bg"], fg=event.widget["fg"])


def clickALL(event):
    clickGeneral(event.widget)
    for i in range(0, 16):
        if i < formate[1]: WellRowList[i].config(bg=event.widget["bg"], fg=event.widget["fg"])
        for j in range(0, 24):
            tempo = WellButtonList[i * 24 + j]
            if tempo["state"] == NORMAL: WellButtonList[i * 24 + j].config(bg=event.widget["bg"], fg=event.widget["fg"])
    for j in range(0, 24):
        if j < formate[0]: WellColList[j].config(bg=event.widget["bg"], fg=event.widget["fg"])


def Leave(event):
    root.destroy()


'''
*********************************
Placing elements in main Window
*********************************
'''

root = Tk()
global X1, Y1, X2, Y2, Z1, Z3, Z2
X1 = 0
Y1 = 0
X2 = 0
Y2 = 0
Z1 = 0
Z2 = 0
Z3 = 0
rootWidth = 900
rootHeight = 1100
ex = Frame(root, width=rootWidth, height=rootHeight)
ex.pack(fill=BOTH, expand=1)

Block1 = 10

labelObjective = Label(root, text="Objective Magnification", fg="Blue", justify=LEFT)
labelObjective.place(x=10, y=Block1)
objective = Entry(root, bg="White", fg="Blue", width=15)
objective.insert(0, "100")
objective.place(x=150, y=Block1)

labelOptovar = Label(root, text="Optovar", fg="Blue")
labelOptovar.place(x=10, y=Block1 + 25)
optovar = Entry(root, bg="White", fg="Blue", width=15)
optovar.insert(0, "None")
optovar.place(x=150, y=Block1 + 25)

Block2 = Block1 + 60

labelCamera = Label(root, text="Camera", fg="Blue")
labelCamera.place(x=10, y=Block2)
CameraList = []
for k, i in enumerate(CameraFormats.keys()):
    CameraList.append(Button(root, text=i, justify=CENTER, width=8))
    CameraList[k].place(x=150 + k * 80, y=Block2)
    CameraList[k].bind("<Button-1>", SelectCamera)

labelPixelSize = Label(root, text="Pixel size (in uM)", fg="Blue")
labelPixelSize.place(x=10, y=Block2 + 40)
pixel = Entry(root, bg="White", fg="Blue", width=15)
pixel.place(x=150, y=Block2 + 40)

numberPixelx = Label(root, text="Number of pixels in X", fg="Blue")
numberPixelx.place(x=10, y=Block2 + 65)
numPixelx = Entry(root, bg="White", fg="Blue", width=15)
numPixelx.place(x=150, y=Block2 + 65)

numberPixely = Label(root, text="Number of pixels in Y", fg="Blue")
numberPixely.place(x=10, y=Block2 + 90)
numPixely = Entry(root, bg="White", fg="Blue", width=15)
numPixely.place(x=150, y=Block2 + 90)

Block3 = Block2 + 135
"""
StartButtons = []
EndButtons = []
for i in range(0, 4):
    StartButtons.append(Button(root, text=list(StartButtonsText)[i], justify=CENTER, width=10))
    EndButtons.append(Button(root, text=list(EndButtonsText)[i], justify=CENTER, width=10))
    StartButtons[i].place(x=10 + i * 90, y=Block3)
    EndButtons[i].place(x=10 + i * 90, y=Block3 + 30)
    StartButtons[i].bind("<Button-1>", clickAllStart)
    EndButtons[i].bind("<Button-1>", clickAllEnd)
"""

LoadParamButton = Button(root, text="Load Positions", width=20, height=1, justify=CENTER)
LoadParamButton.place(x=10, y=Block3)
LoadParamButton.bind("<Button-1>", LoadParam)

global positions
positions = StringVar()
positions.set(
    "X Start " + str(X1) + "; X End " + str(X2) + "\nY Start " + str(Y1) + "; Y End " + str(Y2) + "\nZ Start " + str(
        Z1) + "; Z End " + str(Z3) + "; Z interm " + str(Z2))
srcTxtLabel = Label(root, textvariable=positions, justify=LEFT)
srcTxtLabel.place(x=170, y=Block3 - 5)

Zoption = Checkbutton(root, text="Z triangulation", fg="Blue")
Zoption.place(x=10, y=Block3 + 65)

Block4 = Block3 + 95
numberOfTiles = Label(root, text="Number of Tiles", fg="Blue")
numberOfTiles.place(x=10, y=Block4)
numTile = []
for i in range(0, len(PossNumTiles)):
    numTile.append(
        Button(root, text=str(PossNumTiles[i]) + "x" + str(PossNumTiles[i]), width=4, height=1, justify=CENTER))
    numTile[i].place(x=i * 42 + 10, y=Block4 + 32)
    numTile[i].bind("<Button-1>", clickTile)

OverlapLabel = Label(root, text="Tile Overlap", fg="Blue")
OverlapLabel.place(x=10, y=Block4 + 75)
overlap = Scale(root, length=200, fg="Blue", troughcolor="White", activebackground="Blue", orient=HORIZONTAL,
                resolution=5)
overlap.set(10)
overlap.place(x=10, y=Block4 + 95)

Block5 = Block4 + 90
# A block can be added here


Block6 = Block5 + 60
numberOfWells = Label(root, text="Number of Wells", fg="Blue")
numberOfWells.place(x=10, y=Block6)
numWell = []
for i in range(0, 6):
    numWell.append(Button(root, text=list(PossNumWell)[i], width=3, height=1, justify=CENTER))
    numWell[i].place(x=i * 35 + 10, y=Block6 + 25)
    numWell[i].bind("<Button-1>", clickNumWell)

Block7 = Block6 + 110

WellButtonList = []
counter = 0
for i in range(0, 16):
    for j in range(0, 24):
        WellButtonList.append(
            Button(root, text=col[i] + str(j + 1), width=3, height=1, justify=CENTER, disabledforeground="White",
                   state=NORMAL))
        WellButtonList[counter].place(x=j * 35 + 50, y=i * 30 + Block7)
        WellButtonList[counter].bind("<Button-1>", click)
        counter = counter + 1

WellRowList = []
for i in range(0, len(col)):
    WellRowList.append(Button(root, text=col[i], width=3, height=1, justify=CENTER, disabledforeground="White"))
    WellRowList[i].place(x=10, y=i * 30 + Block7)
    WellRowList[i].bind("<Button-1>", clickRow)

WellColList = []
for i in range(0, 24):
    WellColList.append(Button(root, text=str(i + 1), width=3, height=1, justify=CENTER, disabledforeground="White"))
    WellColList[i].place(x=i * 35 + 50, y=Block7 - 35)
    WellColList[i].bind("<Button-1>", clickCol)

ALL = Button(root, text="ALL", width=3, height=1, justify=CENTER)
ALL.place(x=10, y=Block7 - 35)
ALL.bind("<Button-1>", clickALL)

CalcPosButton = Button(root, text="Calculate Position")
CalcPosButton.place(x=10, y=(rootHeight - 40))
CalcPosButton.config(bg="yellow green")
CalcPosButton.bind("<Button-1>", CalcPos)

quitButton = Button(root, text="Quit")
quitButton.bind("<Button-1>", Leave)
quitButton.config(bg="tomato")
quitButton.place(x=(rootWidth - 50), y=(rootHeight - 40))

root.title("Multi-Well Acquisition")
root.mainloop()
