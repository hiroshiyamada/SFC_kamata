from unittest import TestCase
from nose.tools import ok_, eq_
#import ..imageYOLO import updateNotes
from ... import imageYOLO


def test_updateNotes1():
    out = [1, 2, 3, 4]
    detected = [3, 4, 5]
    ref = [1, 2, 3, 4, 5]
    imageYOLO.updateNotes(detected, out)
    eq_(ref, out)

def test_updateNotes2():
    out = [1, 2, 3, 4, 3, 4, 5]
    detected =  [3, 4, 5, 6]
    ref = [1, 2, 3, 4, 3, 4, 5, 6]
    imageYOLO.updateNotes(detected, out)
    eq_(ref, out)

def test_updateNotes3():
    out = ["fa", "so", "la", "fa", "so", "la", "do"]
    detected = ["so", "la", "do", "re", "mi"]
    ref = ["fa", "so", "la", "fa", "so", "la", "do", "re", "mi"]
    imageYOLO.updateNotes(detected, out)
    eq_(ref, out)

def test_updateNotes4():
    out = [1, 2, 3, 4, 3, 4, 5]
    detected =  [3, 4]
    ref = [1, 2, 3, 4, 3, 4, 5]
    imageYOLO.updateNotes(detected, out)
    eq_(ref, out)

def test_updateNotes5():
    out = [3, 4, 3, 4]
    detected =  [3, 4, 5, 6]
    ref = [3, 4, 3, 4, 5, 6]
    imageYOLO.updateNotes(detected, out)
    eq_(ref, out)

def test_updateNotes6():
    out = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h.')]
    detected =  [('G4', 'h.'),('D5', 'h.'),('C5', 'e3')]
    ref = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h.'),('D5', 'h.'),('C5', 'e3')]
    imageYOLO.updateNotes(detected, out)
    eq_(ref, out)

