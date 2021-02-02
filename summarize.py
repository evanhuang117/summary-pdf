import pdfplumber
import sys
from summarizer import Summarizer
from summarizer.coreference_handler import CoreferenceHandler
from fpdf import FPDF
import spacy

def use_coreference():
    spacy.load('en_core_web_lg')
    handler = CoreferenceHandler(spacy_model='en_core_web_lg')
    return Summarizer(sentence_handler=handler)

# 1. activate python venv "source venv/bin/activate"
# 2. run "python3 summarize.py 'path to PDF' "
file_name = sys.argv[1]
# TODO: find out why this seg faults when true
use_coref = False

pdf = pdfplumber.open(file_name)
print("Imported a PDF with " + str(len(pdf.pages)) + " pages")
#remove file extension from the name
file_name = file_name.split('.', 1)[0]

# read in the text
text = ""
for pg in pdf.pages:
    print("Processing page " + str(pg.page_number))
    text += pg.extract_text()

# run the summarizer
if use_coref:
    model = use_coreference()
else:
    model = Summarizer()

print("summarizing")
summarized = model(body=text)

''' uncomment to print to text file
with open("summarized", 'w') as f:
    f.write(summarized)
'''


# output the summarized text to a pdf
output_pdf = FPDF()
output_pdf.add_page()
output_pdf.set_font("Arial", size=12)
# fix encoding issues with text
summarized = summarized.encode('latin-1', 'replace').decode('utf-8')
# multi_cell auto line breaks (wrap text)
output_pdf.multi_cell(200, 10, summarized, align='L')
output_pdf.output(file_name + "-summarized.pdf")


