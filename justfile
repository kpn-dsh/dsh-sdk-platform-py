TENANT := "training"
DOCKER_REPO_URL := "registry.cp.kpn-dsh.com/"+TENANT
VERSION := "0.1.0"
TAGNAME := "hello-world"
TENANTUSERID := "1054"
IMAGE := DOCKER_REPO_URL+"/"+TAGNAME+":"+VERSION

all:
    just build
    just push
    just show

login:
    docker login {{DOCKER_REPO_URL}}

build:
    docker build --platform linux/amd64 -t {{TAGNAME}} -f Dockerfile --build-arg UID={{TENANTUSERID}} .
    docker tag {{TAGNAME}} {{IMAGE}}


rebuild:
    docker build --platform linux/amd64 --no-cache -t {{TAGNAME}} -f Dockerfile --build-arg UID={{TENANTUSERID}} .
    docker tag {{TAGNAME}} {{IMAGE}}

push:
    docker push {{IMAGE}}

dive:
	dive {{IMAGE}}

show:
    @echo "#make file configuration"
    @echo "#URL          : {{DOCKER_REPO_URL}}"
    @echo "#TENANT       : {{TENANT}}"
    @echo "#tenantuserid : {{TENANTUSERID}}"
    @echo "#tagname      : {{TAGNAME}}"
    @echo "#version      : {{VERSION}}"
    @echo "#image        : {{IMAGE}}"
