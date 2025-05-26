from abc import ABC, abstractmethod
import re
from k_base import load_knowledge_base, KnowledgeGraph, Node, Edge
import json
import math
from abc import ABC, abstractmethod
from typing import List, Dict
import random
class WordConditions(ABC):
    @abstractmethod
    def check(self,nd,kb,values):
        pass
class HaveVerbType(WordConditions):
    def __init__(self,tp):
        self.tp = tp
    def check(self,nd: Node,kb: KnowledgeGraph,values):
        for edg in nd.edges:
            if edg.nd2 == nd:
                continue
            if edg.uid == "adj":
                continue
            verb = kb.edge_to_verb[edg.uid]
            if self.tp in verb.types or self.tp == verb.uid:
                return True
        return False
class HaveAdjTypes(WordConditions):
    def __init__(self,tps):
        self.tps = tps
    def check(self,nd: Node,kb: KnowledgeGraph,values):
        # print("checking adj types of",nd.uid)
        for edg in nd.edges:
            if edg.nd2 == nd:
                continue
            if edg.uid != "adj":
                
                continue
            # print("has adj")
            adj = edg.nd2
            for tp in self.tps:
                if tp in adj.types:
                    # print("has type",tp)
                    return True
        # print("wont work")
        return False
class SameTypeAs(WordConditions):
    def __init__(self,other_noun):
        self.other_noun = other_noun
    def check(self,nd: Node,kb: KnowledgeGraph,values):
        
        if self.other_noun not in values:
            return False
        for tp in nd.types:
            if tp == "object":
                # print(tp)
                continue
            for tp2 in values[self.other_noun].types:
                if tp == tp2:
                    return True
        return False
class DifferentFrom(WordConditions):
    def __init__(self,ls):
        self.ls = ls
    
    def check(self,vl,kb,values):
        
        for itm in self.ls:
            if vl.uid == itm.uid:
                return False
        return True
class WordOperation(ABC):
    
    @abstractmethod
    def get(self,all_current,kb):
        pass

class RandomOne(WordOperation):
    def __init__(self,tp,conditions=[]):
        self.get_vl = True
        self.conditions = conditions
        self.tp = tp
        
    def get(self,all_current: Dict,kb: KnowledgeGraph,condtitions: List[WordConditions]):
        condtitions.append(DifferentFrom(list(all_current.values())))
        viable = kb.get_random(self.tp)
        # print("need",self.tp)
        i = 0
        while i < len(viable):
            incrm = True
            if len(self.conditions) > 0:
                incrm = False
                for c in self.conditions:
                    # print(viable[i].uid,viable[i].types)
                    if hasattr(viable[i],"types") and c in viable[i].types and c not in viable[i].defining_types:
                        incrm = True
                        break
            for c in condtitions:
                if not c.check(viable[i],kb,all_current):
                    
                    incrm = False
                    break
           
            
            if incrm:
                i += 1
            else:
                del viable[i]
        # print(viable)
        if len(viable) == 0:
            return None
        return viable[random.randint(0,len(viable)-1)]

class Is(WordOperation):
    def __init__(self,dependent):
        self.dependent = dependent

    def get(self,all_current: Dict,kb: KnowledgeGraph,condtitions: List[WordConditions]):
        return Node("verb","is",**{"present-singular": "е","present-plural": "са","historical-singular": "бил","historical-plural": "били","passive-singular": "бил"})
class NounToVerb(WordOperation):
    def __init__(self,noun,tp):
        self.noun = noun
        self.tp = tp
    
    def get(self,all_current: Dict,kb: KnowledgeGraph,condtitions: List[WordConditions]):
        if self.noun not in all_current:
            return None
        n: Node = all_current[self.noun]
        condtitions.append(DifferentFrom(list(all_current.values())))
        viable = n.edges.copy()
        # print("need verb",self.tp)
        i = 0
        while i < len(viable):
            incrm = True
            works = False
            edg = viable[i]
            if edg.uid != "adj":

                if edg.nd1 == n and  self.tp in kb.edge_to_verb[edg.uid].types:
                    works = True

            if not works:
                incrm = False
        

            if incrm:
                i += 1
            else:
                del viable[i]
        if len(viable) == 0:
            
            return None
        choice = random.randint(0,len(viable)-1)
       
        for idx,edg in enumerate(viable):

            if idx == choice:
                
                return edg

    
class NounToAdj(WordOperation):
    def __init__(self,noun,tps):
        self.noun = noun
        self.tps = tps
    
    def get(self,all_current: Dict,kb: KnowledgeGraph,condtitions: List[WordConditions]):
        if self.noun not in all_current:
            return None
        n: Node = all_current[self.noun]
        condtitions.append(DifferentFrom(list(all_current.values())))
        viable = n.edges.copy()
        for v in viable:
            if v.uid != "adj":
                continue
            # print(v.nd2.uid)
        i = 0
        while i < len(viable):
            works = False
            edg = viable[i]
            
            if edg.nd1 == n and edg.uid == "adj":
                for tp in self.tps:
                    # print("need type",tp,edg.nd2.uid,edg.nd2.types)
                    if tp in edg.nd2.types:
                        works = True
                        # print("we can put ",edg.nd2.uid)
                        break

            if works:
                i += 1
            else:
                del viable[i]
        if len(viable) == 0:
            return None
        choice = random.randint(0,len(viable)-1)
       
        for idx,edg in enumerate(viable):

            if idx == choice:
                # print("we choose ",edg.nd2.uid)
                return edg.nd2


