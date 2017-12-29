from ... import foo

def something():
    from .two import Two
    return Two()
