'''
Here the certificate is turnt off by CERT variable.
If in future, it is necessary to use CERTificate, use this variable
certificate can be found in https://curl.haxx.se/docs/caextract.html
'''

from tqdm import tqdm
import os
import requests
import warnings
warnings.filterwarnings("ignore")

from src.URL_Generation import *

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
