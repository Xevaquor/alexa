import uuid as uuid
from spacy.en import English
import pygraphviz as PG
import uuid
import threading
import os
import jsonpickle

def clean_file(filename):
    try:
        os.remove(filename)
    except:
        pass

class Node:
    def __init__(self):
        self.left = []
        self.right = []
        self.id = 0
        self.original = ''
        self.semantics = ''
        self.pos = ''
        self.tag = ''

    def get_node_text(self):
        return str(self.id) + ' ' + self.original + '\n' + self.semantics + '\n' + self.pos + '\n' + self.tag

    def traverse(self):
        for l in self.left:
            l.traverse()
        print self.value
        for r in self.right:
            r.traverse()


class SyntaxTreeBuilder:
    parser = English()

    def __init__(self):
        self.renderer = ImageTreeRenderer()

    def _build_tree(self, token):
        root = Node()
        root.original = token.orth_
        root.pos = token.pos_
        root.tag = token.tag_
        root.id = token.idx
        root.semantics = ''
        root.left = [self._build_tree(x) for x in token.lefts]
        root.right = [self._build_tree(x) for x in token.rights]
        return root

    def _parse(self, sentence):
        parsedEx = self.parser(sentence)
        for sentence in parsedEx.sents:
            root = [x for x in sentence if x.dep_ == u'ROOT'][0]
            yield self._build_tree(root)

    def build(self, sentence):
        forest = list(self._parse(sentence))
        storename = uuid.uuid4().hex + '.png'
        self.renderer.render(forest, storename)
        threading.Timer(3.0, clean_file, [storename]).start()
        return storename


class ImageTreeRenderer:
    def __init__(self):
        pass

    def _append_node(self, graph, node):
        for l in node.left:
            graph.add_edge(node.get_node_text(), l.get_node_text(), color='red')
            self._append_node(graph, l)
        for r in node.right:
            graph.add_edge(node.get_node_text(), r.get_node_text(), color='green')
            self._append_node(graph, r)

    def render(self, forest, filename):
        graph = PG.AGraph(directed=True, strict=True)
        for tree in forest:
            self._append_node(graph, tree)
        graph.layout(prog='dot')
        graph.draw(filename)

class PickleRenderer:
    def __init__(self):
        pass

    def render(self, forest, filename):
        return jsonpickle.encode(forest.__dict__)
