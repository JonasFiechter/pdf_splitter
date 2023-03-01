from PyQt6.QtWidgets import QFileDialog


def open_file(widget, *args):
    current_path = QFileDialog.getOpenFileName(widget, 'Open File', filter='*pdf')
    print(current_path)

def open_files(widget, *args):
    current_path = QFileDialog.getOpenFileNames(widget, 'Open Files', filter='*pdf')
    print(current_path)