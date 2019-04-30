release ?= develop
image = den4iks99/revo_api:$(release)

build:
	docker build -t $(image) .

push:
	docker push $(image)
