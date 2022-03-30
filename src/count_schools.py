import csv
import itertools
from utils import valueMapper, profile

def count_fast(data = []):
    states = {}
    cities = {}
    metros = {}
    total_schools = len(data)
    
    for s in data:
        state = s.get("state")
        city = s.get("city")
        metro = s.get("mrank")
        
        if state in states:
            states[state] += 1
        else:
            states[state] = 1
            
        if city in cities:
            cities[city] += 1
        else:
            cities[city] = 1
            
        if metro in metros:
            metros[metro] += 1
        else:
            metros[metro] = 1
            
    print("[1] Total Schools: \t{}".format(total_schools))
    print("[2] Total Schools Per State:")
    keys = list(states)
    keys.sort()
    
    for state in keys:
        print("{}:\t{}".format(state, states[state]))
        
    keys = list(cities)
    keys.sort(key=lambda k: cities[k])
    
    print("[3] City with most schools: {}\t Total Schools: {}".format(keys[-1], cities[keys[-1]]))
    
    keys = list(metros)
    keys.sort()
    
    print("[4] Total Schools Per Metro Local (1-8, N for unassigned):")
    for metro in keys:
        print("{}:\t{}".format(metro, metros[metro]))
        
    at_least_one = filter(lambda c: cities[c] >= 1, list(cities))
    print("[5] Total Unique Cities with at least 1 school: {}".format(len(list(at_least_one))))

def print_total_schools(data = []):
    print("[1] Total Schools: {}".format(len(data)))

def print_highest_schools_city(data = []):
    keyfunc = lambda o: o.get("city")
    totals = {}
    data.sort(key=keyfunc)
    for k, g in itertools.groupby(data, keyfunc):
        totals[k] = len(list(g))

    cities = list(totals)
    cities.sort(key=lambda c: totals[c])            
    
    hkey = {
        "city": cities[-1],
        "schools": totals[cities[-1]]
    }
    print("[3] City with most schools: {city}\tTotal Schools: {schools}".format(**hkey))
    

def print_schools_by_metro(data = []):
    kf = lambda o: o.get("mrank")
    data.sort(key=kf)
    totals = {}
    for k, g in itertools.groupby(data, kf):
        totals[k] = len(list(g))
        
    metros = list(totals)
    metros.sort()
    print("[4] Total Schools By Metro Code (1-8 or N for unassigned):")
    for metro in metros:
        print("{}:\t{}".format(metro, totals.get(metro))) 
        

def print_state_total(data = []):
    keyfunc = lambda o: o.get("state")
    data.sort(key=keyfunc)
    totals = {}
    for k, g in itertools.groupby(data, keyfunc):
        totals[k] = len(list(g))
    
    states = list(totals)
    states.sort()            
    print("[2] Total Schools By States ({} states): \n".format(len(states)))
    for state in states:
        print("{}:\t{}".format(state, totals.get(state)))
        
def print_unique_cities_one_school(data = []):
    keyfunc = lambda o: o.get("city")
    totals = {}
    data.sort(key=keyfunc)
    for k, g in itertools.groupby(data, keyfunc):
        totals[k] = len(list(g))

    cities = list(totals)
    print("[5] [5] Total Unique Cities with at least 1 school: {}".format(len(cities)))

def count_slow(data = []):
    print_total_schools(data.copy())
    print_state_total(data.copy())
    print_highest_schools_city(data.copy())
    print_schools_by_metro(data.copy())
    print_unique_cities_one_school(data.copy())

def print_counts(data = [], strategy = "fast"):
    if strategy == "fast":
        count_fast(data)
    else:
        count_slow(data)
        

def main(prof = False, strategy = "fast"):
    fname = "sl051bai.csv"
    with open(fname, mode="r", encoding="cp1252") as csvfile:
        rows = csv.DictReader(csvfile)
        rows = map(valueMapper, list(rows)[1:])
        data = list(rows)
        
        if prof:
            profile(f=print_counts, data=data, strategy=strategy)
        else:
            print_counts(data=data, strategy=strategy)
                
            
if __name__ == '__main__':
    main(prof=True)
    main(prof=True, strategy="slow")
else:
    main()