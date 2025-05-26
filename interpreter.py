from k_base import load_knowledge_base, KnowledgeGraph, Node, Edge
import re
import json
import math
from abc import ABC, abstractmethod
from typing import List, Dict
import random
from mathematical_interpreter import *
from linguistic_interpreter import *


FRAC_TO_STR = {
    2: "половината",
    3: "една трета",
    4: "една четвърт"
}


def post_process(t):
    ret = ""
    prev_character = None
    after_punctuation = True
    for ch in t:
        if ch == " " and prev_character == " ":
            continue
        prev_character = ch
        if ch in ["?","!","."] and ret[-2:] not in ["лв","км","см"]:
            after_punctuation = True
        elif ch == " ":
            ch = ch
        elif after_punctuation:
            ch = ch.upper()
            after_punctuation = False
        ret += ch
    return ret

def process_string(q,ws,ns,prev_state,prev_noun,code_results,kb):
    
            while True:
                r = re.search('{(.*?)}', q)
                if r == None:
                    break
                item = list(map(lambda el: el.strip(),r.group(1).split(",")))
                
                add = ""
                if "gender" in item[0]:
                    r2 = re.search('\((.*?)\)', item[0])
                    #print("we have",ws)
                    gender = ws[r2.group(1)].gender
                    if gender == "f":
                        add += "а"
                    elif gender == "m":
                        add += ""
                elif item[0] in ns:
                    if len(item) == 3 and item[2] == "inv-str":
                        add = FRAC_TO_STR[ns[item[0]]]
                    else:
                        add = str(ns[item[0]])
                elif item[0] in ws:
                    el = ws[item[0]]
                    
                    if isinstance(el,Edge):
                        add = el.additions_required
                        el = kb.edge_to_verb[el.uid]
                    if item[0] in prev_state and len(item) == 1:
                        add = prev_state[item[0]][0]
                        
                        if el.cls == "noun":
                            
                            prev_noun = prev_state[item[0]][1]

                    elif item[0] not in prev_state:
                        
                        if el.cls == "verb":
                            verb_dependency = prev_state[item[2]][1]
                            tmp = getattr(el,f"present-{verb_dependency}")
                            
                            prev_state[item[0]] = (tmp,f"present-{verb_dependency}")
                            add = tmp + " " + add
                           
                        
                        elif el.cls == "adjective":
                            # print(el.cls)
                            add = getattr(el,"pl")
                            prev_state[item[0]] = (add,"plural")
                        elif el.cls == "name":
                            prev_noun = "singular"
                            add = el.uid
                            prev_state[item[0]] = (add,f"singular")
                        else:
                            if len(item) == 2:
                                prev_noun = "singular"
                                add = el.uid
                                prev_state[item[0]] = (add,f"singular")
                            else:
                                prev_noun = "plural"
                                add = el.plural
                                prev_state[item[0]] = (add,f"plural")
                        
                    else:
                        if item[1] == "passive":
                            
                            add = getattr(el,f"passive-singular")
                            add += "" if prev_noun == "singular" else "и"
                        elif item[1] == "plural":
                            if el.cls == "verb":
                                add = getattr(el,"present-plural")
                        elif item[1] == "historical-singular":
                            add = getattr(el,"historical-singular")
                        elif item[1] == "conj":
                            add = prev_state[item[0]][0]
                            if el.cls == "name":
                                add = add
                            elif prev_state[item[0]][1] == "plural":
                                
                                add += "те"
                            elif el.gender == "m":
                                if add[-2] in ["я","а","a"]:
                                    add += "ят"
                                else:
                                    add += "ът"
                            elif el.gender == "f":
                                add += "та"
                            elif el.gender == "n":
                                add += "то"
                elif item[0] in code_results:
                    add = code_results[item[0]]
                       

                                

                q = q[:r.span()[0]] + add + q[r.span()[1]:]
            
            return q,prev_state,prev_noun


            
            
            






