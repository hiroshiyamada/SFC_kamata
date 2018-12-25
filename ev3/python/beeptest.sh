rm test.txt
for i in {1..5}; do echo "-l 200 -f 349 -l 200 -f 392" >> test.txt ; done&
cat test.txt |xargs -n4 beep
