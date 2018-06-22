.PHONY: build force test

shell:
	docker run -ti \
	-v ${PWD}:/opt/pixels \
	--device /dev/ttyUSB0 \
	--user=root \
	--privileged \
	--net=host \
	pixels /bin/bash

run:
	docker run -ti \
	-v ${PWD}:/opt/pixels \
	--device /dev/ttyUSB0 \
	--user=root \
	--privileged \
	--net=host \
	pixels /bin/bash -c "pypy ./flask_server_par.py"

build:
	docker build -t pixels ./

force:
	docker build -t pixels --no-cache ./

test:
	mamba --enable-coverage --format documentation
