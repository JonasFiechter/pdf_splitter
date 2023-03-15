from PyPDF2 import PdfReader, PdfWriter
from src.components.progress_bar import fill_progress_bar
import os

#TODO: CHECK IF FILE NAMES ALREADY EXISTS, THIS FUNCTION CAN ERASE YOUR FILES

def pdf_splitter(self, pdf_path, customized_pages):
    pdf_file = PdfReader(f'{pdf_path}', 'rb')
    total_pages = len(pdf_file.pages)
    pdf_name = get_file_name(full_path=pdf_path)
    
    if type(customized_pages) == tuple:
        self.pages = len(range(customized_pages[0]-1, customized_pages[1]))
        for index in range(customized_pages[0]-1, customized_pages[1]):
            current_page = pdf_file._get_page(index)
            new_page = PdfWriter()
            new_page.add_page(current_page)
            file_name = check_current_dir(self.path, f'{pdf_name}_page_{index + 1}')
            with open(file_name, 'wb') as output_stream:
                new_page.write(output_stream)
            fill_progress_bar(self)

    elif type(customized_pages) == list:
        self.pages = len(customized_pages)
        for index in customized_pages:
            current_page = pdf_file._get_page(index-1)
            new_page = PdfWriter()
            new_page.add_page(current_page)
            file_name = check_current_dir(self.path, f'{pdf_name}_page_{index}')
            with open(file_name, 'wb') as output_stream:
                new_page.write(output_stream)
            fill_progress_bar(self)
    else:
        self.pages = total_pages
        for index in range(total_pages):
            current_page = pdf_file._get_page(index)
            new_page = PdfWriter()
            new_page.add_page(current_page)
            file_name = check_current_dir(self.path, f'{pdf_name}_page_{index + 1}')
            with open(file_name, 'wb') as output_stream:
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

    file_name = check_current_dir(self.path, f'{file_name}')
    with open(file_name, 'wb') as output_stream:
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

def check_custom_data(pages_list='', page_start=0, page_end=0, total_pages=0):
    error = False
    new_list = []
    if pages_list:
        pages_list = pages_list.split(',')
        for item in pages_list:
            item = item.replace(' ', '')
            if not item.isnumeric():
                return pages_list, 'Invalid character!'
            elif int(item) > total_pages:
                return pages_list, 'Invalid page number'
            else:
                new_list.append(int(item))
            
        return new_list, error
    else:
        if page_start > total_pages or page_end > total_pages:
            error = 'Page number bigger than limit'
            return None, error
        elif page_start > page_end or page_start == page_end:
            error = 'Starting page must be smaller than ending page'
            return None, error
        
        return (page_start, page_end), error
    
def check_current_dir(path, file_name, count=1):
    if file_name + '.pdf' in os.listdir(path):
        file_name += f'_{count}'
        check_current_dir(path, file_name, count=count+1)
    
    return path + '/' + file_name + '.pdf'