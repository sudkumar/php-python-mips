all:
	$(MAKE) -C src all
	echo '#!/usr/bin/env python'  | cat - irgen.zip > irgen
	chmod +x irgen
	mkdir bin
	mv ./irgen ./bin
	rm ./irgen.zip
clean:
	rm -rf ./bin
