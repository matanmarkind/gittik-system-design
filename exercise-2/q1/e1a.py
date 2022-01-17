import os, pathlib

def file_sizes():
    return {i.name : i.stat().st_size for i in pathlib.Path(os.getcwd()).iterdir() if i.is_file()}

