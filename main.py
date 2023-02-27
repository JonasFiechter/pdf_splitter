from src.raw.pdf_splitter import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.pushButton.clicked.connect(self.update_print)

    def update_print(self):
        print(self.radioButton.isChecked())
        path_test = QFileDialog.getOpenFileNames(self, "Select files", r"", "PDF files (*.pdf)")
        print(path_test)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()