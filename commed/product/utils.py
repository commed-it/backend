from functools import lru_cache

from .models import Category


@lru_cache(maxsize=1)
def get_nlp():
    import spacy
    print('imported spacy')
    return spacy.load("en_core_web_lg")


def category_similarity(tag_name):
    nlp = get_nlp()
    nlp_name = nlp(tag_name)
    cats = {cat: nlp(cat.name).similarity(nlp_name) for cat in Category.objects.all()}
    cats = dict(filter(lambda x: x[1] > 0.5, cats.items()))
    return cats
