import sys
import json
import networkx as nx
from networkx import dfs_tree
from networkx.readwrite import json_graph
from scrape import Wikipedia
import urllib
import random

WIKI = "Google"
master_graph = nx.Graph()

def processable_node(node):
    if node.dist <= 3:
       return True
    else:
       return False

def traverse_graph(graph, source, dump=list(), depth=0):
    if source not in dump and depth < 4:
        print source
        links = Wikipedia(source).request()
        links = sorted(links)
        dump.append(source)
            
        size = 5 - depth if len(links) > 5 else len(links)
        for link in random.sample(links, size):
            add_node_to_graph(graph, source, link, depth)
            traverse_graph(graph, link, dump, depth+1)

    # for node in graph.neighbors(source):

    return graph

def add_node_to_graph(graph, parent, node, depth):
    name = urllib.unquote(node.encode('UTF-8'))
    graph.add_node(node, name=name, depth=depth, url=Wikipedia(node).to_url())
    if parent:
        graph.add_edge(parent, node)

def save_to_jsonfile(filename, graph):
    g_json = json_graph.node_link_data(graph)
    json.dump(g_json, open(filename, 'w'))

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        WIKI = sys.argv[1]

    add_node_to_graph(master_graph, None, WIKI, -1)

    traverse_graph(master_graph, WIKI)

    save_to_jsonfile("wikipedia.json", master_graph)


