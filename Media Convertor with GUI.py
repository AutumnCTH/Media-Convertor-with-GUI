import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox


def main():
    def importFile():
        nonlocal pathImport
        pathImport = filedialog.askopenfilename()
        Label(MainWindow, text=fr"{pathImport}").grid(row=0, column=2, sticky=W)


    def saveFile():
        pass

    def convert():
        pass

    MCG_VERSION = "build"
    PATH_FFMPEG = ".\\ffmpeg\\bin\\ffmpeg.exe"
    pathImport = NONE
    pathExport = NONE

    MainWindow = Tk()
    MainWindow.title("MCG " + MCG_VERSION)

    Label(MainWindow, text="Import File:").grid(row=0, sticky=W)
    Label(MainWindow, text="Export File:").grid(row=1, sticky=W)
    Button(MainWindow, text="Choose File", command=importFile).grid(
        row=0, column=1, sticky=W)
    Button(MainWindow, text="Save as", command=saveFile).grid(
        row=1, column=1, sticky=W)
    Label(MainWindow, text="Width(px):").grid(row=2, column=0, sticky=W)
    Label(MainWindow, text="Height(px):").grid(row=2, column=2, sticky=W)
    Label(MainWindow, text="Bitrate(kbps):").grid(row=2, column=4, sticky=W)

    WidthSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    WidthSpinbox.grid(row=2, column=1, sticky=W)

    HeightSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    HeightSpinbox.grid(row=2, column=3, sticky=W)

    BitrateSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    BitrateSpinbox.grid(row=2, column=5, sticky=W)

    Button(MainWindow, text="Start", command=convert).grid(sticky=E)
    Button(MainWindow, text="Quit", command=quit).grid(sticky=E)


    MainWindow.mainloop()

if __name__ == "__main__":
    main()