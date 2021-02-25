import csv

class CSVBuilder:

    fname = ''
    dict = {}
    cDict = {'NOL':'Number of Lines',
             'NOC':'Number of Comments',
             'CPES':'Ratio of comment Line to the executable statements',
             'NOCL':'Number of Classes',
             'NNC1':'Number of Classes of nesting level 1',
             'NNC2':'Number of Classes of nesting level 2',
             'NNC3':'Number of Classes of nesting level 3',
             'NNC4':'Number of Classes of nesting level 4',
             'NNC5':'Number of Classes of nesting level 5',
             'NNC6':'Number of Classes of nesting level 6',
             'NNC7':'Number of Classes of nesting level 7',
             'NNC8':'Number of Classes of nesting level 8',
             'NNC9':'Number of Classes of nesting level 9',
             'NNC10':'Number of Classes of nesting level 10',
             'NNC':'Numbre of Nested classes',
             'NOM':'Total Number of Methods',
             'NIM':'Number of Inherited Methods',
             'NLM':'Number of Local Methods',
             'NOVM':'Number of overridden methods',
             'ANIM':'Average Number of Inherited Methods per Class',
             'ANLM':'Average Number of Local methods per Class',
             'NOH':'Number of Hierarchies',
             'NAC':'Number of Abstract Classes',
             'NLC':'Number of Leaf Classes',
             'NPPM':'Average Number of Parameters per method',
             'NOA':'Number of Attributes',
             'AWI':'Average Width of Inheritance'}

    def __init__(self, filename: str, table: dict[str,int]):
        self.fname = filename
        self.dict = table

    def build():
        global dict
        with open(fname,"a+") as f:
            for k in dict:
                try:
                    dict[cDict[k]] = dict.pop(k)
                    f.write(cDict[k] + ',' + str(dict[k]))
                except KeyError:
                    return 1
        return 0
