# -*- coding: utf-8 -*-
import requests

def convertNotes(notes):
    test = {}
    test["key0"] = len(notes)
    for i in range(len(notes)):
        key = "key" + str(i+1)
        test[key] = notes[i]
        #temp.append(test2[i])
    return test
    
note_dict={
        'C4' : '261', #.63
        'D4' : '293', #.66
        'E4' : '329', #.63
        'F4' : '349', #.23
        'G4' : '392', #.00
        'A4' : '440', #.00
        'A#4/Bb4': '466', #.16
        'C5' : '523', #.25
        'D5' : '587', #.33
        'Z'  : '17000'
}

def convertNotes2(notes):
    test = ""
    for n in notes:
        test += " -l 500 -f "
#        test += " -l 800 -f "
        print(note_dict.get(n[0], '16000'))
        test += note_dict.get(n[0], '16000')
    print(test)
    return test

#    test["key0"] = len(notes)
#    for i in range(len(notes)):
#        key = "key" + str(i+1)
#        test[key] = notes[i]
#        #temp.append(test2[i])
#    return test
    

def postMusic(notes):
    #入力データ
#    test = {}
    #temp = []
    #test2 = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h'),('D5', 'h'),('C5', 'e3'),
    #('B4', 'e3'),('A4', 'e3'),('G5', 'h'),('D5', 'q'),('C5', 'e3'),('B4', 'e3'),
    #('A4', 'e3'),('G5', 'h'),('D5', 'q'),('C5', 'e3'),('B4', 'e3'),('C5', 'e3'),
    #('A4', 'h.')]
    #test2 = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h'),('D5', 'h'),('C5', 'e3')]

#    test["key0"] = len(notes)
#    for i in range(len(notes)):
#        key = "key" + str(i+1)
#        test[key] = notes[i]
#        #temp.append(test2[i])
    test = convertNotes2(notes)
#    test = "-l 200 -f 349 -l 200 -f 392"
    #マインドストームのアドレスに送信
    s = requests.session()
#    r = s.post("http://49.135.3.100:8080/python/receive.py", data = test)
    r = s.post("http://49.135.3.100:8080/python/test.py", data = test)
    #送信結果を表示
    print(r.text)

if __name__ == "__main__":
  #test_notes = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h'),('D5', 'h'),('C5', 'e3')]
  test_notes = [('C4', 'e3'),('C4', 'e3'),('A4', 'e3'),('G4', 'h'),('F4', 'h'),('C4', 'e3'),('Z', 'e3'),('Z', 'e3'),('Z', 'e3'),('C4', 'e3'),('C4', 'e3'),('A4', 'e3'),('G4', 'h'),('F4', 'h'),('D4', 'e3'),('Z', 'e3'),('Z', 'e3'),('Z', 'e3')]
  postMusic(test_notes)
