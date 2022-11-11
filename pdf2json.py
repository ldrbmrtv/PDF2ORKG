import pikepdf
from bs4 import BeautifulSoup
#from json import dump
from ORKG_connector import *
import time

# Read PDF metadata
start = time.time()
pdf = pikepdf.Pdf.open('paper.pdf')
data = str(pdf.open_metadata())
data = BeautifulSoup(data, 'xml')

title = data.find('hasTitle').get_text()
authors = data.find_all('hasAuthor')
authors = [{'label': x.get_text()} for x in authors]
research_field = data.find('hasResearchField').get_text()
contributions = data.find('ResearchContribution')
contributions = contributions.find_all()
print(f'Read PDF: {round(time.time() - start, 3)}')

#Requesting IDs
start = time.time()
research_field_id = get_researchfield_id(research_field)
py_contributions = {}
for i, contribution in enumerate(contributions):
    entity_id = get_property_id(contribution.name)
    if entity_id:
        py_contributions[entity_id] = [
            {'text': contribution.get_text()}]
print(f'Requesting IDs: {round(time.time() - start, 3)}')

# Uploading paper to ORKG
start = time.time()
result = {'predicates': [],
          'paper': {
              'title': title,
              'authors': authors,
              'researchField': research_field_id,
              'contributions': [{'name': 'Contribution 1',
                                 'values': py_contributions}]}}

# Write json
#with open('metadata.json', 'w', encoding = 'utf-8') as f:
#    dump(result, f, ensure_ascii=False, indent=4)

upload_paper(result, update=False)
print(f'Uploading paper: {round(time.time() - start, 3)}')
