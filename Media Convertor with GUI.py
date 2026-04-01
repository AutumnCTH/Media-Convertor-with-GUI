from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from subprocess import Popen


def main():
    def sysCommand(inputCommand: list):
        shellResult = Popen(inputCommand)
        return shellResult.returncode
    
    def importFile():
        nonlocal pathImport
        pathImport = filedialog.askopenfilename()
        Label(MainWindow, text=fr"{pathImport}").grid(row=0, column=2, sticky=W)


    def saveFile():
        nonlocal pathImport, pathExport
        pathExport = filedialog.asksaveasfilename()
        Label(MainWindow, text=fr"{pathExport}").grid(row=1, column=2, sticky=W)


    def loadConfig():
        pathLoadConfig = filedialog.askopenfilename()
        configFile = open(pathLoadConfig, 'r')
        for i in configList:
            i = configFile.readline()


    def saveConfig():
        pathSaveConfig = filedialog.asksaveasfilename()
        getParameters()
        configFile = open(pathSaveConfig, 'w')
        
        for i in configList:
            configFile.writelines(str(i) + "\n")

        configFile.close()


    def getParameters():
        nonlocal width, height, bitrate

        width = WidthSpinbox.get()
        height = HeightSpinbox.get()
        bitrate = BitrateSpinbox.get()


    def convert():
        getParameters()
        convertCmd = [PATH_FFMPEG, "-i", pathImport, "-b:v", f"{bitrate}k", "-s", f"{width}x{height}", pathExport]
        sysCommand(convertCmd)


    MCG_VERSION = "build"
    PATH_FFMPEG = ".\\ffmpeg\\bin\\ffmpeg.exe"
    pathImport = None
    pathExport = None
    width = None
    height = None
    bitrate = None
    configList = [pathImport, 
                       pathExport,
                       width,
                       height,
                       bitrate]

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
    WidthSpinbox.insert(0, "640")

    HeightSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    HeightSpinbox.grid(row=2, column=3, sticky=W)
    HeightSpinbox.insert(0, "360")

    BitrateSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    BitrateSpinbox.grid(row=2, column=5, sticky=W)
    BitrateSpinbox.insert(0, "1000")

    Button(MainWindow, text="Save Config", command=saveConfig).grid(row=3, column=0, sticky=W)
    Button(MainWindow, text="Load Config", command=loadConfig).grid(row=3, column=1, sticky=W)
    Button(MainWindow, text="Start", command=convert).grid(sticky=E)
    Button(MainWindow, text="Quit", command=quit).grid(sticky=E)


    MainWindow.mainloop()

if __name__ == "__main__":
    main()