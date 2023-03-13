from PyPDF2 import PdfReader, PdfWriter
from src.components.progress_bar import fill_progress_bar
from time import sleep

#TODO: CHECK IF FILE NAMES ALREADY EXISTS, THIS FUNCTION CAN ERASE YOUR FILES

#   Function that makes the magic happen, will be implemented a range of
# starting and ending page so the user can choose which pages to split
def pdf_splitter(self, pdf_path, pages_range):
    pdf_file = PdfReader(f'{pdf_path}', 'rb')
    total_pages = len(pdf_file.pages)
    pdf_name = get_file_name(full_path=pdf_path)
    self.pages = total_pages
    for index in range(total_pages):
        current_page = pdf_file._get_page(index)
        new_page = PdfWriter()
        new_page.add_page(current_page)
        with open(f'{self.path}/{pdf_name}_page_{index + 1}.pdf', 'wb') as output_stream:
            new_page.write(output_stream)
        fill_progress_bar(self)

def pdf_merger(self, file_name:str, pdf_files:list):
    new_pdf = PdfWriter()
    self.pages = len(pdf_files)
    for file in pdf_files:
        pdf_file = PdfReader(file)
        for page in pdf_file.pages:
            new_pdf.add_page(page)
            fill_progress_bar(self)

    with open(f'{self.path}/{file_name}.pdf', 'wb') as output_stream:
        new_pdf.write(output_stream)

def count_pdf_pages(pdf_files: list):
    pages_count = 0
    for file in pdf_files:
        pdf_file = PdfReader(file)
        pages_count += len(pdf_file.pages)

    return pages_count

def get_file_name(full_path: str) -> str:
    splitted_path = full_path.split('/')

    return splitted_path[-1]