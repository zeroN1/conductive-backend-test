import imp
import math
import csv
from utils import valueMapper, formatSchoolName

Data = None

def find_closest(skey = "", data = []):
    lo = 0
    hi = len(data)-1
    idx = None
    
    while lo<=hi:
        
        mid = math.floor((lo+hi)/2)
        
        if data[mid]["school"] < skey:
            lo += 1
        elif data[mid]["school"] > skey:
            hi -= 1
        else:
            idx = mid
            break
    if not idx:
        # no exact match found
        # lo = hi + 1 and lo > hi
        # skey should be in between hi and lo (insertion point)
        # so, return these two entries
        lo = min(len(data)-1, lo)
        hi = max(0, hi)
        
        return [data[hi], data[lo]]
    else:
        # found an exact match
        # return this and two other entries around it
        lo = max(0, idx-1)
        hi = min(len(data)-1, idx+1)
        return [data[idx], data[lo], data[hi]]
    
def search_school(key = ""):
    global Data
    if not Data:
        main()
    key = formatSchoolName(key)
    matches = find_closest(key, Data)
    print("Results for {}:".format(key))
    for i, match in enumerate(matches):
        print("{i}. {school}\n {city}, {state}".format(**match, i=i+1))

def main():
    global Data
    fname = "sl051bai.csv"
    with open(fname, mode="r", encoding="cp1252") as csvfile:
        rows = csv.DictReader(csvfile)
        rows = map(valueMapper, list(rows)[1:])
        Data = list(rows)
        Data.sort(key=lambda o: o["school"])
        
if __name__ == '__main__':
    # Test
    main()
    search_school("hogwarts school of wizardry")
else:
    main()
    