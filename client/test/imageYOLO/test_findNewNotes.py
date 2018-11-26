from unittest import TestCase
from nose.tools import ok_, eq_
#import ..imageYOLO import findNewNotes
from ... import imageYOLO


def test_findNewNotes1():
    past = [1, 2, 3, 4]
    detected = [3, 4, 5]
    ref = [5]
    out = imageYOLO.findNewNotes(detected, past)
    eq_(ref, out)

def test_findNewNotes2():
    past = [1, 2, 3, 4, 3, 4, 5]
    detected =  [3, 4, 5, 6]
    ref = [6]
    out = imageYOLO.findNewNotes(detected, past)
    eq_(ref, out)

def test_findNewNotes3():
    past = ["fa", "so", "la", "fa", "so", "la", "do"]
    detected = ["so", "la", "do", "re", "mi"]
    ref = ["re", "mi"]
    out = imageYOLO.findNewNotes(detected, past)
    eq_(ref, out)

def test_findNewNotes4():
    past = [1, 2, 3, 4, 3, 4, 5]
    detected =  [3, 4]
    ref = []
    out = imageYOLO.findNewNotes(detected, past)
    eq_(ref, out)

def test_findNewNotes5():
    past = [3, 4, 3, 4]
    detected =  [3, 4, 5, 6]
    ref = [5, 6]
    out = imageYOLO.findNewNotes(detected, past)
    eq_(ref, out)

def test_findNewNotes6():
    past = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h.')]
    detected =  [('G4', 'h.'),('D5', 'h.'),('C5', 'e3')]
    ref = [('D5', 'h.'),('C5', 'e3')]
    out = imageYOLO.findNewNotes(detected, past)
    eq_(ref, out)

