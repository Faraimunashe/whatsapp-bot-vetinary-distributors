import re
from get_int import integer
from models import Product

def qouter(string):
    pattern = r"[Xx][1-9][0-9]*"

    matches = re.findall(pattern, string)
    prodpattern = rf'(\w+)\s*(?:\b(?:{"|".join(matches)})\b)'
    prodmatch = re.findall(prodpattern, string)
    print(prodmatch, matches)

    if prodmatch:
        i=0
        for sch in prodmatch:
            prod = Product.query.filter(Product.tags.like(sch)).first()
            print(prod.price * integer(matches[i]))
            i=i+1



