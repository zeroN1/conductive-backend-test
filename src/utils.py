import time

Fields = {
    "NcesId"        : "NCESSCH",
    "LeaId"         : "LEAID",
    "AuthorityName" : "LEANM05",
    "SchoolName"    : "SCHNAM05",
    "City"          : "LCITY05",
    "State"         : "LSTATE05",
    "Lat"           : "LATCOD",
    "Lon"           : "LONCOD",
    "MetroRank"     : "MLOCALE",
    "UrbanRank"     : "ULOCALE",
    "Status"        : "status05",
}

def formatSchoolName(name = ""):
    name = name.replace(" ", "|").replace("-", "").replace("||", "|")
    return name.lower()

def valueMapper(row):
    global Fields
    urank = row.get(Fields.get("UrbanRank"))
    mrank = row.get(Fields.get("MetroRank"))
    return {
        "ncesid": row.get(Fields.get("NcesId")),
        "status":row.get(Fields.get("Status")),
        "school":formatSchoolName(row.get(Fields.get("SchoolName"))),
        "city"  :row.get(Fields.get("City")),
        "state" :row.get(Fields.get("State")),
        "urank" :urank,
        "mrank" :mrank
    }
    
def profile(f, data, strategy):
    start = time.time()
    f(data, strategy)
    end = time.time()
    
    fname = f.__name__
    timems = (end-start) * 1000
    print("Function {} took {} millseconds".format(fname, timems))