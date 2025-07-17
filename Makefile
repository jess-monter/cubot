.PHONY: install run test test-build test-clean


# 📜 Default target: show all commands with descriptions
all:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## ⚙️ Install Docker and Docker Compose
	@echo "🔍 Checking Docker installation..."
	@if command -v docker >/dev/null 2>&1; then \
		echo "✅ Docker is already installed."; \
	else \
		echo "🔧 Installing Docker..."; \
		curl -fsSL https://get.docker.com -o get-docker.sh; \
		sh get-docker.sh; \
		rm get-docker.sh; \
	fi

	@echo "🔍 Checking Docker Compose plugin..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "✅ Docker Compose plugin is already installed."; \
	else \
		echo "🧩 Installing Docker Compose plugin..."; \
		sudo mkdir -p /usr/local/lib/docker/cli-plugins; \
		curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
			-o /usr/local/lib/docker/cli-plugins/docker-compose; \
		sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose; \
	fi

	@echo "🔄 Ensuring current user is in the docker group..."
	@if groups $$USER | grep -q docker; then \
		echo "✅ User already in docker group."; \
	else \
		echo "➕ Adding user to docker group..."; \
		sudo usermod -aG docker $$USER; \
		echo "⚠️  Please log out and back in or run 'newgrp docker' to apply changes."; \
	fi

run: ## ☄️ Run project in Docker
	docker compose up -d

down: ## 🚦 Stop services
	docker compose down --volumes --remove-orphans

clean: ## 🧹 Clean up Docker resources
	docker compose down --volumes --remove-orphans
	@echo "🧹 Cleaning up dangling images..."
	docker image prune -f
	@echo "🧹 Cleaning up unused volumes..."
	docker volume prune -f

test: ## 🧪 Run tests inside Docker
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit


test-build: ## 🛠️ Build the test image without running
	docker compose -f docker-compose.test.yml build


test-clean: ## 🧹 Clean up test containers
	docker compose -f docker-compose.test.yml down --volumes --remove-orphans
