#%%
from pathlib import Path
from dataclasses import dataclass, field
import matplotlib.pyplot as plt 

import time 

DATA_PATH = Path("data/")

with (DATA_PATH / "input.txt").open() as infile: 
    data = infile.read()
    data = data.split("\n")   


#%%


@dataclass
class Rope():
    x: int = 0 
    y: int = 0
    history:list = field(default_factory=list)
    #history_x: list = field(default_factory=list)
    #history_y: list = field(default_factory=list) 

    def is_attached(self, other):
        if abs(other.x - self.x) > 1: 
            return False 
        if abs(other.y - self.y) > 1: 
            return False 
        return True 
    
    def follow(self, other): 
        
        if other.x > self.x: 
            if other.y < self.y: 
                self.move("D")
            elif other.y > self.y:
                self.move("U")
            self.move("R")

        elif other.x < self.x: 
            if other.y < self.y: 
                self.move("D")
            elif other.y > self.y:
                self.move("U")
            self.move("L")

        elif (other.y > self.y): 
            self.move("U")
        
        elif (other.y < self.y): 
            self.move("D")

        else: 
            print("i did not move!")
            return 


    def move(self, direction): 
        x, y = move(direction, self.x, self.y)
        
        #self.history_x.append(x)
        #self.history_y.append(y)
        
        #self.history.append((x, y))
        self.x, self.y = x, y 
    
    def record_history(self): 
        self.history.append((self.x, self.y))


def move(direction, x, y):
    if direction == "R": 
        return x+1, y 
    if direction == "L": 
        return x-1, y 
    if direction == "D": 
        return x, y-1 
    if direction == "U": 
        return x, y+1 


#%%

knots = [Rope(0,0) for _ in range(10)]
head = knots[0]


for row in data: 
    direction, steps = row.split(" ")
    #print("_______________")
    #print("row: ", direction, steps)

    for _ in range(int(steps)): 
        head.move(direction)

        for idx, knot in enumerate(knots[1:]):
            last_knot = knots[idx]
            if not knot.is_attached(last_knot): 
                knot.follow(last_knot)
                knot.record_history()

        #print("head:", head.x, head.y)
        #print("tail:", tail.x, tail.y)


#%%

tail = knots[-1]
tail.history.append((0, 0))
len(set(tail.history))



#%%


