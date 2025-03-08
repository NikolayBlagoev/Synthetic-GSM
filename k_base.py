import pandas as pd
from typing import List
class Edge(object):
    def __init__(self,nd1,nd2,uid,additions_required = [],degree = 0):
        self.nd1 = nd1
        self.nd2 = nd2
        self.uid = uid
        self.additions_required = additions_required
        self.degree = degree
class Node(object):
    def __init__(self,cls,uid,**kwargs):
        self.cls = cls
        self.uid = uid
        self.plural = uid
        for k,v in kwargs.items():
            
            setattr(self,k,v)
        self.edges: List[Edge] = []

    def has_con_to(self,nd2):
        for edg in self.edges:
            if nd2 == edg.nd1 or nd2 == edg.nd2:
                return True
        return False
        
class KnowledgeGraph(object):
    def __init__(self,nouns,verbs,adjectives,names,connection_fp):
        
        self.nouns = []
        for k,v in nouns.items():
            self.nouns.append(Node("noun",k,**v))
        self.verbs = []
        self.edge_to_verb = {}
        for k,v in verbs.items():
            self.verbs.append(Node("verb",k,**v))
            self.edge_to_verb[k] = self.verbs[-1]
        
        
        self.adjectives = []
        self.edge_to_adj = {}
        for k,v in adjectives.items():
            self.adjectives.append(Node("adjective",k,**v))
            self.edge_to_adj[k] = self.adjectives[-1]
        self.names = []
        for k,v in names.items():
            self.names.append(Node("name",k,**v))
        self.edges = []
        self.form_connections(connection_fp)

    def get_random(self,tp):
        viable = []
        if "noun" in tp and "name" in tp:
            # print("nouns and names",len(self.nouns),len(self.names))
            viable = self.nouns.copy()
            viable.extend(self.names.copy())
            # print(len(viable))
        elif "noun" in tp:
            viable = self.nouns.copy()
        elif "name" in tp:
            viable = self.names.copy()
        elif "verb" in tp:
            viable = self.verbs.copy()
        elif "adj" in tp:
            viable = self.adjectives.copy()
        
        return viable
        
        
        

        
    def filter_nodes(self,properties,nodes):
        if "(" in properties:
            properties = properties[1:-1]
            for nd in self.nouns:
                if nd in nodes:
                    continue
                if properties in nd.types:
                    
                    nodes.append(nd)
            for nd in self.adjectives:

                if nd in nodes:
                    continue
                if properties in nd.types:
                    
                    nodes.append(nd)
        elif "{" in properties:
            properties = properties[1:-1]
            for nd in self.nouns:
                if nd in nodes:
                    continue
                if nd.cls == properties:
                    nodes.append(nd)
            for nd in self.names:
                if nd in nodes:
                    continue
                if nd.cls == properties:
                    nodes.append(nd)
        else:
            for nd in self.nouns:
                if nd in nodes:
                    continue
                if nd.uid == properties:
                    nodes.append(nd)
            for nd in self.adjectives:
                if nd in nodes:
                    continue
                if nd.uid == properties:
                    nodes.append(nd)
            for nd in self.names:
                if nd in nodes:
                    continue
                if nd.uid == properties:
                    nodes.append(nd)     
        return nodes
    def filter_edges(self,properties,nodes,edges):
        if "(" in properties:
            properties = properties[1:-1]
            for edg in self.edges:
                if edg.uid not in edges:
                    continue
                if edg.nd2 in nodes:
                    continue
                if properties in edg.nd2.types:
                    nodes.append((edg.uid,edg.additions_required,edg.nd2))  
        elif "{" in properties:
            properties = properties[1:-1]
            for edg in self.edges:
                if edg.uid not in edges:
                    continue
                if edg.nd2 in nodes:
                    continue
                if edg.nd2.cls == properties:
                    nodes.append((edg.uid,edg.additions_required,edg.nd2))  
        else:
            for edg in self.edges:
                if edg.uid not in edges:
                    continue
                if edg.nd2 in nodes:
                    continue
                if edg.nd2.uid == properties:
                    nodes.append((edg.uid,edg.additions_required,edg.nd2))  
        return nodes
    def interpret_node(self,ls):
        ls = list(map(lambda el: el.strip(), ls.split(",")))
        nodes = []
        for el in ls:

            nodes = self.filter_nodes(el,nodes)
       
        return nodes
    def interpret_suitable(self,ls,verbs):
        ls = list(map(lambda el: el.strip(), ls.split(",")))
        verbs = list(map(lambda el: el[0], verbs))
        nodes = []
        for el in ls:
            el = el[1:]
            nodes = self.filter_edges(el,nodes,verbs)
       
        return nodes

    def filter_verbs(self,properties,edges,addition = ""):
        if "(" in properties:
            properties = properties[1:-1]
            for nd in self.verbs:
                
                if properties in nd.types:
                    edges.append((nd.uid,addition))
       
        else:
            
            for nd in self.verbs:
                
                if nd.uid == properties:
                    edges.append((nd.uid,addition))     
        return edges
    def interpret_verbs(self,ls):
        ls = list(map(lambda el: el.strip(), ls.split(",")))
        edges = []
        for el in ls:
            addition = ""
            if "+" in el:
                addition = el.split("+")[1].strip()
                el = el.split("+")[0].strip()

            edges = self.filter_verbs(el,edges,addition)
        return edges
    def form_connections(self,fp):
        buffer = []
        degree = 0
        lines = []
        with open(fp,"r",encoding='utf-8') as fd:
            for ln in fd.readlines():
                if "-" not in ln:
                    continue
                lines.append(list(map(lambda el: el.strip(), ln.split("-"))))
        
        
        while len(lines) > 0:
            i = 0
            # print(degree,len(lines))
            while i < len(lines):
                el = lines[i]
                
                if len(el) == 3:
                    if ("*" in el[0] or "*" in el[1] or "*" in el[2]) and degree < 3:
                        i += 1
                        continue
                    elif degree == 3:
                        l = self.interpret_node(el[0][1:-1])
                        m = self.interpret_verbs(el[1][1:-1])
                        
                        r = self.interpret_suitable(el[2][1:-1],m)
                        for noun1 in l:
                       
                            for noun2 in r:
                                if noun1.has_con_to(noun2[2]):
                                    continue
                                tmp = Edge(noun1,noun2[2],noun2[0],noun2[1],degree)
                                self.edges.append(tmp)
                                noun1.edges.append(tmp)
                                noun2[2].edges.append(tmp)
                                # print(noun1.uid," can be ", noun2[0], " to ",noun2[2].uid)
                        del lines[i]
                        continue
                    if ("{" in el[0] or "{" in el[1] or "{" in el[2]) and degree < 2:
                        i += 1
                        continue
                    if (")" in el[0] or ")" in el[1] or ")" in el[2]) and degree < 1:
                        i += 1
                        continue
                    # print(el,len(el))
                    l = self.interpret_node(el[0][1:-1])
                    m = self.interpret_verbs(el[1][1:-1])
                    
                    r = self.interpret_node(el[2][1:-1])
                    
                    
                    for noun1 in l:
                        for v in m:
                            for noun2 in r:
                                if noun1.has_con_to(noun2):
                                    
                                    continue
                                # print(noun1.uid,"connected to",noun2.uid,"via",v[0])
                                tmp = Edge(noun1,noun2,v[0],v[1],degree)
                                self.edges.append(tmp)
                                noun1.edges.append(tmp)
                                noun2.edges.append(tmp)
                                # print(noun1.uid," can be ", v[0], " to ",noun2.uid)
                    
                    del lines[i]
                elif len(el) == 2:
                    if ("*" in el[0] or "*" in el[1]) and degree < 3:
                        i += 1
                        continue
                    elif degree == 3:
                        del lines[i]
                        continue
                    if ("{" in el[0] or "{" in el[1]) and degree < 2:
                        i += 1
                        continue
                    if (")" in el[0] or ")" in el[1]) and degree < 1:
                        i += 1
                        continue
                    # print(el,len(el))
                    
                    l = self.interpret_node(el[0][1:-1])
                    
                    
                    r = self.interpret_node(el[1][1:-1])
                    
                    
                    for noun1 in l:
                        
                        for noun2 in r:
                                if noun1.has_con_to(noun2):
                                    
                                    continue
                                tmp = Edge(noun1,noun2,"adj","",degree)
                                self.edges.append(tmp)
                                noun1.edges.append(tmp)
                                noun2.edges.append(tmp)
                                
                    
                    del lines[i]
                else:
                    del lines[i]



                

            degree += 1
        

