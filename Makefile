
n ?= test
NAMESPACE=$(n)

prepare:
	cp test-values.yaml.template test-values.yaml
	
deploy:
	helm upgrade --install -n ${NAMESPACE} pub-sub-demo charts/example-pubsub-communication --values test-values.yaml --create-namespace

destroy:
	helm uninstall -n ${NAMESPACE} pub-sub-demo

build:
	docker build . -t zifter/dummy-pubsub-worker:v0.1

push:
	docker push zifter/dummy-pubsub-worker:v0.1
