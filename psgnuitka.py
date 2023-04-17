import PySimpleGUI
import pathlib
import subprocess
import time
import locale
import os


def collectinfomation() -> dict:
    info = dict()
    sys_language = locale.getlocale()[0]
    language_code = locale.getpreferredencoding(do_setlocale=False)
    if sys_language == "Chinese (Simplified)_China":
        sys_language = "zh_CN"
    info['sys_language'] = sys_language
    info['language_code'] = language_code
    return info


def runbuildcommand(command: str, window: PySimpleGUI.Window = None, timeout: int = None, system_encode: str = None) -> tuple:
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # if PySimpleGUI.running_windows():
    #     # command = shlex.split(command)
    #     p = subprocess.Popen(
    #         command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # else:
    #     command = shlex.split(command)
    #     p = subprocess.Popen(
    #         command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        # line = line.decode('cp936', errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        line = line.decode(system_encode)
        output += line
        print(line, end="", flush=True)
        window.Refresh() if window else None  # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return retval, output  # also return the output just for fun


if __name__ == '__main__':
    sys_info = collectinfomation()
    PySimpleGUI.theme("DarkGrey6")
    all_text = {
        "en_US": {
            "PYTHON-PATH": "Select Python Interpreter",
            "FileBrowse-Button": "Browse File",
            "FolderBrowse-Button": "Browse Dir",
            "PY-PATH": "Select Python Script"
        },
        "zh_CN": {
            "PYTHON-PATH": "使用的Python解释器位置",
            "FileBrowse-Button": "选择文件",
            "FolderBrowse-Button": "选择目录",
            "PY-PATH": "选择Python脚本文件",
        }
    }
    text=all_text.get(sys_info['sys_language'],"zh_CN")
    # text=all_text[sys_info['sys_language']]

    # 主体布局
    main_layout = [
        [
            PySimpleGUI.Text(text["PYTHON-PATH"]
                             ), PySimpleGUI.Input(key="PYTHON-PATH"),
            PySimpleGUI.FileBrowse(button_text=text['FileBrowse-Button'], file_types=[("", "python.exe python")],
                                   target="PYTHON-PATH"), PySimpleGUI.Text(text["PY-PATH"]),
            PySimpleGUI.Input(key="PY-PATH"),
            PySimpleGUI.FileBrowse(button_text=text['FileBrowse-Button'], file_types=[("", "*.py")], target="PY-PATH")],
        [
        ],
        [
            PySimpleGUI.Text("构建生成目录"),
            PySimpleGUI.Input(key="OUTPUT-DIR"),
            PySimpleGUI.FolderBrowse(button_text=text['FolderBrowse-Button'],
                                     target="OUTPUT-DIR"),
            PySimpleGUI.Text("可执行文件名"),
            PySimpleGUI.Input(key="OUTPUT-FILENAME"),
        ],
        [
            PySimpleGUI.Frame("C编译器选择", layout=[[
                PySimpleGUI.Radio(group_id="CCOMPILER",
                                  text="MingW64", default=True, key="MINGW64"),
                PySimpleGUI.Radio(group_id="CCOMPILER",
                                  text="Clang", default=False, key="CLANG"),
                PySimpleGUI.Radio(group_id="CCOMPILER",
                                  text="MSVC", default=False, key="MSVC"),
            ]]),
            PySimpleGUI.Frame("单文件模式", layout=[[
                PySimpleGUI.Checkbox(
                    text="onefile", default=False, key="ONEFILE")
            ]]),
            PySimpleGUI.Frame("是否控制台可用", layout=[[
                PySimpleGUI.Radio(group_id="CONSOLE", text="enable",
                                  default=True, key="ENABLE-CONSOLE"),
                PySimpleGUI.Radio(group_id="CONSOLE", text="disable",
                                  default=False, key="DISABLE-CONSOLE"),
            ]]),
            PySimpleGUI.Frame("工具链来源选择", layout=[[
                PySimpleGUI.Radio(group_id="TOOLCHAINFROM", text="使用系统环境路径", default=False,
                                  key="SYSTEMTOOLCHAIN"),
                PySimpleGUI.Radio(group_id="TOOLCHAINFROM", text="使用本工具自带版本", default=False,
                                  key="LOCALTOOLCHAIN", disabled=True),
                PySimpleGUI.Radio(group_id="TOOLCHAINFROM", text="由nuitka自动下载处理", default=True,
                                  key="NUITKATOOLCHAIN"),
            ]]),
        ],
        [
            PySimpleGUI.Frame("额外插件", layout=[
                [
                    PySimpleGUI.Checkbox(
                        text="eventlet", default=False, key="EVENTLET"),
                    PySimpleGUI.Checkbox(
                        text="gevent", default=False, key="GEVENT"),
                    PySimpleGUI.Checkbox(text="gi", default=False, key="GI"),
                    PySimpleGUI.Checkbox(
                        text="glfw", default=False, key="GLFW"),
                    PySimpleGUI.Checkbox(
                        text="kivy ", default=False, key="KIVY"),

                ],
                [
                    PySimpleGUI.Checkbox(
                        text="matplotlib", default=False, key="MATPLOTLIB"),
                    PySimpleGUI.Checkbox(
                        text="no-qt", default=False, key="NO-QT"),
                    PySimpleGUI.Checkbox(
                        text="numpy", default=False, key="NUMPY"),
                    PySimpleGUI.Checkbox(
                        text="pmw-freezer", default=False, key="PMW-FREEZER"),
                    PySimpleGUI.Checkbox(
                        text="pylint-warnings", default=False, key="PYLINT-WARNINGS"),

                ],
                [

                    PySimpleGUI.Checkbox(
                        text="pyqt5", default=False, key="PYQT5"),
                    PySimpleGUI.Checkbox(
                        text="pyqt6", default=False, key="PYQT6"),
                    PySimpleGUI.Checkbox(
                        text="pyside2", default=False, key="PYSIDE2"),
                    PySimpleGUI.Checkbox(
                        text="pyside6", default=False, key="PYSIDE6"),
                    PySimpleGUI.Checkbox(
                        text="pywebview", default=False, key="PYWEBVIEW"),

                ],
                [

                    PySimpleGUI.Checkbox(
                        text="tensorflow", default=False, key="TENSORFLOW"),
                    PySimpleGUI.Checkbox(
                        text="tk-inter", default=False, key="TK-INTER"),
                    PySimpleGUI.Checkbox(
                        text="torch", default=False, key="TORCH"),
                    PySimpleGUI.Checkbox(
                        text="trio", default=False, key="TRIO"),
                    PySimpleGUI.Checkbox(text="upx", default=False, key="UPX"),

                ],
                [

                ]
            ]),
        ],
        [
            PySimpleGUI.Frame("需要的数据文件", expand_x=True, layout=[
                [PySimpleGUI.Table(values=[[]], headings=["添加列表"], key="DATA-TABLE",
                                   expand_x=True, justification="left")],
                [PySimpleGUI.Button("添加文件", key="ADD-DATA-FILE"),
                 PySimpleGUI.Button("添加目录", key="ADD-DATA-DIR"),
                 PySimpleGUI.Button("添加指定模块的所有数据文件", key="ADD-DATA-PACKAGE"),
                 PySimpleGUI.Button("删除选中", key="DEL-DATA-TABLE")]
            ]),
            PySimpleGUI.Frame("需要的模块", expand_x=True, layout=[
                [PySimpleGUI.Table(values=[[]], headings=["添加列表"], key="MODULE-TABLE",
                                   expand_x=True, justification="left")],
                [PySimpleGUI.Button("指定需要导入的模块", key="ADD-MODULE-NAME"),
                 PySimpleGUI.Button("指定不希望导入的模块", key="NO-MODULE-NAME"),
                 PySimpleGUI.Button("删除选中", key="DEL-MODULE-TABLE")]
            ])
        ],

        [
            PySimpleGUI.Text("构建命令:")
        ],
        [
            PySimpleGUI.Multiline(
                key="BUILD-CMD", size=(160, 4), expand_x=True, expand_y=True)
        ],
        [
            PySimpleGUI.Text("显示输出:"),

        ],
        [
            PySimpleGUI.Output(key="BUILD-OUTPUT",
                               size=(160, 8), expand_x=True, expand_y=True)
        ],
        [
            PySimpleGUI.Button(button_text="生成构建命令", key="GENERATE-CMD"),
            PySimpleGUI.Button(button_text="构建", key="BUILD"),
            PySimpleGUI.Button(button_text="退出", key="EXIT")
        ]
    ]
    window = PySimpleGUI.Window(title="psgnuitka", layout=main_layout, font="_ 14", resizable=True,
                                auto_size_text=True, auto_size_buttons=True, scaling=1.0,)

    data_table = []
    module_table = []
    build_cmd = ""
    start_time = 0
    stop_time = 0
    i = 0
    while True:
        event, values = window.read(timeout=10)
        if event in [PySimpleGUI.WINDOW_CLOSED, "EXIT"]:
            break
        if event == "GENERATE-CMD":
            cmd = list()
            cmd.append(str(pathlib.Path(values['PYTHON-PATH']).absolute()))
            cmd.append('-m')
            cmd.append('nuitka')
            if values["MINGW64"] is True:
                cmd.append("--mingw64")
            elif values["CLANG"] is True:
                cmd.append("--clang")
            elif values["MSVC"] is True:
                cmd.append("--MSVC")
            if values["ONEFILE"] is True:
                cmd.append("--onefile")
            cmd.append("--standalone")
            if values["DISABLE-CONSOLE"] is True:
                cmd.append("--disable-console")
            if len(module_table) != 0:
                for i in module_table:
                    cmd.append(i[0])
            if len(data_table) != 0:
                for i in data_table:
                    cmd.append(i[0])
            plugin_list = ["eventlet", "gevent", "gi", "glfw", "kivy", "matplotlib", "no-qt", "numpy", "pmw-freezer",
                           "pylint-warnings", "pyqt5", "pyqt6", "pyside2", "pyside6", "pywebview", "tensorflow",
                           "tk-inter", "torch", "trio", "upx"]
            for plugin in plugin_list:
                if values[plugin.upper()] is True:
                    cmd.append("--enable-plugin=" + plugin)
            if values["NUITKATOOLCHAIN"] is True:
                cmd.append("--assume-yes-for-downloads")
            if values["OUTPUT-FILENAME"]:
                cmd.append("--output-filename=" + values["OUTPUT-FILENAME"])
            if values["OUTPUT-DIR"]:
                cmd.append("--output-dir=" +
                           str(pathlib.Path(values["OUTPUT-DIR"]).absolute()))
            # cmd.append("--remove-output")
            # cmd.append("--verbose")
            cmd.append(str(pathlib.Path(values['PY-PATH']).absolute()))
            build_cmd = " ".join(cmd)
            window['BUILD-CMD'].update(build_cmd)
            # print(os.environ.get("PYTHONHOME"), os.environ.get("PYTHONPATH"))
            # PySimpleGUI.popup_get_file(message="选择要添加的文件", no_window=True)
        if event == "ADD-DATA-FILE":
            file_path = PySimpleGUI.popup_get_file(message="", no_window=True,keep_on_top=True)
            if file_path:
                file_name = PySimpleGUI.popup_get_text(
                    message="添加的文件名为", default_text=file_path.split("/")[-1], font="_ 14",keep_on_top=True)
                data_table.append(
                    ["--include-data-files=" + str(pathlib.Path(file_path).absolute()) + "=" + file_name])
                window["DATA-TABLE"].update(values=data_table)
            else:
                continue
        if event == "ADD-DATA-DIR":
            dir_path = PySimpleGUI.popup_get_folder(message="", no_window=True,keep_on_top=True)
            if dir_path:
                dir_name = PySimpleGUI.popup_get_text(message="添加的目录名为",
                                                      default_text=dir_path.split("/")[-1], font="_ 14",keep_on_top=True)
                data_table.append(
                    ["--include-data-dir=" + str(pathlib.Path(dir_path).absolute()) + "=" + dir_name])
                window["DATA-TABLE"].update(values=data_table)
            else:
                continue
        if event == "ADD-DATA-PACKAGE":
            package_name = PySimpleGUI.popup_get_text(
                message="添加指定模块数据", font="_ 14",keep_on_top=True)
            if package_name:
                data_table.append(["--include-package-data=" + package_name])
                window["DATA-TABLE"].update(values=data_table)
            else:
                continue
        if event == "DEL-DATA-TABLE":
            if values["DATA-TABLE"]:
                if len(data_table) != 0:
                    data_table.pop(values["DATA-TABLE"][0])
                    window["DATA-TABLE"].update(values=data_table)
            else:
                continue
        if event == "ADD-MODULE-NAME":
            module_name = PySimpleGUI.popup_get_text(
                message="希望导入的模块", font="_ 14",keep_on_top=True)
            if module_name:
                module_table.append(["--follow-import-to=" + module_name])
                window["MODULE-TABLE"].update(values=module_table)
            else:
                continue
        if event == "NO-MODULE-NAME":
            module_name = PySimpleGUI.popup_get_text(
                message="不希望导入的模块", font="_ 14",keep_on_top=True)
            if module_name:
                module_table.append(["--nofollow-import-to=" + module_name])
                window["MODULE-TABLE"].update(values=module_table)
            else:
                continue
        if event == "DEL-MODULE-TABLE":
            if values["MODULE-TABLE"]:
                if len(module_table) != 0:
                    module_table.pop(values["MODULE-TABLE"][0])
                    window["MODULE-TABLE"].update(values=module_table)
            else:
                continue
        if event == "BUILD":
            if build_cmd == "":
                PySimpleGUI.PopupError(f"出错了，请先生成构建命令", font="_ 14",keep_on_top=True)
                continue
            if PySimpleGUI.running_windows():
                os.environ["PYTHONPATH"] = str(pathlib.Path(
                    values['PYTHON-PATH']).absolute().parent)
                os.environ["PYTHONHOME"] = str(pathlib.Path(
                    values['PYTHON-PATH']).absolute().parent)
            start_time = time.perf_counter()
            window['BUILD'].update(disabled=True)
            window["BUILD-OUTPUT"].update("")
            # ret = subprocess.run(build_cmd, shell=True)
            # print(build_cmd)
            window.perform_long_operation(lambda: runbuildcommand(
                command=build_cmd, window=window, system_encode=sys_info['language_code']), "BUILD-DONE")
            # stop_time = time.perf_counter()
            # use_time = round(stop_time - start_time, 2)
        if event == "BUILD-DONE":
            stop_time = time.perf_counter()
            use_time = round(stop_time - start_time, 2)
            # PySimpleGUI.PopupOK(f"处理完毕，用时{use_time}s", font="_ 14")
            window['BUILD'].update(disabled=False)
            # print(values["BUILD-DONE"])
            if values["BUILD-DONE"][0] == 0:
                PySimpleGUI.popup_ok(f"处理完毕，用时{use_time}s", font="_ 14",keep_on_top=True)
            else:
                PySimpleGUI.popup_error(
                    f"出错了，请对照输出检查信息，用时{use_time}s", font="_ 14",keep_on_top=True)
    window.close()
