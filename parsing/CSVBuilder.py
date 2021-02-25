import csv

#This class will take a dictionary of strings and integers and transform it into a CSV file with the correct converted metric names.
class CSVBuilder:

    #Constructor for the class.  Accept a filename as a string, and a dictionary.
    #First, if the dictionary is not in the correct format (all keys are strings, and all values are integers),
    #then set the correctFormat boolean to False, for when the build function is run.  Then, store the parameters
    #in their corresponding global variables.
    def __init__(self, filename: str, table: dict):
        self.correctFormat = True
        for x in table.keys():
            if not isinstance(x, str):
                self.correctFormat = False
            if not isinstance(table[x], int):
                self.correctFormat = False
        self.fname = filename
        self.myDict = table

    #This function will build the CSV file and return an integer value.
    #It will return 0 if it ran successfully, and 1 if it failed.
    def build(self):
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

        #If the dictionary was determined to be of the correct format, then convert the keys
        #to their corresponding metric names, and write to a file.
        if self.correctFormat:
            with open(self.fname,"a+") as f:
                f.write('Metric,Value\n')
                for k in self.myDict:
                    try:
                        self.myDict[cDict[k]] = self.myDict.pop(k)
                        f.write(cDict[k] + ',' + str(self.myDict[cDict[k]]) + '\n')
                    except KeyError:
                        return 1
            return 0
        else:
            return 1
