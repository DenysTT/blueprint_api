release ?= develop
image = den4iks99/revo_api:$(release)

build:
	docker build -t $(image) .

push:
	docker push $(image)

provision:
	ansible-playbook --diff -i ansible/inventory --private-key=$(KEY) --vault-password-file=$(VAULT_FILE) ansible/playbook.yml