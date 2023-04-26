import time
import pikepdf
from ORKG_connector import get_researchfield_id, get_property_id, upload_paper
#from json import dump
from io import IOBase
from bs4 import BeautifulSoup
from scikgmetadata import extract_metadata_no_deps, parse_xmp_no_deps

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


def extract_metadata(document, compatibility_mode: bool):
    """
    This method extracts metadata from a PDF file created with SciKGTeX.
    
    Parameters:
        document: the PDF file either as a pikepdf._qpdf.Pdf or just a filehandler of a PDF file.
        compatibility_mode (bool): whether or not to parse the metadata written from compatibility mode. 
            Best to try both and take whichever can be found.
    """
    ## overload method
    if isinstance(document, pikepdf._qpdf.Pdf):
        return extract_extract_metadata_pikepdf(document, compatibility_mode)
    elif isinstance(document, IOBase):
        return extract_metadata_no_deps(document, compatibility_mode)

def extract_extract_metadata_pikepdf(document: pikepdf._qpdf.Pdf, compatibility_mode: bool):
    """
    This method extracts metadata from a PDF file created with SciKGTeX.
    
    Parameters:
        document (pikepdf._qpdf.Pdf): the PDF file loaded with pikepdf.open()
        compatibility_mode (bool): whether or not to parse the metadata written from compatibility mode. 
            Best to try both and take whichever can be found.
    """
    if compatibility_mode:
        data = document.Root.SciKGMetadata.read_bytes().decode()
    else:
        data = document.Root.Metadata.read_bytes().decode()
    return data

def parse_xmp(xmp_stream):
    return parse_xmp_beautiful_soup(xmp_stream)

def parse_xmp_beautiful_soup(xmp_stream):
    data = BeautifulSoup(xmp_stream, 'xml')
    return data

def xmp2json(data):
    title = data.find('hasTitle').get_text()
    authors = data.find_all('hasAuthor')
    authors = [{'label': x.get_text()} for x in authors]
    research_field = data.find('hasResearchField').get_text()
    contributions = data.find('ResearchContribution')
    contributions = contributions.find_all()

if __name__=="__main__":
    metadata_json =  pdf2json('paper.pdf')
    start = time.time()
    upload_paper(metadata_json, update=False)
    print(f'Uploading paper: {round(time.time() - start, 3)}')