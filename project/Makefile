
all:
	make clean
	$(MAKE) -C src all
	echo '#!/usr/bin/env python'  | cat - irgen.zip > irgen
	chmod +x irgen
	mkdir bin
	mv ./irgen ./bin
	rm ./irgen.zip
	./bin/irgen ./test/test3.php > out.txt
clean:
	rm -rf ./bin