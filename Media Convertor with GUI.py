from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from subprocess import Popen
import os


def main():
    def sysCommand(inputCommand: list):
        """调用shell"""

        shellResult = Popen(inputCommand)
        return shellResult.returncode

    def importFile():
        """向用户请求导入文件路径"""

        nonlocal pathImport
        pathImport.getValue(filedialog.askopenfilename(filetypes=videoFiletypes))
        pathImport.loadPara()

    def saveFile():
        """向用户请求导出文件路径"""

        nonlocal pathExport, saveType
        pathExport.getValue(
            filedialog.asksaveasfilename(
                filetypes=videoFiletypes, typevariable=saveType, defaultextension=".mp4"
            )
        )
        pathExport.isTypeSupported()
        pathExport.loadPara()

    def loadConfig():
        """读取用户指定配置"""

        pathLoadConfig = filedialog.askopenfilename(filetypes=configFiletypes)
        if not pathLoadConfig:
            return
        configFile = open(pathLoadConfig, "r")

        for i in configList:
            line = configFile.readline()
            if line.endswith("\n"):
                line = line[:-1]  # 删除换行符

            i.getValue(line)
            i.loadPara()

    def saveConfig():
        """向用户请求导出配置文件"""

        pathSaveConfig = filedialog.asksaveasfilename(filetypes=configFiletypes)
        if not pathSaveConfig:
            return
        getParameters()
        configFile = open(pathSaveConfig, "w")
        for i in configList:
            configFile.writelines(
                str(i.value) + "\n"
            )  # VSCode检测不到i作为实例的成员value，实际可以运行
        configFile.close()

    def getParameters():
        """刷新参数"""

        nonlocal width, height, bitrate, pathImport, pathExport

        width.getValue(WidthSpinbox.get())
        height.getValue(HeightSpinbox.get())
        bitrate.getValue(BitrateSpinbox.get())
        pathImport.getValue(ImportPathEntry.get())
        pathExport.getValue(ExportPathEntry.get())

    def convert():
        """调用ffmpeg"""

        getParameters()
        if not (
            (pathImport.checkPath() and pathExport.checkDir())
            and (pathImport.isTypeSupported() and pathExport.isTypeSupported())
        ):
            return
        convertCmd = [
            PATH_FFMPEG,
            "-y",
            "-i",
            pathImport.value,
            "-b:v",
            f"{bitrate.value}k",
            "-s",
            f"{width.value}x{height.value}",
            pathExport.value,
        ]
        sysCommand(convertCmd)

    class ParameterSpinbox(Spinbox):
        def __init__(
            self, master=None, row=0, from_=0, to=300000, width=6, values=None, text=""
        ):
            super().__init__(master, from_=from_, to=to, width=width)
            self.grid(row=row, column=1, sticky=W)
            self.set(values)
            self.bind("<Key>", self.spinboxOnlyNumber)  # 阻止向Spinbox内输入非数字
            Label(MainWindow, text=text).grid(row=row, column=0, sticky=W)

        def spinboxOnlyNumber(self, event):
            """阻止向Spinbox内输入非数字"""
            allowedKeys = [
                "BackSpace",
                "Delete",
                "Left",
                "Right",
                "Up",
                "Down",
                "Home",
                "End",
            ]
            if not event.char.isdigit() and event.keysym not in allowedKeys:
                return "break"

    class ConfigParameter:
        value = None
        widget = None

        def __init__(self, widget=None):
            self.widget = widget

        def getValue(self, value):
            self.value = str(value)

        def loadPara(self):
            self.widget.set(self.value)

    class ConfigPath(ConfigParameter):
        typeList = [".mp4", ".mkv", ".flv", ".mov"]
        def loadPara(self):
            self.widget.delete(0, END)
            self.widget.insert(0, self.value)

        def checkPath(self):
            if not os.path.exists(self.value):
                messagebox.showerror(
                    title="pathErr",
                    message="The path of file to import doesn't existed!",
                )
                return False
            return True

        def checkDir(self):
            if not os.path.isdir(os.path.dirname(self.value)):
                messagebox.showerror(
                    title="pathErr",
                    message="The path of file to export doesn't existed!",
                )
                return False
            return True

        def isTypeSupported(self):
            for i in self.typeList:
                if self.value.endswith(i):
                    return True
            messagebox.showerror(title="typeErr", message="The type isn't supported!")
            return False
        
        def completeTypeName(self):
            for i in self.typeList:
                if self.value.endswith(i):
                    return
            self.value += typeDict[saveType.get()]

    MCG_VERSION = "dev"
    PATH_FFMPEG = ".\\ffmpeg\\bin\\ffmpeg.exe"
    videoFiletypes = [
        ("MPEG-4", "*.mp4"),
        ("Flash Video", "*.flv"),
        ("Matroska Video", "*.mkv"),
        ("QuickTime", "*.mov"),
    ]
    configFiletypes = [("Config", "*.mcg")]
    typeDict = {
        "MPEG-4": ".mp4",
        "Flash Video": ".flv",
        "Matroska Video": ".mkv",
        "QuickTime": ".mov",
    }

    MainWindow = Tk()
    MainWindow.title("MCG " + MCG_VERSION)

    saveType = StringVar(MainWindow, "")

    Label(MainWindow, text="Import File:").grid(row=0, sticky=W)
    Button(MainWindow, text="Choose File", command=importFile).grid(
        row=0, column=1, sticky=W
    )
    ImportPathEntry = Entry(exportselection=0, width=60)
    ImportPathEntry.grid(row=0, column=2, sticky=W)

    Label(MainWindow, text="Export File:").grid(row=1, sticky=W)
    Button(MainWindow, text="Save as", command=saveFile).grid(row=1, column=1, sticky=W)
    ExportPathEntry = Entry(exportselection=0, width=60)
    ExportPathEntry.grid(row=1, column=2, sticky=W)

    WidthSpinbox = ParameterSpinbox(MainWindow, row=2, values=640, text="Width(px):")
    HeightSpinbox = ParameterSpinbox(MainWindow, row=3, values=360, text="Height(px):")
    BitrateSpinbox = ParameterSpinbox(
        MainWindow, row=4, values=500, text="Bitrate(kbps):"
    )

    pathImport = ConfigPath(ImportPathEntry)
    pathExport = ConfigPath(ExportPathEntry)
    width = ConfigParameter(WidthSpinbox)
    height = ConfigParameter(HeightSpinbox)
    bitrate = ConfigParameter(BitrateSpinbox)
    configList = [pathImport, pathExport, width, height, bitrate]

    Button(MainWindow, text="Save Config", command=saveConfig).grid(
        row=5, column=0, sticky=W
    )
    Button(MainWindow, text="Load Config", command=loadConfig).grid(
        row=5, column=1, sticky=W
    )
    Button(MainWindow, text="Start", command=convert).grid(row=4, column=2, sticky=E)
    Button(MainWindow, text="Quit", command=quit).grid(row=5, column=2, sticky=E)

    MainWindow.mainloop()


if __name__ == "__main__":
    main()
