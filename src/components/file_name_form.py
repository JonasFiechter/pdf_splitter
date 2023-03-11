from src.raw.file_name_input import Ui_Form

class FileNameForm(Ui_Form):
    def __init__(self, object):
        super().__init__()
        super().setupUi(Form=object)
