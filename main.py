from src.raw.pdf_splitter import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
from src.components.file_dialog import open_file, open_files

from time import sleep
import sys


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.pushButton.clicked.connect(lambda: open_files(self))
        self.progressBar.setValue(0)

    def lock_buttons(self):
        self.pushButton.setDisabled(True)
        self.pushButton.disconnect()

    def unlock_buttons(self):
        self.pushButton.setEnabled(True)
        self.pushButton.clicked.connect(self.fill_progress_bar)

    def fill_progress_bar(self, total_iterations):
        self.lock_buttons()
        percentage_total = 100 // total_iterations
        percentage_total_rest = 100 % total_iterations
        current_progress = 0
        for i in range(total_iterations):
            current_progress += percentage_total
            sleep(0.05)
            print(current_progress)
            self.progressBar.setValue(current_progress)
        
        current_progress += percentage_total_rest
        self.progressBar.setValue(current_progress)
        
        if current_progress == 100:
            # Here we should call a success dialog box function;
            # A function that receives the operation and the message would 
            # work fine;
            pass

        self.unlock_buttons()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()