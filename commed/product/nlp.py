from functools import lru_cache, reduce
from typing import List
from commed.settings import DEBUG
from .models import Category, Product

THRESHOLD = 0.5

@lru_cache(maxsize=1)
def get_nlp():
    import spacy
    if DEBUG:
        print('imported spacy')
    try:
        spacy.load("en_core_web_md")
    except:
        return spacy.load("commed/en_core_web_md")


def category_similarity(tag_name):
    nlp = get_nlp()
    nlp_name = nlp(tag_name)
    cats = {cat: nlp(cat.name).similarity(nlp_name) for cat in Category.objects.all()}
    cats = dict(filter(lambda x: x[1] > THRESHOLD, cats.items()))
    return cats


def search_by_tag(products, data):
    nlp = get_nlp()
    cats: List[Category] = list(reduce(lambda x, y: x.union(y), map(
        lambda tag:
        set(filter(lambda x:
                   nlp(x.name).similarity(nlp(tag['name'])) > THRESHOLD,
                   Category.objects.all())),
        data.pop('tags'))))
    result = set()
    for tag in reduce(lambda x, y: x.union(y),
                      (set(cat.tag_children.all()) for cat in cats), set()):
        result = result.union(products.filter(tag__name__contains=tag.name))
    result = list(result)
    return result