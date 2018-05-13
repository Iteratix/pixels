.PHONY: build force test

shell:
	docker run -ti \
	-v ${PWD}:/opt/pixels \
	--device /dev/ttyUSB0 \
	--user=root \
	--privileged \
	--net=host \
	pixels /bin/bash

build:
	docker build -t pixels ./

force:
	docker build -t pixels --no-cache ./

test:
	mamba --enable-coverage --format documentation
