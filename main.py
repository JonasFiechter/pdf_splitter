from src.raw.pdf_splitter import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, \
                            QApplication, \
                            QMessageBox
from src.components.file_name_form import FileNameForm
from src.components.file_dialog import open_file, get_path
from src.components.services import pdf_splitter, pdf_merger, count_pdf_pages
from PyQt6.QtWidgets import QWidget
import sys, os

#TODO: Check with button apply and with execute the selected pages before run
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
        self.custom_check_btn.stateChanged.connect(self.update_page)
        self.range_radio_btn.clicked.connect(self.update_page)
        self.range_radio_btn_2.clicked.connect(self.update_page)
        self.apply_btn.clicked.connect(self.apply_configuration)

        # Other variables
        self.setFixedSize(599, 318)
        self.path = os.getcwd()
        self.destination_label.setText(f'Destination: {self.path}')
        self.setWindowTitle("TCP - PDF Splitter")
        self.open_file_btn.setDisabled(True)
        self.file_name = ""
        self.pages_range = []

        # Instance of Filename form
        self.file_name_widget = QWidget()
        self.file_name_app = FileNameForm(self.file_name_widget)

    # Buttons and fields
    def lock_buttons(self):
        self.execute_btn.setDisabled(True)
        self.range_radio_btn.setDisabled(True)
        self.range_radio_btn_2.setDisabled(True)
        self.list_entry.setDisabled(True)
        self.starting_page.setDisabled(True)
        self.ending_page.setDisabled(True)
        self.apply_btn.setDisabled(True)
        self.custom_check_btn.setDisabled(True)

    def unlock_buttons(self):
        self.execute_btn.setEnabled(True)
        self.apply_btn.setEnabled(True)

    # Check and switch between split and merge options;
    def radio_btn_interact(self):
        self.reset_state()
        self.open_file_btn.setEnabled(True)
        if self.split_radio_btn.isChecked():
            self.custom_check_btn.setEnabled(True)
        else:
            self.custom_check_btn.setDisabled(True)
        self.update_page()

    def select_destination(self):
        self.path = get_path(self)
        self.update_label(path=self.path)


    def apply_configuration(self):
        
        pass

    # Functions
    def select_file(self):
        self.selected_files = open_file(self)
        self.update_page()

    def update_label(self, message='', path=''):
        if message:
            self.status_label.setText(message)
        elif path:
            self.destination_label.setText(f'Destination: {path}')

    # Check for faults and update the window behavior;
    def update_page(self):
        print('running update_page')

        # Verify and switch between range fields and list of pages;
        if self.range_radio_btn.isChecked():
            self.list_entry.setDisabled(True)
            self.starting_page.setEnabled(True)
            self.ending_page.setEnabled(True)
        elif self.range_radio_btn_2.isChecked():
            self.list_entry.setEnabled(True)
            self.starting_page.setDisabled(True)
            self.ending_page.setDisabled(True)

        # Verify and enables or disables custom functionalities
        if self.custom_check_btn.isChecked():
            self.range_radio_btn.setEnabled(True)
            self.range_radio_btn_2.setEnabled(True)
        else:
            self.range_radio_btn.setDisabled(True)
            self.range_radio_btn_2.setDisabled(True)
            self.list_entry.setDisabled(True)
            self.starting_page.setDisabled(True)
            self.ending_page.setDisabled(True)
            
        if self.selected_files and self.custom_check_btn.isChecked():
            self.apply_btn.setEnabled(True)
        else:
            self.apply_btn.setDisabled(True)

        #   Verify state of selected files and options
        if not self.selected_files and self.split_radio_btn.isChecked():
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
            self.execute_btn.setEnabled(True)
        
        self.update_label(message=message)

    def execute_operation(self):
        if self.split_radio_btn.isChecked():
            pdf_splitter(self, self.selected_files[0], 'range_here')
            self.success_dialog()
            self.radio_btn_interact()

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