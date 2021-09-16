from tqdm import tqdm
import os
import pickle

from src.Year_Semester import *
from src.CONSTANTS import *

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
