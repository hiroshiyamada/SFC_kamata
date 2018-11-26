from unittest import TestCase
from nose.tools import ok_, eq_
from ... import imageYOLO

def test_convertNotes1():
    dic_4cat = {"fa":("F4", "q"), "so":("G4", "q"), "la":("A4", "q"), "do":("C4", "q")}
    detection_results = [(b'fa', 0.9, (1, 2, 3, 4)), (b'so', 0.9, (1, 2, 3, 4)), (b'la', 0.9, (1, 2, 3, 4))]
    ref = [("F4", "q"), ("G4", "q"), ("A4", "q")]
    out = imageYOLO.convertNotes(detection_results,dic_4cat)
    eq_(ref, out)
