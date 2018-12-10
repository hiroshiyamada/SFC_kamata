from unittest import TestCase
from nose.tools import ok_, eq_
#import ..imageYOLO import updateNotes
from ... import imageYOLO

def test1():
    detected = [
        (b'truck', 0.9165929555892944, (580.9117431640625, 125.05439758300781, 208.13427734375, 87.27819061279297)),
        (b'bicycle', 0.991621732711792, (344.5289306640625, 286.759765625, 486.18890380859375, 321.3658447265625)),
        (b'dog', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125))
        ]
    ref = [
        (b'dog', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125)),
        (b'bicycle', 0.991621732711792, (344.5289306640625, 286.759765625, 486.18890380859375, 321.3658447265625)), 
        (b'truck', 0.9165929555892944, (580.9117431640625, 125.05439758300781, 208.13427734375, 87.27819061279297))
        ]
    detected = imageYOLO.sortSheet(detected)
    eq_(ref, detected)

def test2():
    detected = [
        ("test", 0.33, (4,2,3,4)),
        ("test", 0.455, (2,2,3,4)),
        ("test", 0.3422, (5,3,4,5)),
        ("test", 0.112, (1,3,4,5))
        ]
    ref = [
        ("test", 0.112, (1,3,4,5)),
        ("test", 0.455, (2,2,3,4)),
        ("test", 0.33, (4,2,3,4)),
        ("test", 0.3422, (5,3,4,5))
        ]
    detected = imageYOLO.sortSheet(detected)
    eq_(ref, detected)
