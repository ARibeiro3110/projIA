all:
	python3 bimaru.py < instances/instance01.txt > out.txt
	diff out.txt instances/instance01.out
	python3 bimaru.py < instances/instance02.txt > out.txt
	diff out.txt instances/instance02.out
	python3 bimaru.py < instances/instance03.txt > out.txt
	diff out.txt instances/instance03.out
	python3 bimaru.py < instances/instance04.txt > out.txt
	diff out.txt instances/instance04.out
	python3 bimaru.py < instances/instance05.txt > out.txt
	diff out.txt instances/instance05.out
	python3 bimaru.py < instances/instance06.txt > out.txt
	diff out.txt instances/instance06.out
	python3 bimaru.py < instances/instance07.txt > out.txt
	diff out.txt instances/instance07.out
	python3 bimaru.py < instances/instance08.txt > out.txt
	diff out.txt instances/instance08.out
	python3 bimaru.py < instances/instance09.txt > out.txt
	diff out.txt instances/instance09.out
	python3 bimaru.py < instances/instance10.txt > out.txt
	diff out.txt instances/instance10.out
	rm out.txt

	python3 Tester/tester.py

c:
	rm -rfv Tester/Resultados
