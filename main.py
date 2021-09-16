from src.CONSTANTS import *
from src.URL_Generation import *
from src.HTML_Parsing import *
from src.PDF_Parsing import *
from src.Download_PDF import *

def main():
    html_links = Generating_URL(show=False)
    pdf_links = Parsing_HTML_For_PDF_Links(html_links)
    Downloading_PDF(html_links, pdf_links)
    db = Parsing_PDF()
    print(db)

if __name__ == "__main__":
    main()
