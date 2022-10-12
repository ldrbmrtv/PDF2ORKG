from bs4 import BeautifulSoup
from json import dump

def get_researchfield_id(research_field_name):
    if research_field_name == 'Information Science':
        return 'R278'

def get_property_id(class_name):
    if class_name == 'researchproblem':
        return 'P32'
    elif class_name == 'result':
        return 'P1'
    elif class_name == 'conclusion':
        return 'P7072'
    elif class_name == 'objective':
        return 'P7077'
    elif class_name == 'method':
        return 'P2'

with open('output.xmp_metadata.xml', 'r') as f:
    data = f.read()

print(data)
data = BeautifulSoup(data, 'xml')

title = data.find('hasTitle').get_text()
authors = data.find_all('hasAuthor')
authors = [{'label': x.get_text()} for x in authors]
research_field = get_researchfield_id(data.find('hasResearchField').get_text())
contributions = data.find('ResearchContribution')
contributions = contributions.find_all()
py_contributions = {}
for i, contribution in enumerate(contributions):
    py_contributions[get_property_id(contribution.name)] = [
        {'text': contribution.get_text()}]

result = {'predicates': [],
          'paper': {
              'title': title,
              #'doi': '',
              'authors': authors,
              #'publicationMonth' : '',
              #'publicationYear': 2022,
              #'publishedIn': '',
              'researchField': research_field,
              'contributions': [{'name': 'Contribution 1',
                                 'values': py_contributions}]}}

with open('metadata.json', 'w', encoding = 'utf-8') as f:
    dump(result, f, ensure_ascii=False, indent=4)
