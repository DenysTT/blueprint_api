release ?= develop
image = den4iks99/blueprint_api:$(release)

build:
	docker build -t $(image) .

push:
	docker push $(image)

provision:
	ansible-playbook --diff -i ansible/inventory --private-key=${KEY} ansible/playbook.yml
