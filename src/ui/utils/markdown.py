import os


def read_file(filepath):
    absolute_path = os.path.abspath(filepath)
    with open(absolute_path, "r", encoding="utf-8") as f:
        return f.read()
