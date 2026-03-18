import os
from tkinter import *
from tkinter.ttk import *


def main():

    MCG_VERSION = "build-0"
    FFMPEG_PATH = ".\\ffmpeg\\bin\\ffmpeg.exe"

    mainWindow = Tk()
    mainWindow.title("MCG " + MCG_VERSION)

    Label(mainWindow, text="Import File:").grid(row=0, sticky=W)
    Label(mainWindow, text="Export File:").grid(row=1, sticky=W)
    Button(mainWindow, text="Choose File", command=importFile).grid(
        row=0, column=1, sticky=W)
    Button(mainWindow, text="Save as", command=saveFile).grid(
        row=1, column=1, sticky=W)
    Label(mainWindow, text="Width(px):").grid(row=2, column=0, sticky=W)
    Label(mainWindow, text="Height(px):").grid(row=2, column=2, sticky=W)
    Label(mainWindow, text="Bitrate(kbps):").grid(row=2, column=4, sticky=W)
    width_spinbox = Spinbox(mainWindow, from_=0, to=300000, width=5)
    width_spinbox.grid(row=2, column=1, sticky=W)

    height_spinbox = Spinbox(mainWindow, from_=0, to=300000, width=5)
    height_spinbox.grid(row=2, column=3, sticky=W)

    bitrate_spinbox = Spinbox(mainWindow, from_=0, to=300000, width=5)
    bitrate_spinbox.grid(row=2, column=5, sticky=W)

    Button(mainWindow, text="Start", command=convert).grid(sticky=E)
    Button(mainWindow, text="Quit", command=quit).grid(sticky=E)



    mainWindow.mainloop()

if __name__ == "__main__":
    main()