default: release

APP="castai/rebalancer"
TAG_LATEST=$(APP):latest
TAG_VERSION=$(APP):v0.2

pull:
	docker pull $(TAG_LATEST)

build:
	@echo "==> Building rebalancer container"
	docker build --cache-from $(TAG_LATEST) --platform linux/amd64 -t $(TAG_LATEST) -t $(TAG_VERSION) .

publish:
	@echo "==> pushing to docker hub"
	docker push --all-tags $(APP)

release: pull
release: build
release: publish

deploy:
	kubectl apply -f deploy.yaml