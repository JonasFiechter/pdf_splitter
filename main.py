from src.raw.pdf_splitter import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
from src.components.file_dialog import open_file, get_path
from src.components.progress_bar import fill_progress_bar
import sys, os


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.lock_buttons()
        self.progressBar.setValue(0)
        self.open_file_btn.clicked.connect(lambda: self.select_file())
        self.split_radio_btn.clicked.connect(self.radio_btn_interact)
        self.merge_radio_btn.clicked.connect(self.radio_btn_interact)
        self.destination_btn.clicked.connect(self.select_destination)
        self.execute_btn.clicked.connect(self.execute_operation)
        self.path = os.getcwd()
        self.destination_label.setText(f'Destination: {self.path}')
        self.selected_files = []

    def lock_buttons(self):
        self.open_file_btn.setDisabled(True)
        self.open_file_btn.disconnect()
        self.execute_btn.setDisabled(True)

    def unlock_buttons(self):
        self.execute_btn.setEnabled(True)

    def radio_btn_interact(self):
        self.open_file_btn.setEnabled(True)
        self.open_file_btn.setEnabled(True)
        self.update_page()

    def select_destination(self):
        self.path = get_path(self)
        self.update_label(path=self.path)

    def update_label(self, message='', path=''):
        if message:
            self.status_label.setText(message)
        elif path:
            self.destination_label.setText(f'Destination: {path}')

    def select_file(self):
        self.selected_files = open_file(self)
        self.update_page()

    def update_page(self):
        if len(self.selected_files) == 0 and self.split_radio_btn.isChecked():
            message = f'Select a PDF file!'
            self.execute_btn.setDisabled(True)
        elif len(self.selected_files) > 1 and self.split_radio_btn.isChecked():
            message = f'Split one file at a time!'
            self.execute_btn.setDisabled(True)
        elif self.merge_radio_btn.isChecked() and len(self.selected_files) < 2:
            message = f'Select more files to merge!'
            self.execute_btn.setDisabled(True)
        else:
            message=f'Selected {len(self.selected_files)} file(s)'
            self.unlock_buttons()

        self.update_label(message)

    def execute_operation(self):
        fill_progress_bar(self, 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()