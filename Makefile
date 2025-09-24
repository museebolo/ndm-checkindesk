prefix  ?= canelrom1
name    ?= abcm-checkindesk
tag     ?= $(shell date +%Y%m%d.%H%M%S)

all: build

build: src/Dockerfile
	docker build -t $(prefix)/$(name):$(tag) src
	docker tag $(prefix)/$(name):$(tag) $(prefix)/$(name):latest 

run:
	docker run -d -p 80:8080 --name $(name) $(prefix)/$(name):latest

rm:
	docker stop $(name)
	docker rm $(name)

up:
	docker-compose up -d

down:
	docker-compose down


# vim: ft=make
