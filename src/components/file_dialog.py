from PyQt6.QtWidgets import QFileDialog, QDialog


def open_file(widget, *args):
    if widget.split_radio_btn.isChecked():
        temp_path = QFileDialog.getOpenFileName(
                                                    widget, 
                                                    'Open File', 
                                                    filter='*pdf'
                                                    )[0]
        current_path = [temp_path]
        if current_path[0] == '':
            current_path = []
    else:
        current_path = QFileDialog.getOpenFileNames(
                                                    widget, 
                                                    'Open Files', 
                                                    filter='*pdf'
                                                    )[0]
    return current_path

def get_path(widget, *args):
    path = QFileDialog.getExistingDirectory(widget, 'Select destination')
    return path