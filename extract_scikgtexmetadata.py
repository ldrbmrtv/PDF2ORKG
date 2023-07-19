import sys
from scikgmetadata import extract_metadata_no_deps
fn = sys.argv[1]
with open(fn, 'rb') as pdf:
    document=pdf.read()
    data = extract_metadata_no_deps(document, True)
    if data:
        print(data)
    else:
        data = extract_metadata_no_deps(document, False)
        if data:
            print(data)
        else:
            print(f"No Metadata found in PDF Document {fn}!")