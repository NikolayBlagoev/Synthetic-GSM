from abc import ABC, abstractmethod
import re
from typing import List, Dict
import random
import math

def binary_gcd(a,b):
    if a == 0 and b != 0:
        return b
    if a != 0 and b == 0:
        return a
    if a % 2 == 0 and b % 2 == 0:
        return 2*binary_gcd(a >> 1, b >> 1)
    if a % 2 == 1 and b % 2 == 0:
        return binary_gcd(a, b >> 1)
    if a % 2 == 0 and b % 2 == 1:
        return binary_gcd(a >> 1, b)
    if a >= b:
        return binary_gcd(a - b, b)
    if b > a:
        return binary_gcd(a, b - a)
    return 1
class Operation(ABC):
    @abstractmethod
    def check(self,vl,all_current):
        pass
    @abstractmethod
    def get(self,all_current):
        pass
   
class RandomInteger(Operation):
    def __init__(self, a, b, skip):
        self.get_vl = True
        self.a = a
        self.b = b+1
        self.skip = skip
    def check(self,vl,all_current):
        return vl >= self.a and vl <= self.b and (vl - self.a) % self.skip == 0
    def get(self,all_current):
        return random.randrange(self.a,self.b,self.skip)
    
class RandomFloat(Operation):
    def __init__(self, a, b, f_point):
        self.get_vl = True
        self.a = a
        self.b = b+1
        self.f_point = f_point
    def check(self,vl,all_current):
        return vl >= self.a and vl <= self.b
    def get(self,all_current):
        temp = random.uniform(self.a,self.b)
        return round(temp, self.f_point)

class NonPrime(Operation):
    def __init__(self):
        self.get_vl = False
        
    def check(self,vl,all_current):
        
        for v in range(2,math.floor(math.sqrt(vl))):
            if vl % v == 0:
                return True
        return False
    def get(self,all_current):
        return None

class GCD(Operation):
    def __init__(self, a, b):
        self.get_vl = False
        self.a = a
        self.b = b
    
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            
            b = self.b
        elif isinstance(self.b, str):
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        a = None
        if isinstance(self.a,int):
            a = self.a
        elif isinstance(self.a, str):
            if self.a not in all_current:
                return False
            a = all_current[self.a]
        return vl == binary_gcd(a,b)
        
    def get(self,all_current):
        b = None
        if isinstance(self.b,int):
            
            b = self.b
        elif isinstance(self.b, str):
            if self.b not in all_current:
                return None
            b = all_current[self.b]
        a = None
        if isinstance(self.a,int):
            a = self.a
        elif isinstance(self.a, str):
            if self.a not in all_current:
                return None
            a = all_current[self.a]
        return binary_gcd(a,b)


class LCM(Operation):
    def __init__(self, a, b):
        self.get_vl = False
        self.a = a
        self.b = b
    
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            
            b = self.b
        elif isinstance(self.b, str):
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        a = None
        if isinstance(self.a,int):
            a = self.a
        elif isinstance(self.a, str):
            if self.a not in all_current:
                return False
            a = all_current[self.a]
        return vl == a*b/binary_gcd(a,b)
        
    def get(self,all_current):
        b = None
        if isinstance(self.b,int):
            
            b = self.b
        elif isinstance(self.b, str):
            if self.b not in all_current:
                return None
            b = all_current[self.b]
        a = None
        if isinstance(self.a,int):
            a = self.a
        elif isinstance(self.a, str):
            if self.a not in all_current:
                return None
            a = all_current[self.a]
        return a*b/binary_gcd(a,b)