class NounToNoun(WordOperation):
    def __init__(self,noun,verb):
        self.noun = noun
        self.verb = verb
    
    def get(self,all_current: Dict,kb: KnowledgeGraph,condtitions: List[WordConditions]):
        if self.noun not in all_current:
            return None
        condtitions.append(DifferentFrom(list(all_current.values())))
        
        viable = []
        for edg in all_current[self.noun].edges:
            # print(edg.uid,self.verb)
            if edg.uid == self.verb:
                viable.append(edg.nd2)

        
        
        i = 0
        while i < len(viable):
            incrm = True
            for c in condtitions:
                
                if not c.check(viable[i],kb,all_current):
                    
                    incrm = False
                    break
            if incrm:
                i += 1
            else:
                del viable[i]
        
        if len(viable) == 0:
            return None
        return random.choice(viable)

class VerbToNoun(WordOperation):
    def __init__(self,verb):
        self.verb = verb
    
    def get(self,all_current: Dict,kb: KnowledgeGraph,condtitions: List[WordConditions]):
        if self.verb not in all_current:
            return None
        condtitions.append(DifferentFrom(list(all_current.values())))
        
        viable = []
        for edg in all_current[self.verb].nd1.edges:
            # print(edg.uid,self.verb)
            if edg.uid == all_current[self.verb].uid:
                viable.append(edg.nd2)

        
        
        i = 0
        while i < len(viable):
            incrm = True
            for c in condtitions:
                
                if not c.check(viable[i],kb,all_current):
                    
                    incrm = False
                    break
            if incrm:
                i += 1
            else:
                del viable[i]
        
        if len(viable) == 0:
            return None
        return random.choice(viable)

def get_all_words(q,a,word_conditions,kb):
    mem: Dict[str,List[Operation]] = {}
    q_words = re.findall('{(.*?)}', q)
    a_words = re.findall('{(.*?)}', a)
    q_words.extend(a_words)
    conditions = {}
    for literal in q_words:
        if "int" in literal or "float" in literal:
            continue
        literal = list(map(lambda el: el.strip(),literal.split(",")))
        if literal[0] in mem:
            continue
        if len(literal) == 1:
            continue
        mem[literal[0]] = []
        if literal[0] not in conditions:
            conditions[literal[0]] = []
        # print(literal)
        if len(literal) == 2 or literal[2] == "plural":
            
            literal[1] = list(map(lambda el: el.strip(),literal[1].split("-")))
            tp = literal[1][0]
            if len(literal[1]) > 1:
                literal[1] = list(map(lambda el: el.strip(),literal[1][1].split("+")))
            else:
                literal[1] = []
            mem[literal[0]].append(RandomOne(tp,literal[1]))
            continue
        elif len(literal) == 3:
            if literal[1] == "is":

                mem[literal[0]].append(Is(literal[2]))
            elif literal[1] in ["verb","work","activity"]:
                mem[literal[0]].append(NounToVerb(literal[2],literal[1]))
                if literal[2] not in conditions:
                    conditions[literal[2]] = []
                
                conditions[literal[2]].append(HaveVerbType(literal[1]))         
            elif literal[1] == "noun":
                
                mem[literal[0]].append(VerbToNoun(literal[2]))
            elif "adj" in literal[1]:
                
                literal[1] = list(map(lambda el: el.strip(),literal[1].split("-")))[1]
                literal[1] = list(map(lambda el: el.strip(),literal[1].split("+")))
                # print("ADJECTIVE!! with types",literal[1])
                mem[literal[0]].append(NounToAdj(literal[2], literal[1]))
                conditions[literal[2]].append(HaveAdjTypes(literal[1]))        
            elif "--" in literal[1]:
                literal[1] = list(map(lambda el: el.strip(),literal[1].split("--")))
                
                tp = literal[1][0]
                descriptor = literal[1][1]
                depdendent = literal[2]
                # print(descriptor,depdendent)
                mem[literal[0]].append(NounToNoun(depdendent,descriptor))
                conditions[literal[2]].append(HaveVerbType(descriptor))   
    # print(word_conditions)
    for k,c in word_conditions.items():
        for v in c:
            if k not in mem:
                continue
            if "sameas" in v:
                
                conditions[k].append(SameTypeAs(v[7:-1]))
    solutions = []
    attempts = 0
    # print(mem)
    while len(solutions) < 5:
        settled = {}
        while len(settled) < len(mem):
            # print(settled,mem)
            before = len(settled)
            for k,v in mem.items():
                
                if k in settled:
                    continue
                
                ret = None
                for c in v:
                    # print("getting ",k)
                    ret = c.get(settled,kb,conditions[k])
                    if ret != None:
                        break
                if ret != None:
                    # print(k,"is",ret.uid)
                    settled[k] = ret
            if len(settled) == before:
                
                break
        success = len(settled) == len(mem)
        
        if success:    
            
            can_keep = False
            if len(solutions) == 0 and len(settled) > 0:
                can_keep = True

            for s in solutions:
                if can_keep:
                    break
                for k,v in settled.items():
                    
                    if s[k] != v:
                        can_keep = True
                        break
            if can_keep:
                attempts = 0
                solutions.append(settled)
            else:
                attempts += 1
        else:
            attempts += 1

        if attempts == 5:
            # print("FAILED")
            break

    return solutions