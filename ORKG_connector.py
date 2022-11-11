from orkg import ORKG
from json import load

def get_researchfield_id(label):
    responce = orkg.classes.get_resource_by_class(class_id = 'ResearchField',
                                                  q = label,
                                                  exact=True)
    content = responce.content
    if content:
        return content[0]['id']
    else:
        return default_researchfield

def get_property_id(label):
    property_id = default_properties.get(label)
    if not property_id:
        responce = orkg.predicates.get(q = label, exact=True)
        content = responce.content
        if content:
            property_id = content[0]['id']
    return property_id

def upload_paper(paper, update = True):
    response = orkg.papers.add(params=paper, merge_if_exists=update)
    print(response.succeeded)


orkg = ORKG(host='https://sandbox.orkg.org/',
            creds=('baimuratov.i@gmail.com', '8520123JohnVonNeumann!'))

default_researchfield = 'ResearchField'

default_properties = {
    'researchproblem': 'P32',
    'result': 'P1',
    'conclusion': 'P7072',
    'objective': 'P7077',
    'method': 'P2'}
