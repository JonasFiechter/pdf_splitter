from src.raw.pdf_splitter import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, \
                            QApplication, \
                            QMessageBox
from src.components.file_name_form import FileNameForm
from src.components.file_dialog import open_file, get_path
from src.components.services import pdf_splitter, pdf_merger, count_pdf_pages
from PyQt6.QtWidgets import QWidget
import sys, os


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.reset_state()
        # General Buttons
        self.open_file_btn.clicked.connect(lambda: self.select_file())
        self.split_radio_btn.clicked.connect(self.radio_btn_interact)
        self.merge_radio_btn.clicked.connect(self.radio_btn_interact)
        self.destination_btn.clicked.connect(self.select_destination)
        self.execute_btn.clicked.connect(self.execute_operation)

        # Custom options
        self.custom_check_btn.clicked.connect(self.custom_mode_check)
        self.range_radio_btn.clicked.connect(self.custom_btn_interact)
        self.range_radio_btn_2.clicked.connect(self.custom_btn_interact)

        # Other variables
        self.path = os.getcwd()
        self.destination_label.setText(f'Destination: {self.path}')
        self.setWindowTitle("TCP - PDF Splitter")
        self.open_file_btn.setDisabled(True)
        self.file_name = ""

        # Instance of Filename form
        self.file_name_widget = QWidget()
        self.file_name_app = FileNameForm(self.file_name_widget)

    # Buttons and fields
    def lock_buttons(self):
        self.execute_btn.setDisabled(True)
        self.lock_custom_radio_btns()
        self.lock_list_entry()
        self.lock_range_fields()
        self.lock_apply_btn()
        self.lock_custom_check_btn()
    
    def lock_custom_check_btn(self):
        self.custom_check_btn.setEnabled(False)

    def lock_custom_radio_btns(self):
        self.range_radio_btn.setEnabled(False)
        self.range_radio_btn_2.setEnabled(False)

    def lock_list_entry(self):
        self.list_entry.setEnabled(False)
    
    def lock_range_fields(self):
        self.starting_page.setEnabled(False)
        self.ending_page.setEnabled(False)

    def lock_apply_btn(self):
        self.apply_btn.setEnabled(False)

    def unlock_buttons(self):
        self.execute_btn.setEnabled(True)

    def radio_btn_interact(self):
        self.reset_state()
        self.open_file_btn.setEnabled(True)
        if self.split_radio_btn.isChecked():
            self.custom_check_btn.setEnabled(True)
        else:
            self.custom_check_btn.setEnabled(False)
        self.update_page()

    def select_destination(self):
        self.path = get_path(self)
        self.update_label(path=self.path)

    def custom_btn_interact(self):
        if self.range_radio_btn.isChecked():
            self.list_entry.setEnabled(False)
            self.starting_page.setEnabled(True)
            self.ending_page.setEnabled(True)
        elif self.range_radio_btn_2.isChecked():
            self.list_entry.setEnabled(True)
            self.starting_page.setEnabled(False)
            self.ending_page.setEnabled(False)
        self.update_page()
    
    def custom_mode_check(self):
        if self.custom_check_btn.isChecked():
            self.range_radio_btn.setEnabled(True)
            self.range_radio_btn_2.setEnabled(True)
            self.custom_btn_interact()
        else:
            self.lock_custom_radio_btns()
            self.lock_list_entry()
            self.lock_range_fields()


    # Functions
    def select_file(self):
        self.selected_files = open_file(self)
        self.update_page()

    def update_label(self, message='', path=''):
        if message:
            self.status_label.setText(message)
        elif path:
            self.destination_label.setText(f'Destination: {path}')

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
            total_pages = count_pdf_pages(pdf_files=self.selected_files)
            message=f'Selected {len(self.selected_files)} file(s)' \
                    f' | Total pages - {total_pages}'
            self.unlock_buttons()

        self.update_label(message=message)

    def execute_operation(self):
        if self.split_radio_btn.isChecked():
            pdf_splitter(self, self.selected_files[0], 'range_here')

            self.success_dialog()

        elif self.merge_radio_btn.isChecked():
            self.pages = count_pdf_pages(self.selected_files)
            self.open_file_name_form()

    def success_dialog(self):
        dialog = QMessageBox(self)
        dialog.setText("Success!")
        dialog.show()
        button_ok = dialog.buttons()[0]
        button_ok.clicked.connect(self.reset_state)

    def reset_state(self):
        self.lock_buttons()
        self.progress = 0
        self.pages = 0
        self.progressBar.setValue(self.progress)
        self.selected_files = []

    def open_file_name_form(self):
        self.file_name_widget.show()
        self.file_name_app.file_name_btn.clicked.connect(self.get_file_name)

    def get_file_name(self):
        self.file_name = self.file_name_app.file_name_input.text()
        if self.file_name:
            pdf_merger(self, file_name=self.file_name, pdf_files=self.selected_files)
            self.file_name_widget.close()
            self.success_dialog()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()