'''
Here the certificate is turnt off by CERT variable.
If in future, it is necessary to use CERTificate, use this variable
CERTificate can be found in https://curl.haxx.se/docs/caextract.html
'''

from tqdm import tqdm
import requests
import re
import os
import time
import warnings
import pickle
import json
import PyPDF2

warnings.filterwarnings("ignore")

ROOT_DIR = 'PDF_Archieve'
PICKLE_DIR = 'Pickle_Archieve'
SEAT_PLAN_HTML_LINKS = f'{PICKLE_DIR}/Seat_Plan_HTML_Links.pkl'
PDF_LINKS = f'{PICKLE_DIR}/PDF_Links.pkl'
STUDENT_INFO = f'{PICKLE_DIR}/Student_Info_Unstructured.pkl'
CERT = False

def Generating_URL(show=True):
    if os.path.exists(SEAT_PLAN_HTML_LINKS):
        print("Already HTML Links Generated")
        with open(SEAT_PLAN_HTML_LINKS, 'rb') as f:
            return pickle.load(f)
    else:
        print("Generating HTML Links")
        url='https://www.bracu.ac.bd/final-examinations-seat-plan-'
        semesters=[ 'spring-', 'summer-', 'fall-' ]
        urls = [ ]
        year, month = y_m_time()
        # starting from 2017 the link will start to generate
        for i in tqdm(range(2017,(year+1))):
            for s in range(len(semesters)):
                # if the current semester is not bigger of the semesters[s] eg 1, 2, 3
                if (not(month>(s+1)) and i==year):
                    pass
                else:
                    #generated url
                    temp_url = url+semesters[s]+str(i)
                    if show:
                        print(temp_url)
                    urls.append(temp_url)
        with open(SEAT_PLAN_HTML_LINKS, 'wb') as f:
            pickle.dump(urls, f)
    return urls

def Parsing_HTML_For_PDF_Links(urls):
    pattern = r'<a href="//(www.bracu.ac.bd/sites/default/files/registrar/exam_seat_plan/[-a-zA-Z0-9]*/[+a-zA-Z0-9]*.pdf)" target="_blank"'
    if os.path.exists(PDF_LINKS):
        print("Already PDF Links Generated")
        with open(PDF_LINKS, 'rb') as f:
            return pickle.load(f)
    else:
        print('Finding PDF links in these HTMLs')
        pdf_links = []
        for url in tqdm(urls):
            #download the plain html file
            file = requests.get(url, timeout=20, verify=CERT)
            html = file.text
            link_pattern = re.compile(pattern)
            pdf_link = link_pattern.findall(html)
            pdf_links.append(pdf_link)
        with open(PDF_LINKS, 'wb') as f:
            pickle.dump(pdf_links, f)
        return pdf_links

def Downloading_PDF(html_urls_list, pdf_urls_list):
    print('Downloading from PDFs Links')
    if not os.path.exists(ROOT_DIR):
        os.mkdir(ROOT_DIR)
    for html, pdfs in tqdm(zip(html_urls_list, pdf_urls_list)):
        folder_name = f"{ROOT_DIR}/{html.split('/')[-1]}"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        for pdf in tqdm(pdfs):
            file_name = pdf.split('/')[-1]
            if not os.path.exists(f'{folder_name}/{file_name}'):
                r = requests.get('http://'+pdf, stream=True, verify=CERT)
                chunk_size = 2000
                with open(f'{folder_name}/{file_name}', 'wb') as fd:
                    for chunk in r.iter_content(chunk_size):
                        fd.write(chunk)
                fd.close()

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

#                        #if the id is not in json
#                        if not(st_id in db.values()) :
#                            db['id'] = int(st_id)
#                            db['info'] = {}
#                            db['info']['name'] = name
#                            db['info']['Registration No'] = int(reg)
#                            db['info']['course'] = {}
#                            db['info']['course'][d] = [course_name.split('.')[0].upper()]
#                        else :
#                                #id is there so, name Registration No and atleast one course
#                                #so now checking the if the current semester exist
#                                if not(d in db['info']['course'].values()):
#                                    db['info']['course'][d] = [course_name.split('.')[0].upper]
#                                else : #a list for course of this current semester exist
#                                    db['info']['course'][d].append(course_name.split('.')[0]) #add the course by appending
    return db

#   format
#   [{  'id' : 17201049
#       'name' = 'Kamrul Hasan',
#       'Registration No': 1234123412 ,
#       'course' : {
#           { 'Summer 2017' : ['CSE101', 'BIO101'],
#             'Fall 2017' : ['CSE101', 'BIO101']
#                               }
#               }
#     },........]


def y_m_time():
    """
    this function returns tuple of year and number of semester in that year
    """
    current_date_raw = str(time.localtime())
    t = re.compile(r'time.struct_time\(tm_year=(\d{4}), tm_mon=(\d{1,2}),')
    r = t.findall(current_date_raw) # r is [('2019', '9')]
    year = int(r[0][0])
    m = int(r[0][1])
    month = 0
    if m <= 4 :
        month = 1
    elif m <= 8 and m>8 :
        month = 2
    else :
        month = 3
    return (year, month)

def main():
    html_links = Generating_URL(show=False)
    pdf_links = Parsing_HTML_For_PDF_Links(html_links)
    #print({html_links[i]: len(link) for i, link in enumerate(pdf_links)})
    Downloading_PDF(html_links, pdf_links)
    db = Parsing_PDF()
    print(db)


if __name__ == "__main__":
    main()
