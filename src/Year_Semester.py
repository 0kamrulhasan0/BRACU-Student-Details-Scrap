import time
import re

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
