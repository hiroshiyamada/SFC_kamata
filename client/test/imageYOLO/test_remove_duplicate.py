from unittest import TestCase
from nose.tools import ok_, eq_
#import ..imageYOLO import updateNotes
from ... import imageYOLO

def test1():
    detected = [
        (b'dog', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125)),
        (b'bicycle', 0.991621732711792, (344.5289306640625, 286.759765625, 486.18890380859375, 321.3658447265625)), 
        (b'truck', 0.9165929555892944, (580.9117431640625, 125.05439758300781, 208.13427734375, 87.27819061279297))
        ]
    ref = [
        (b'dog', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125))
        ]
    detected = imageYOLO.remove_duplicate(detected)
    eq_(ref, detected)

def test2():
    detected = [
        (b"test", 0.92, (1,250,4,5)),
        (b"test", 0.88, (2,388,3,4)),
        (b"test", 0.93, (4,345,3,4)),
        (b"test", 0.98, (5,150,4,5))
        ]
    ref = [
        (b"test", 0.88, (2,388,3,4)),
        (b"test", 0.93, (4,345,3,4))
        ]
    detected = imageYOLO.remove_duplicate(detected)
    eq_(ref, detected)