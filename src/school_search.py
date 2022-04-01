import csv
import csv
from itertools import groupby
from utils import Fields

CHARSET_SZ = 256
StateCodes = {}
StateNames = {}
StateFullNames = set()
CityNames = set()
SchoolDirectory = None
fname = "sl051bai.csv"
stateFname = "states-codes.csv"

def valueMapper(row):
    global Fields, StateCodes
    urank = row.get(Fields.get("UrbanRank"))
    urank = int(urank) if urank != "N" else 0
    mrank = row.get(Fields.get("MetroRank"))
    mrank = int(mrank) if mrank != "N" else 0
    return {
        "status":row.get(Fields.get("Status")),
        "school":row.get(Fields.get("SchoolName")),
        "city"  :row.get(Fields.get("City")),
        "state" :row.get(Fields.get("State")),
        "urank" :urank,
        "mrank" :mrank,
        "statefull": StateCodes[row.get(Fields.get("State")).lower()]
    }
    
def tokenizeSearchKeywords(kw):
    # check for state full names, state 2 letter code
    # and city name in search keywords
    global CityNames, StateFullNames, StateCodes, StateNames
    words = kw.split(" ")
    city = None
    state = None
    search = []
    
    for word in words:
        word = word.lower()
        if len(word) == 2:
            # check for state codes
            try:
                s = StateCodes[word]
                state = s
            except KeyError:
                pass
        if word in CityNames:
            print("CityWord: {}".format(word))
            city = word.lower()
        elif word in StateFullNames:
            print("StateWord: {}".format(word))
            state = word.lower()
       
        search.append(word)
    
    if state and len(state) > 2:
        # replace with code
        state = StateNames[state.lower()]
    
    
    return ("".join(search), city, state,)        

def tokenize(obj):
    name = obj["school"].replace(" ", "")
    name += obj["city"]
    name += obj["state"]
    return name.lower()

class TrieNode():
    
    def __init__(self, char = "", meta = None):
        self.char = char
        self.word = None
        self.children = [None for _ in range(CHARSET_SZ)]
        self.terminal = False
        self.meta = meta

        
class Trie():
    
    def __init__(self):
        self.root = TrieNode("\0")
        
    def insert(self, token, meta = None):
        curr = self.root
        for c in token:
            idx = self._getIndex(c)
            if not curr.children[idx]:
                # add a new node
                curr.children[idx] = TrieNode(c.lower())
            curr = curr.children[idx]
            
        # add meta to the terminal node
        curr.terminal = True
        curr.meta = meta
        curr.word = token
        
    def search(self, prefix):
        # return a tuple indicating full prefix found
        # or partial match found
        full, node = self._getNode(prefix)
        return (True, node,) if (full and node.terminal) else (False, node,)
    
    def startsWith(self, prefix = ""):
        # returns True on a Full Prefix Match
        return self._getNode(prefix)[0]                 
    
        
    def _print(self, root, city, state, prefs):
        # Note: see if word can be constrcuted from the letter
        # and more space can be saved instead of keeping the
        # word in set
        if not root:
            return
        if root.terminal:
            add = True
            if city and state:
                if root.meta["city"].lower() == city and \
                    root.meta["state"].lower() == state:
                        prefs.insert(0, root.meta)
                        add = False    
            elif city:
                if root.meta["city"].lower() == city:
                    prefs.insert(0, root.meta)
                    add = False
            elif state:
                if root.meta["state"].lower() == state:
                    prefs.insert(0, root.meta)
                    add = False
            
            if add: 
                prefs.append(root.meta)
            
            
        for node in root.children:
            self._print(node, city, state, prefs)
             
    def printTrie(self, root = None, city = None, state = None):
        if not root:
            root = self.root
        prefs = []
        self._print(root, city, state, prefs)
        #print("Prefs", prefs)
        for (i, o) in enumerate(prefs):
            v = {
                "i": i+1,
                "city": o["city"].upper(),
                "school": o["school"].upper(),
                "state": o["state"].upper()
            }
            print("{i}. {school}\n{city}, {state}".format(**v))
        
        
    
    def _getNode(self, prefix):
        # returns a tuple where
        #   first value: 
        #       is bool and indicates a full prefix
        #       match when True and False on partial or no match
        #   second value:
        #       the last char node of the token
        #
        curr = self.root
        for c in prefix:
            idx = self._getIndex(c)
            if not curr.children[idx]:
                # the node was not found
                # curr represents all the matches, can even
                # be the root node if there was no match
                return (False, curr,)
            curr = curr.children[idx]
        
        # the pointer is now at the end node of the token
        # the char is the last char of the token
        return (True, curr,)
        
    def _getIndex(self, c):
        return ord(c)



def main():
    data = None
    global StateCodes, StateFullNames, CityNames, StateNames, SchoolDirectory, stateFname, fname
    SchoolDirectory = Trie()
    
    with open(stateFname, "r") as codesfile:
        line = codesfile.readline()
        while line:
            stateName, code = list(map(lambda v: v.strip(), line.split(",")))
            StateCodes[code.lower()] = stateName.lower()
            StateFullNames.add(stateName.lower())
            StateNames[stateName.lower()] = code.lower()
            line = codesfile.readline()
        
    with open(fname, mode="r", encoding="cp1252") as csvfile:
        rows = csv.DictReader(csvfile)
        data = list(map(valueMapper, list(rows)[1:]))
        
        groupCities = lambda o: o.get("city")
        
        rows = data.copy()
        rows.sort(key=groupCities)
        
        for city, _ in groupby(rows, key=groupCities):
            CityNames.add(city.lower())
            
        for row in data:
            token = tokenize(row)
            SchoolDirectory.insert(token, row)
    
def search_school(keyword):
    global SchoolDirectory
    token, city, state = tokenizeSearchKeywords(keyword)
    full, node = SchoolDirectory.search(token)
    if not full:
        SchoolDirectory.printTrie(node, city, state)
    else:
        # show the result that has a full match
        i = 0
        v = {
            "i": i+1,
            "city": node.meta["city"].upper(),
            "school": node.meta["school"].upper(),
            "state": node.meta["state"].upper()
        }
        print("{i}. {school}\n{city}, {state}".format(**v))
        
if __name__ == '__main__':
    # Test
    main()
    search_school("hogwarts school of wizardry")
else:
    main()