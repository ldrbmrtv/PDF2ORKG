from orkg import ORKG
from json import load

orkg = ORKG(host='https://sandbox.orkg.org/',
            creds=('baimuratov.i@gmail.com', '8520123JohnVonNeumann!'))

responce = orkg.classes.get_resource_by_class(class_id='ResearchField',
                                              q='Information Science',
                                              exact=True)

print(responce.succeeded)
print(responce.content)
