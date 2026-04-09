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
        pathImport.getValue(filedialog.askopenfilename())
        pathImport.loadPara()


    def saveFile():
        nonlocal pathImport, pathExport
        pathExport.getValue(filedialog.asksaveasfilename())
        pathExport.loadPara()


    def loadConfig():
        pathLoadConfig = filedialog.askopenfilename()
        configFile = open(pathLoadConfig, 'r')

        for i in configList:
            line = configFile.readline()
            if line.endswith('\n'):
                line = line[:-1]    #删除换行符

            i.getValue(line)
            i.loadPara()
            

    def saveConfig():
        pathSaveConfig = filedialog.asksaveasfilename()
        getParameters()
        configFile = open(pathSaveConfig, 'w')
        for i in configList:
            configFile.writelines(str(i.value) + "\n") #VSCode检测不到i作为实例的成员value，实际可以运行
        configFile.close()


    def getParameters():
        nonlocal width, height, bitrate, pathImport, pathExport

        width.getValue(int(WidthSpinbox.get()))
        height.getValue(int(HeightSpinbox.get()))
        bitrate.getValue(int(BitrateSpinbox.get()))
        pathImport.getValue(ImportPathEntry.get())
        pathExport.getValue(ExportPathEntry.get())


    def convert():
        getParameters()
        convertCmd = [PATH_FFMPEG, "-i", pathImport.value, "-b:v", f"{bitrate.value}k", "-s", f"{width.value}x{height.value}", pathExport.value]
        sysCommand(convertCmd)


    class ConfigParameter:
        value = None
        widget = None

        def __init__(self, spinbox = None):
            self.widget = spinbox

        def getValue(self, value):
            self.value = value

        def loadPara(self):
            self.widget.set(self.value)



    MCG_VERSION = "build"
    PATH_FFMPEG = ".\\ffmpeg\\bin\\ffmpeg.exe"
    

    MainWindow = Tk()
    MainWindow.title("MCG " + MCG_VERSION)

    Label(MainWindow, text="Import File:").grid(row=0, sticky=W)
    Button(MainWindow, text="Choose File", command=importFile).grid(row=0, column=1, sticky=W)
    ImportPathEntry = Entry(exportselection=0)
    ImportPathEntry.grid(row=0, column=2, sticky=W)

    Label(MainWindow, text="Export File:").grid(row=1, sticky=W)
    Button(MainWindow, text="Save as", command=saveFile).grid(
        row=1, column=1, sticky=W)
    ExportPathEntry = Entry(exportselection=0)
    ExportPathEntry.grid(row=1, column=2, sticky=W)

    Label(MainWindow, text="Width(px):").grid(row=2, column=0, sticky=W)
    Label(MainWindow, text="Height(px):").grid(row=3, column=0, sticky=W)
    Label(MainWindow, text="Bitrate(kbps):").grid(row=4, column=0, sticky=W)

    WidthSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    WidthSpinbox.grid(row=2, column=1, sticky=W)
    WidthSpinbox.set(640)

    HeightSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    HeightSpinbox.grid(row=3, column=1, sticky=W)
    HeightSpinbox.set(360)

    BitrateSpinbox = Spinbox(MainWindow, from_=0, to=300000, width=5)
    BitrateSpinbox.grid(row=4, column=1, sticky=W)
    BitrateSpinbox.set(500)

    pathImport = ConfigParameter(ImportPathEntry)
    pathExport = ConfigParameter(ExportPathEntry)
    width = ConfigParameter(WidthSpinbox)
    height = ConfigParameter(HeightSpinbox)
    bitrate = ConfigParameter(BitrateSpinbox)
    configList = [pathImport, 
        pathExport,
        width,
        height,
        bitrate]

    Button(MainWindow, text="Save Config", command=saveConfig).grid(row=5, column=0, sticky=W)
    Button(MainWindow, text="Load Config", command=loadConfig).grid(row=5, column=1, sticky=W)
    Button(MainWindow, text="Start", command=convert).grid(sticky=E)
    Button(MainWindow, text="Quit", command=quit).grid(sticky=E)


    MainWindow.mainloop()

    

if __name__ == "__main__":
    main()