import pikepdf
from io import IOBase
from bs4 import BeautifulSoup

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

def extract_metadata_no_deps(document: IOBase, compatibility_mode: bool):
    """
    This method extracts metadata from a PDF file created with SciKGTeX.
    
    Parameters:
        document (IOBase): the PDF file opened in 'rb' mode
        compatibility_mode (bool): whether or not to parse the metadata written from compatibility mode. 
            Best to try both and take whichever can be found.
    """
    file_str = document.readlines()
    data = ""
    in_metadata_stream = False
    start_copy = False
    metadata_key='/Type /SciKGMetadata' if compatibility_mode else '/Type /Metadata'
    for line in file_str:
        try:
            line=line.decode()
        except UnicodeDecodeError:
            continue
        
        if metadata_key in line:
            in_metadata_stream=True

        if in_metadata_stream:
            if line.strip()=="stream":
                start_copy=True

            elif start_copy and line.strip()!="endstream":
                data+=line

            elif line.strip()=="endstream":
                start_copy=False
                in_metadata_stream=False
    return data.strip()

def parse_xmp(xmp_stream):
    return parse_xmp_beautiful_soup(xmp_stream)

def parse_xmp_beautiful_soup(xmp_stream):
    data = BeautifulSoup(xmp_stream, 'xml')
    return data

def parse_xmp_no_deps(xmp_stream):
    raise NotImplementedError

def xmp2json(data):
    title = data.find('hasTitle').get_text()
    authors = data.find_all('hasAuthor')
    authors = [{'label': x.get_text()} for x in authors]
    research_field = data.find('hasResearchField').get_text()
    contributions = data.find('ResearchContribution')
    contributions = contributions.find_all()