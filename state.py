# SO now we are creating graph 
# and the first thing you create is a state



import os

# 1) typed DICT

from typing import TypedDict

class State(TypedDict):
    topic: str
    summary: str
    score: int

# 2) Pydantic Approch
# It is good as data validation nd type checking

from pydantic import BaseModel,field_validator

class State(BaseModel):
    topic: str
    summary: str = ""
    score: int

    @field_validator
    def score_positive(cls,v):
        if v<0:
            raise ValueError("Score must be positive")
        
# 3) Python Dataclasses
# It is standard class but it is use very rarely

from dataclasses import dataclass,field

@dataclass

class State:
    topic: str=""
    summary: str=""
    messages: list=field(default_factory=list)
    score: int

# 4) Using Langgraph message state

from langgraph.graph import MessagesState

class State(MessagesState):
    topic: str=""
    summary: str=""
    score: int

