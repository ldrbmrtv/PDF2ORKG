import pikepdf
#from json import dump
from ORKG_connector import get_researchfield_id, get_property_id, upload_paper
import time
from scikgmetadata import extract_metadata, parse_xmp

def pdf2json(pdf_file_name):
    start = time.time()
    pdf = pikepdf.Pdf.open(pdf_file_name)
    # Read PDF metadata
    data = extract_metadata(pdf)
    data = parse_xmp(data)

    title = data.find('hasTitle').get_text()
    authors = data.find_all('hasAuthor')
    authors = [{'label': x.get_text()} for x in authors]
    research_field = data.find('hasResearchField').get_text()
    contributions = data.find('ResearchContribution')
    contributions = contributions.find_all()
    print(f'Read PDF: {round(time.time() - start, 3)}')

    #Requesting IDs
    start = time.time()
    research_field_id =  get_researchfield_id(research_field)
    py_contributions = {}
    for contribution in contributions:
        entity_id = get_property_id(contribution.name)
        if entity_id:
            py_contributions[entity_id] = [
                {'text': contribution.get_text()}]
    print(f'Requesting IDs: {round(time.time() - start, 3)}')

    # Uploading paper to ORKG
    result = {
        'predicates': [],
        'paper': {
            'title': title,
            'authors': authors,
            'researchField': research_field_id,
            'contributions': [
                {
                    'name': 'Contribution 1',
                    'values': py_contributions
                },
            ],
        }
    }
    return result

if __name__=="__main__":
    metadata_json =  pdf2json('paper.pdf')
    start = time.time()
    upload_paper(metadata_json, update=False)
    print(f'Uploading paper: {round(time.time() - start, 3)}')