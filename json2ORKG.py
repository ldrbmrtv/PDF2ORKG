from orkg import ORKG
from json import load

orkg = ORKG(host='https://sandbox.orkg.org/',
            creds=('baimuratov.i@gmail.com', '8520123JohnVonNeumann!'))

with open('paper.json') as f:
    paper = load(f)

responce = orkg.papers.add(params=paper)
print(responce.succeeded)
print(responce.content)
