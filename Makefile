.PHONY: test test-build test-clean


## ☄️ Run project in Docker
run:
	docker compose up -d
## 🧪 Run tests inside Docker
test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

## 🛠️ Build the test image without running
test-build:
	docker compose -f docker-compose.test.yml build

## 🧹 Clean up test containers and network
test-clean:
	docker compose -f docker-compose.test.yml down --volumes --remove-orphans
