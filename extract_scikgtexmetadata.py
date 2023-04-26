import sys
from scikgmetadata import extract_metadata_no_deps
fn = sys.argv[1]
with open(fn, 'rb') as pdf:
    data = extract_metadata_no_deps(pdf, True)
    if data:
        print(data)
    else:
        data = extract_metadata_no_deps(pdf, False)
        if data:
            print(data)
        else:
            print("No Metadata found in PDF Document {fn}!")