def load_knowledge_base():
    nouns = pd.read_csv("knowledge_base/nouns/list.csv")
    tmp = {}
    for index, row in nouns.iterrows():
        types = []
        defining_types = []
        for v in row['type'].split("-"):
            if "(" in v:
                types.append(v[1:-1])
                defining_types.append(v[1:-1])
            else:
                types.append(v)

        tmp[row['noun']] = {
            "noun": row['noun'],
            "gender":row["gender"],
            "plural":row["plural"],
            "types":types,
            "defining_types":defining_types
        }
    nouns = tmp

    names = pd.read_csv("knowledge_base/names/list.csv")
    tmp = {}
    for index, row in names.iterrows():
        

        tmp[row['name']] = {
            "name": row['name'],
            "gender":row["gender"]
        
        }
    names = tmp

    verbs = pd.read_csv("knowledge_base/verbs/list.csv")
    tmp = {}
    
    for index, row in verbs.iterrows():
    
        tmp[row['present-singular']] = {
            "present-singular": row['present-singular'],
            "present-plural":row["present-plural"],
            "historical-singular":row["historical-singular"],
            "passive-singular":row["passive-singular"],
            "types":row["type"].split("-"),
        
        }
    verbs = tmp

    adjectives = pd.read_csv("knowledge_base/adjectives/list.csv")
    tmp = {}
    
    for index, row in adjectives.iterrows():
    
        tmp[row['m']] = {
            "m": row['m'],
            "f":row["f"],
            "n":row["n"],
            "pl":row["pl"],
            "types":row["type"].split("-"),
        
        }
    
    adjectives = tmp
    return KnowledgeGraph(nouns,verbs,adjectives,names,"knowledge_base/connections.txt")


