from tqdm import tqdm
import requests
import re
import os
import pickle
import warnings
warnings.filterwarnings("ignore")

from src.CONSTANTS import *

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
