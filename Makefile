TENANT=training
VERSION=0.1.0
tagname=test
tenantuserid=2053

DOCKER_REPO_URL=registry.cp.kpn-dsh.com/$(TENANT)
image=$(DOCKER_REPO_URL)/$(tagname):$(VERSION)

project:
	git init
	git add .
	poetry init --dependency=loguru --dependency=icecream
	echo "[tool.pyright]" >> pyproject.toml
	echo 'reportMatchNotExhaustive = "error"' >> pyproject.toml
	poetry lock --no-update
	# poetry install --no-root
	direnv allow

build:
	docker build --platform linux/amd64 -t $(tagname) -f Dockerfile --build-arg tenantuserid=$(tenantuserid) .
	docker tag  $(tagname) $(image)
all:
	make build
	make push
	make show
push:
	docker push $(image)
run:
	docker run --platform linux/amd64 -u $(tenantuserid):$(tenantuserid) -it --entrypoint "/bin/sh" $(image)