class Modulo(Operation):
    def __init__(self,b,direction):
        self.get_vl = False
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        self.direction = direction
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            
            b = self.b
        elif isinstance(self.b, str):
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        if self.direction == 0:
            
            return vl % b == 0
        else:
            
            return b % vl == 0
        
    def get(self,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        elif isinstance(self.b, str):
            if self.b not in all_current:
                return None
            b = all_current[self.b]
        if self.direction == 0:
            
            return None
        else:
            ls = []
            for v in range(2,b):
                if b % v == 0:
                    ls.append(v)
            return random.choice(ls)

class LT(Operation):
    def __init__(self,b):
        self.get_vl = False
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        
        return b > vl
        
    def get(self,all_current):
        return None

class GT(Operation):
    def __init__(self,b):
        self.get_vl = False
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        
        return b < vl
        
    def get(self,all_current):
        return None
class Eq(Operation):
    def __init__(self,b):
        self.get_vl = False
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        
        return b == vl
        
    def get(self,all_current):
        return None
class CeilOp(Operation):
    def __init__(self,b):
        self.get_vl = True
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        
        return vl == math.ceil(b)
        
    def get(self,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
            
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return None
            b = all_current[self.b]
        
        return math.ceil(b)
class FloorOp(Operation):
    def __init__(self,b):
        self.get_vl = True
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        
        return vl == math.floor(b)
        
    def get(self,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
            
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return None
            b = all_current[self.b]
        
        return math.floor(b)
class Different(Operation):
    def __init__(self,b):
        self.get_vl = False
        try:
            self.b = int(b)
        except ValueError:
            self.b = b
        
        
    def check(self,vl,all_current):
        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        
        return b != vl
        
    def get(self,all_current):
        return None
class SumAll(Operation):
    def __init__(self,vls):
        self.dependencies = []

        self.get_vl = True
        for el in vls:
            try:
                el = int(el)
            except ValueError:
                el = el
                self.get_vl = False
            self.dependencies.append(el)
        
    def check(self,vl,all_current):
        sm = 0
        for dp in self.dependencies:
            if isinstance(dp,int):
                sm += dp
                continue
            if not dp in all_current:
                return False
            sm += all_current[dp]
        return sm == vl
    def get(self,all_current):
        sm = 0
        for dp in self.dependencies:
            if isinstance(dp,int):
                sm += dp
                continue
            if not dp in all_current:
                return None
            sm += all_current[dp]

        return sm

class MultAll(Operation):
    def __init__(self,vls):
        self.dependencies = []

        self.get_vl = True
        for el in vls:
            try:
                el = int(el)
            except ValueError:
                el = el
                self.get_vl = False
            self.dependencies.append(el)
        
    def check(self,vl,all_current):
        sm = 1
        for dp in self.dependencies:
            if isinstance(dp,int):
                sm *= dp
                continue
            if not dp in all_current:
                return False
            sm *= all_current[dp]
        return sm == vl
    def get(self,all_current):
        sm = 1
        for dp in self.dependencies:
            if isinstance(dp,int):
                sm *= dp
                continue
            if not dp in all_current:
                return None
            sm *= all_current[dp]

        return sm

class SubAll(Operation):
    def __init__(self,vls):
        self.dependencies = []

        self.get_vl = True
        for el in vls:
            try:
                el = int(el)
            except ValueError:
                el = el
                self.get_vl = False
            self.dependencies.append(el)
        
    def check(self,vl,all_current):
        sm = None
        for dp in self.dependencies:
            if isinstance(dp,int):
                if sm == None:
                    sm = dp
                else:
                    sm -= dp
                continue
            if not dp in all_current:
                return False
            if sm == None:
                sm =  all_current[dp]
            else: 
                sm -= all_current[dp]
        return sm == vl
    def get(self,all_current):
        sm = None
        for dp in self.dependencies:
            if isinstance(dp,int):
                if sm == None:
                    sm = dp
                else:
                    sm -= dp
                continue
            if not dp in all_current:
                return None
            if sm == None:
                sm = all_current[dp]
            else: 
                sm -= all_current[dp]
        return sm
class DivAll(Operation):
    def __init__(self,vls):
        self.dependencies = []

        self.get_vl = True
        for el in vls:
            try:
                el = int(el)
            except ValueError:
                el = el
                self.get_vl = False
            self.dependencies.append(el)
        
    def check(self,vl,all_current):
        sm = None
        for dp in self.dependencies:
            if isinstance(dp,int):
                if sm == None:
                    sm = dp
                else:
                    sm = sm/dp
                continue
            if not dp in all_current:
                return False
            if sm == None:
                sm =  all_current[dp]
            else: 
                sm = sm/all_current[dp]
        return sm == vl
    def get(self,all_current):
        sm = None
        for dp in self.dependencies:
            if isinstance(dp,int):
                if sm == None:
                    sm = dp
                else:
                    sm = sm/dp
                continue
            if not dp in all_current:
                
                return None
            if sm == None:
                sm = all_current[dp]
            else: 
                sm = sm/all_current[dp]
        return sm


class WholeDivAll(Operation):
    def __init__(self,vls):
        self.dependencies = []

        self.get_vl = True
        for el in vls:
            try:
                el = int(el)
            except ValueError:
                el = el
                self.get_vl = False
            self.dependencies.append(el)
        
    def check(self,vl,all_current):
        sm = None
        for dp in self.dependencies:
            if isinstance(dp,int):
                if sm == None:
                    sm = dp
                else:
                    sm = sm//dp
                continue
            if not dp in all_current:
                return False
            if sm == None:
                sm =  all_current[dp]
            else: 
                sm = sm//all_current[dp]
        return sm == vl
    def get(self,all_current):
        sm = None
        for dp in self.dependencies:
            if isinstance(dp,int):
                if sm == None:
                    sm = dp
                else:
                    sm = sm//dp
                continue
            if not dp in all_current:
                
                return None
            if sm == None:
                sm = all_current[dp]
            else: 
                sm = sm//all_current[dp]
        return sm

class Remainder(Operation):
    def __init__(self,a, b):
        self.get_vl = True
        self.a = a
        self.b = b
    def check(self, vl, all_current):
        a = None
        if isinstance(self.b,int):
            a = self.b
        
        elif isinstance(self.b, str):
            
            if self.a not in all_current:
                return False
            a = all_current[self.a]

        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return False
            b = all_current[self.b]
        if a < b:
            return False

        return a%b

    def get(self, all_current):
        a = None
        if isinstance(self.b,int):
            a = self.b
        
        elif isinstance(self.b, str):
            
            if self.a not in all_current:
                return False
            a = all_current[self.a]

        b = None
        if isinstance(self.b,int):
            b = self.b
        
        elif isinstance(self.b, str):
            
            if self.b not in all_current:
                return None
            b = all_current[self.b]
        if a < b:
            return None

        return a%b


def get_all_numbers(q,a,constraints):
    mem: Dict[str,List[Operation]] = {}
    q_ints = re.findall('{(.*?)}', q)
    a_ints = re.findall('{(.*?)}', a)
    q_ints.extend(a_ints)
    
    for literal in q_ints:
        if "int" not in literal:
            continue
        literal = list(map(lambda el: el.strip(),literal.split(",")))
        if literal[0] in mem:
            continue
        mem[literal[0]] = []
        
        if len(literal) == 2:
            continue
        if len(literal) == 1:
            continue
        if "inv" in literal[2]:
            continue
        if len(literal) == 4:
            literal.append("1")
        
        mem[literal[0]].append(RandomInteger(int(literal[2]), int(literal[3]), int(literal[4])))

    for k,v in constraints.items():
        ls = []
        if k not in mem:
            mem[k] = []
        for c in v:
            c = c.replace("{","").replace("}","")
            if c == "non-prime":
                ls.append(NonPrime())
            elif "randint" in c:
                vls = c[8:-1].split(",")
                if len(vls) == 2:
                    vls.append("1")
                ls.append(RandomInteger(int(vls[0]), int(vls[1]), int(vls[2])))
            elif "randfloat" in c:
                vls = c[10:-1].split(",")
                if len(vls) == 2:
                    vls.append("1")
                ls.append(RandomFloat(float(vls[0]), float(vls[1]), int(vls[2])))
            elif "+" in c:
                vls = list(map(lambda el: el.strip(), c.split("+")))
                ls.append(SumAll(vls))
            elif "-" in c:
                vls = list(map(lambda el: el.strip(), c.split("-")))
                ls.append(SubAll(vls))
            elif "!" in c:
                vls = list(map(lambda el: el.strip(), c.split("!")))
                ls.append(Different(vls[1]))
            
            elif "//" in c:
                vls = list(map(lambda el: el.strip(), c.split("//")))
               
                ls.append(WholeDivAll(vls))
            elif "/" in c:
                vls = list(map(lambda el: el.strip(), c.split("/")))
                ls.append(DivAll(vls))
            elif "*" in c:
                vls = list(map(lambda el: el.strip(), c.split("*")))
                ls.append(MultAll(vls))
            elif "<" in c:
                vls = list(map(lambda el: el.strip(), c.split("<")))
                ls.append(LT(vls[1]))
            elif ">" in c:
                vls = list(map(lambda el: el.strip(), c.split(">")))
                ls.append(GT(vls[1]))
            elif "=" in c:
                vls = list(map(lambda el: el.strip(), c.split("=")))
                ls.append(Eq(vls[1]))
            elif "%" in c:
                vls = list(map(lambda el: el.strip(), c.split("%")))
                # print(k," modulo ",vls[1])
                if vls[1] == k:
                   
                    ls.append(Modulo(vls[0],1))
                else:
                    ls.append(Modulo(vls[1],0))
            elif "ceil" in c:
                vls = list(map(lambda el: el.strip(), c.split("ceil")))
                ls.append(CeilOp(vls[1]))
            elif "floor" in c:
                vls = list(map(lambda el: el.strip(), c.split("floor")))
                ls.append(FloorOp(vls[1]))
            elif "gcd" in c:
                vls = list(map(lambda el: el.strip(), c.split("gcd")))
                ls.append(GCD(vls[1],vls[2]))
            elif "lcm" in c:
                vls = list(map(lambda el: el.strip(), c.split("lcm")))
                ls.append(LCM(vls[1],vls[2]))
            elif "rem" in c:
                vls = list(map(lambda el: el.strip(), c.split("rem")))
                ls.append(Remainder(vls[0],vls[1]))
        mem[k].extend(ls)



    solutions = []
    attempts = 0
    while len(solutions) < 5:
        settled = {}
        while len(settled) < len(mem):
            
            for k,v in mem.items():
                print(settled)
                if k in settled:
                    continue
                
                ret = None
                for c in v:
                    ret = c.get(settled)
                    if ret != None:
                        break
                if ret != None:
                    
                    settled[k] = ret
        success = True
        for k,v in mem.items():
            if not success:
                break
            for c in v:
                success = c.check(settled[k],settled)
                
                if success == False:
                    break
        if success:    
            attempts = 0
            solutions.append(settled)
        else:
            attempts += 1

        if attempts == 20:
            break
    return solutions