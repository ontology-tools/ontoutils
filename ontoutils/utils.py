import re


def quoteIfNeeded(value):
    # first check if already existing quotes
    if not (value[0]=="'" and value[-1]=="'"):
        if " " in value:
            return( "\'"+value+"\'")
    return(value)


quoted = re.compile("(?<=')[^']+(?=')")
