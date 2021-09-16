import PyPDF2
import re
import os
import pickle

from src.CONSTANTS import *

def Read_PDF(d, course_name):
    with open(ROOT_DIR+'/'+d+'/'+course_name, 'rb') as pdf_object:
        # First line is being read to check if it is a "file not found" html page
        temp = pdf_object.readline()
        temp = temp[:2]
        files_first_line = temp.decode()
        # in html page first two character would be <! and as the file is being
        # read as byte it is being converted to string by .decode()
        if files_first_line == '<!':
            pass
        else:
            pypdf2_object = PyPDF2.PdfFileReader(pdf_object)
            for page_no in range(0, pypdf2_object.numPages):
                page_object = pypdf2_object.getPage(page_no)
                total_text = page_object.extractText()
                r = re.compile(r'(\d{8})(\D+\s(\D*\s)*\D+)\d{2}(\d{10})')
                info = r.findall(total_text)
            return info
"""
 Format:
 [{'id' : 17201049
   'name' = 'Kamrul Hasan',
   'Registration No': 1234123412 ,
   'course' : {
       { 'Summer 2017' : ['CSE101', 'BIO101'],
         'Fall 2017' : ['CSE101', 'BIO101']
                           }
           }
   },........]
"""

def Parsing_PDF():
    if os.path.exists(STUDENT_INFO):
        print('Already Student Info Parsed')
        with open(STUDENT_INFO, 'rb') as f:
            db = pickle.load(f)
    else:
        print('Parsing Student Info')
        db = []
        dir_list = [d for d in os.listdir(ROOT_DIR) if not d.endswith('pkl')]
        for d in tqdm(dir_list):
            file_list = os.listdir(ROOT_DIR+'/'+d)
            if not os.path.exists(f'{PICKLE_DIR}/{d}.pkl'):
                sem = []
                for course_name in tqdm(file_list):
                    info = Read_PDF(d, course_name)
                    if info:
                        st_db = []
                        for i in info:
                            st_id, name, blank, reg = i
                            st_db.append((st_id, name, reg))
                        sem.append({ course_name: st_db })
                with open(f'{PICKLE_DIR}/{d}.pkl', 'wb') as f:
                    pickle.dump(sem, f)
                print(sem)
            else:
                with open(f'{PICKLE_DIR}/{d}.pkl', 'rb') as f:
                    sem = pickle.load(f)
                print(sem)
            db.append({ d : sem })
        with open(STUDENT_INFO, 'wb') as f:
            pickle.dump(db, f)
    return db
