import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from scikgmetadata import extract_metadata, parse_xmp
import pikepdf
from bs4 import BeautifulSoup
import pytest

@pytest.mark.parametrize("input_file_name,comp_mode", [
    ("paper.pdf", False),
    ("../SciKGTeX/test/test_pdfa_switch/test.pdf", True),
])
def test_extract_metadata_without_deps(input_file_name, comp_mode):
    with open(input_file_name, 'rb') as pdf:
        data = extract_metadata(pdf, comp_mode)
    assert data is not None

@pytest.mark.parametrize("input_file_name,comp_mode", [
    ("paper.pdf", False),
    ("../SciKGTeX/test/test_pdfa_switch/test.pdf", True),
])
def test_extract_metadata_pikepdf(input_file_name, comp_mode):
    pdf = pikepdf.Pdf.open(input_file_name)
    data = extract_metadata(pdf, comp_mode)
    assert data is not None

@pytest.mark.parametrize("input_file_name,comp_mode", [
    ("paper.pdf", False),
    ("../SciKGTeX/test/test_pdfa_switch/test.pdf",True),
])
def test_extract_methods_equivalent(input_file_name, comp_mode):
    pdf1 = pikepdf.Pdf.open(input_file_name)
    data1 = extract_metadata(pdf1, comp_mode)
    with open(input_file_name, 'rb') as pdf2:
        data2 = extract_metadata(pdf2, comp_mode)
    assert data1==data2

if __name__=="__main__":
    with open("../SciKGTeX/test/test_pdfa_switch/test.pdf", 'rb') as pdf:
        data = extract_metadata(pdf, True)
    xml_file=parse_xmp(data)
    print(xml_file)