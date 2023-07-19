import zlib
import re

def extract_metadata_no_deps(doc_str: bytes, compatibility_mode: bool) -> str:
    """
    This method extracts metadata from a PDF file created with SciKGTeX.
    
    Parameters:
        doc_str (bytes): the PDF file as a string of bytes
        compatibility_mode (bool): whether or not to parse the metadata written from compatibility mode. 
            Best to try both and take whichever can be found.
    """
    metadata_key=b'/Type /SciKGMetadata' if compatibility_mode else b'/Type /Metadata'
    metadata_pattern = re.compile(b'(' + metadata_key + b'.*?)stream(.*?)endstream', re.S)
    for header, data in re.findall(metadata_pattern, doc_str):
        if '/FlateDecode' in header.decode('utf-8'):
            return zlib.decompress(data.strip(b'\r\n')).decode('utf-8').strip()
        else:
            return data.decode('utf-8').strip()

def parse_xmp_no_deps(xmp_stream):
    raise NotImplementedError

