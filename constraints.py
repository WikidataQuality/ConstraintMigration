#import pywikibot
import json
import re
import codecs
import pywikibot
filename = '/home/amir/constraints.json'
site = pywikibot.Site('en', 'wikipedia')
repo = site.data_repository()
property_id = 1234567
Qid_constraints = {
    'Type': 123475,
    'Value type': 1224,
}
qualifers_dict = {
    'property': 12345,
    'class': 124565,
    'relation': 1234,
    'instance': 1223,
    'constraint_status': 1223,
    'mandatory': 1234,
}


class Constraint(object):

    """docstring for Constraint."""

    def fromJSON(self, dict_name):
        self.type = dict_name['Constraint']
        self.parameters = dict_name['Constraint_Parameters']
        self.page = pywikibot.PropertyPage(repo, 'P' + dict_name['Property'])

    def treat(self):
        claim = pywikibot.Claim(repo, 'P%d' % property_id)
        constraint_item = pywikibot.ItemPage(repo, Qid_constraints[self.type])
        claim.setTarget(constraint_item)
        for case in self.parameters:
            qualifer = pywikibot.Claim(repo, 'P%d' % qualifers_dict[case])
            if re.search('^Q\d+?$', self.parameters[case]):
                qualifer_target = pywikibot.ItemPage(repo, self.parameters[case])
            elif self.parameters[case] in qualifers_dict:
                qualifer_target = pywikibot.ItemPage(repo, 'Q%d' % qualifers_dict[self.parameters[case]])
            else:
                qualifer_target = self.parameters[case]
            qualifer.setTarget(qualifer_target)
            claim.addQualifier(qualifer)
        #Flusing away anything
        self.page.addClaim(claim)
with codecs.open(filename, 'r', 'utf-8') as f:
    constraints = json.loads(f.read())
for i in constraints[:10]:
    res = None
    for case in i['Constraint_Parameters']:
        if re.search('^Q\d+?,', i['Constraint_Parameters'][case]):
            res = i['Constraint_Parameters'][case].split(',')
    if res is not None:
        cases = []
        for case in i['Constraint_Parameters']:
            if re.search('^Q\d+?,', i['Constraint_Parameters'][case]):
                for item in i['Constraint_Parameters'][case].split(','):
                    case_temp = i
                    case_temp['Constraint_Parameters'][case] = item
                    cases.append(case_temp)
    else:
        cases = [i]
    for case in cases:
        constraint = Constraint()
        constraint.fromJSON(case)
        constraint.treat()
print(constraints[0])
