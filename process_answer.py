import xmltodict
from pprint import pprint
def get_answer(s):
    r =  list(xmltodict.parse(s).get('QuestionFormAnswers').get('Answer'))
    l = {i.get('QuestionIdentifier'):i.get('FreeText') for i in r}
    return l


if __name__ == '__main__':
    s ='<?xml version="1.0" encoding="ASCII"?><QuestionFormAnswers xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd"><Answer><QuestionIdentifier>shortCode</QuestionIdentifier><FreeText>B13zx8Og97H</FreeText></Answer><Answer><QuestionIdentifier>setting</QuestionIdentifier><FreeText>Green</FreeText></Answer><Answer><QuestionIdentifier>mood</QuestionIdentifier><FreeText>Relaxation</FreeText></Answer><Answer><QuestionIdentifier>style</QuestionIdentifier><FreeText>Authentic</FreeText></Answer></QuestionFormAnswers>'
    pprint(get_answer(s))