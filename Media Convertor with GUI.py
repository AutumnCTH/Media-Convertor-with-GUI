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
        Label(MainWindow, text = pathImport.value).grid(row=0, column=2, sticky=W)


    def saveFile():
        nonlocal pathImport, pathExport
        pathExport.getValue(filedialog.asksaveasfilename())
        Label(MainWindow, text = pathExport.value).grid(row=1, column=2, sticky=W)


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
        nonlocal width, height, bitrate

        width.getValue(int(WidthSpinbox.get()))
        height.getValue(int(HeightSpinbox.get()))
        bitrate.getValue(int(BitrateSpinbox.get()))


    def convert():
        getParameters()
        convertCmd = [PATH_FFMPEG, "-i", pathImport.value, "-b:v", f"{bitrate.value}k", "-s", f"{width.value}x{height.value}", pathExport.value]
        sysCommand(convertCmd)


    class ConfigParameter:
        value = None

        def getValue(self, value):
            self.value = value


    class ConfigPath(ConfigParameter):
        def __init__(self, gridPosition):
            self.gridPosition = gridPosition

        def loadPara(self):
            Label(MainWindow, text=fr"{self.value}").grid(row=self.gridPosition, column=2, sticky=W)
                #gridPosition Import is 0, export = 1


    class ConfigInt(ConfigParameter):
        spinbox = None
        def __init__(self, spinbox = None):
            self.spinbox = spinbox

        def loadPara(self):
            self.spinbox.set(self.value)



    MCG_VERSION = "build"
    PATH_FFMPEG = ".\\ffmpeg\\bin\\ffmpeg.exe"
    

    MainWindow = Tk()
    MainWindow.title("MCG " + MCG_VERSION)

    Label(MainWindow, text="Import File:").grid(row=0, sticky=W)
    Label(MainWindow, text="Export File:").grid(row=1, sticky=W)
    Button(MainWindow, text="Choose File", command=importFile).grid(
        row=0, column=1, sticky=W)
    Button(MainWindow, text="Save as", command=saveFile).grid(
        row=1, column=1, sticky=W)
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

    pathImport = ConfigPath(0)
    pathExport = ConfigPath(1)
    width = ConfigInt(WidthSpinbox)
    height = ConfigInt(HeightSpinbox)
    bitrate = ConfigInt(BitrateSpinbox)
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