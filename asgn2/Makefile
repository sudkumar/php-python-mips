all:
	$(MAKE) -C src all
	echo '#!/usr/bin/env python'  | cat - codegen.zip > codegen
	chmod +x codegen
	mkdir bin
	mv ./codegen ./bin
	rm ./codegen.zip
clean:
	rm -rf ./bin
