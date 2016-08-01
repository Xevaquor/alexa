from spacy.en import English

import pygraphviz as PG

parser = English()


#
# multisentence = "There is an art, it says, or rather, a knack to flying." \
#                 "The knack lies in learning how to throw yourself at the ground and miss." \
#                 "In the beginning the Universe was created. This has made a lot of people "\
#                 "very angry and been widely regarded as a bad move."
#
# parsed = parser(multisentence)
#
# # for i, token in enumerate(parsed):
# #     print("original:", token.orth, token.orth_)
# #     print("lowercased:", token.lower, token.lower_)
# #     print("lemma:", token.lemma, token.lemma_)
# #     print("shape:", token.shape, token.shape_)
# #     print("prefix:", token.prefix, token.prefix_)
# #     print("suffix:", token.suffix, token.suffix_)
# #     print("log probability:", token.prob)
# #     print("Brown cluster id:", token.cluster)
# #     print("----------------------------------------")
# #     if i > 10:
# #         break
# sent = None
# for span in parsed.sents:
#     sent = [parsed[i] for i in range(span.start, span.end)]
#     break
#
# for token in sent:
#     print(token.orth_, token.pos_)
#
# print('----------------')
#

class Node:
    def __init__(self, value):
        self.value = value
        self.left = []
        self.right = []

    def traverse(self):
        print self.value
        for l in self.left:
            l.traverse()
        for r in self.right:
            r.traverse()


example = u"Avastin is also used for the treatment of adult patients with advanced non-small cell lung cancer"
parsedEx = parser(example)


def build_tree(token):
    root = Node('\n'.join([token.orth_, token.pos_, token.tag_]))
    root.left = [build_tree(x) for x in token.lefts]
    root.right = [build_tree(x) for x in token.rights]

    return root



# shown as: original token, dependency tag, head word, left dependents, right dependents
tree = None

for token in parsedEx:
    print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])
    if token.dep_ == u'ROOT':
        tree = build_tree(token)

tree.traverse()
g = PG.AGraph(directed=True, strict=True)

def makepic(tree, g):
    for l in tree.left:
        g.add_edge(tree.value, l.value, color='red')
        makepic(l, g)
    for l in tree.right:
        g.add_edge(tree.value, l.value, color='green')
        makepic(l, g)

makepic(tree, g)

# A = PG.AGraph(directed=True, strict=True)
#
# A.add_edge("7th Edition", "32V")
# A.add_edge("7th Edition", "Xenix")
# etc., etc.

# save the graph in dot format
g.write('ademo.dot')

# pygraphviz renders graphs in neato by default,
# so you need to specify dot as the layout engine
g.layout(prog='dot')
g.draw('tree.png')


# import nltk, re
# from nltk.corpus import wordnet as wn
# from pprint import pprint
#
# synset = wn.synset('cancer.n.01')
# root = synset.hypernym_paths()
# pprint(root)
# pprint(synset.lemma_names())
# pprint(synset.hyponyms())
# pprint('----------------------')
