SHELL=/bin/bash -o pipefail
BUILD_PRINT = \e[1;34mSTEP:
END_BUILD_PRINT = \e[0m

CURRENT_UID := $(shell id -u)
export CURRENT_UID
# These are constants used for make targets so we can start prod and staging services on the same machine
ENV_FILE := .env

# include .env files if they exist
-include .env

#-----------------------------------------------------------------------------
# Dev commands
#-----------------------------------------------------------------------------
install: install-dev
	@ echo -e "$(BUILD_PRINT)Installing the requirements$(END_BUILD_PRINT)"
	@ pip install --upgrade pip
	@ pip install -r requirements.txt

install-dev:
	@ echo -e "$(BUILD_PRINT)Installing the dev requirements$(END_BUILD_PRINT)"
	@ pip install --upgrade pip
	@ pip install -r requirements.dev.txt

test: test-unit

test-unit:
	@ echo -e "$(BUILD_PRINT)Unit Testing ...$(END_BUILD_PRINT)"
	@ tox -e unit

test-features:
	@ echo -e "$(BUILD_PRINT)Gherkin Features Testing ...$(END_BUILD_PRINT)"
	@ tox -e features

test-e2e:
	@ echo -e "$(BUILD_PRINT)End to End Testing ...$(END_BUILD_PRINT)"
	@ tox -e e2e

test-all-parallel:
	@ echo -e "$(BUILD_PRINT)Complete Testing ...$(END_BUILD_PRINT)"
	@ tox -p

test-all:
	@ echo -e "$(BUILD_PRINT)Complete Testing ...$(END_BUILD_PRINT)"
	@ tox

build-externals:
	@ echo "$(BUILD_PRINT)Creating the necessary volumes, networks and folders and setting the special rights"
	@ docker network create proxy-net || true

#-----------------------------------------------------------------------------
# SERVER SERVICES
#-----------------------------------------------------------------------------
start-traefik: build-externals
	@ echo "$(BUILD_PRINT)Starting the Traefik services"
	@ docker-compose -p common --file ./infra/traefik/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-traefik:
	@ echo "$(BUILD_PRINT)Stopping the Traefik services"
	@ docker-compose -p common --file ./infra/traefik/docker-compose.yml --env-file ${ENV_FILE} down

start-portainer: build-externals
	@ echo "$(BUILD_PRINT)Starting the Portainer services"
	@ docker-compose -p common --file ./infra/portainer/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-portainer:
	@ echo "$(BUILD_PRINT)Stopping the Portainer services"
	@ docker-compose -p common --file ./infra/portainer/docker-compose.yml --env-file ${ENV_FILE} down

start-server-services: | start-traefik start-portainer
stop-server-services: | stop-traefik stop-portainer

#-----------------------------------------------------------------------------
# PROJECT SERVICES
#-----------------------------------------------------------------------------
create-env-airflow:
	@ echo "$(BUILD_PRINT) Create Airflow env"
	@ mkdir -p infra/airflow/logs infra/airflow/plugins
	@ cd infra/airflow/ && ln -s -f ../../dags && ln -s -f ../../ted_sws
	@ echo -e "AIRFLOW_UID=$(CURRENT_UID)" >infra/airflow/.env


build-airflow: guard-ENVIRONMENT create-env-airflow build-externals
	@ echo "$(BUILD_PRINT) Build Airflow services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/airflow/docker-compose.yaml --env-file ${ENV_FILE} build --no-cache --force-rm
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/airflow/docker-compose.yaml --env-file ${ENV_FILE} up -d --force-recreate
start-airflow: build-externals
	@ echo "$(BUILD_PRINT)Starting Airflow servies"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/airflow/docker-compose.yaml --env-file ${ENV_FILE} up -d
stop-airflow:
	@ echo "$(BUILD_PRINT)Stoping Airflow services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/airflow/docker-compose.yaml --env-file ${ENV_FILE} down

#	------------------------
start-allegro-graph: build-externals
	@ echo "$(BUILD_PRINT)Starting Allegro-Graph servies"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/allegro-graph/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-allegro-graph:
	@ echo "$(BUILD_PRINT)Stoping Allegro-Graph services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/allegro-graph/docker-compose.yml --env-file ${ENV_FILE} down

#	------------------------
build-elasticsearch: build-externals
	@ echo "$(BUILD_PRINT) Build Elasticsearch services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/elasticsearch/docker-compose.yml --env-file ${ENV_FILE} build --no-cache --force-rm
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/elasticsearch/docker-compose.yml --env-file ${ENV_FILE} up -d --force-recreate

start-elasticsearch: build-externals
	@ echo "$(BUILD_PRINT)Starting the Elasticsearch services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/elasticsearch/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-elasticsearch:
	@ echo "$(BUILD_PRINT)Stopping the Elasticsearch services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/elasticsearch/docker-compose.yml --env-file ${ENV_FILE} down


start-minio: build-externals
	@ echo "$(BUILD_PRINT)Starting the Minio services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/minio/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-minio:
	@ echo "$(BUILD_PRINT)Stopping the Minio services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/minio/docker-compose.yml --env-file ${ENV_FILE} down


start-mongo: build-externals
	@ echo "$(BUILD_PRINT)Starting the Minio services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/mongo/docker-compose.yml --env-file ${ENV_FILE} up -d

stop-mongo:
	@ echo "$(BUILD_PRINT)Stopping the Minio services"
	@ docker-compose -p ${ENVIRONMENT} --file ./infra/mongo/docker-compose.yml --env-file ${ENV_FILE} down


start-project-services: | start-airflow start-elasticsearch start-allegro-graph start-minio start-mongo
stop-project-services: | stop-airflow stop-elasticsearch stop-allegro-graph stop-minio stop-mongo

#-----------------------------------------------------------------------------
# VAULT SERVICES
#-----------------------------------------------------------------------------
# Testing whether an env variable is set or not
guard-%:
	@ if [ "${${*}}" = "" ]; then \
        echo "$(BUILD_PRINT)Environment variable $* not set"; \
        exit 1; \
	fi

# Testing that vault is installed
vault-installed: #; @which vault1 > /dev/null
	@ if ! hash vault 2>/dev/null; then \
        echo "$(BUILD_PRINT)Vault is not installed, refer to https://www.vaultproject.io/downloads"; \
        exit 1; \
	fi
# Get secrets in dotenv format
staging-dotenv-file: guard-VAULT_ADDR guard-VAULT_TOKEN vault-installed
	@ echo "$(BUILD_PRINT)Creating .env.staging file"
	@ echo VAULT_ADDR=${VAULT_ADDR} > .env
	@ echo VAULT_TOKEN=${VAULT_TOKEN} >> .env
	@ echo DOMAIN=ted-data.eu >> .env
	@ echo ENVIRONMENT=staging >> .env
	@ echo SUBDOMAIN=staging. >> .env
	@ vault kv get -format="json" ted-staging/airflow | jq -r ".data.data | keys[] as \$$k | \"\(\$$k)=\(.[\$$k])\"" >> .env
	@ vault kv get -format="json" ted-staging/mongo-db | jq -r ".data.data | keys[] as \$$k | \"\(\$$k)=\(.[\$$k])\"" >> .env

dev-dotenv-file: guard-VAULT_ADDR guard-VAULT_TOKEN vault-installed
	@ echo "$(BUILD_PRINT)Create .env file"
	@ echo VAULT_ADDR=${VAULT_ADDR} > .env
	@ echo VAULT_TOKEN=${VAULT_TOKEN} >> .env
	@ echo DOMAIN=localhost >> .env
	@ echo ENVIRONMENT=staging >> .env
	@ echo SUBDOMAIN= >> .env
	@ vault kv get -format="json" ted-staging/airflow | jq -r ".data.data | keys[] as \$$k | \"\(\$$k)=\(.[\$$k])\"" >> .env
	@ vault kv get -format="json" ted-staging/mongo-db | jq -r ".data.data | keys[] as \$$k | \"\(\$$k)=\(.[\$$k])\"" >> .env


prod-dotenv-file: guard-VAULT_ADDR guard-VAULT_TOKEN vault-installed
	@ echo "$(BUILD_PRINT)Create .env file"
	@ echo VAULT_ADDR=${VAULT_ADDR} > .env
	@ echo VAULT_TOKEN=${VAULT_TOKEN} >> .env
	@ echo DOMAIN=ted-data.eu >> .env
	@ echo ENVIRONMENT=prod >> .env
	@ echo SUBDOMAIN= >> .env
	@ vault kv get -format="json" ted-prod/airflow | jq -r ".data.data | keys[] as \$$k | \"\(\$$k)=\(.[\$$k])\"" >> .env
	@ vault kv get -format="json" ted-prod/mongo-db | jq -r ".data.data | keys[] as \$$k | \"\(\$$k)=\(.[\$$k])\"" >> .env


#clean-mongo-db:
#	@ export PYTHONPATH=$(PWD) && python ./tests/clean_mongo_db.py


#build-open-semantic-search:
#	@ echo "Build open-semantic-search"
#	@ cd infra && rm -rf open-semantic-search
#	@ cd infra && git clone --recurse-submodules --remote-submodules https://github.com/opensemanticsearch/open-semantic-search.git
#	@ cd infra/open-semantic-search/ && ./build-deb
#	@ echo "Patch open-semantic-search configs"
#	@ cat infra/docker-compose-configs/open-semantic-search-compose-patch.yml > infra/open-semantic-search/docker-compose.yml
#	@ cd infra/open-semantic-search/ && docker-compose rm -fsv
#	@ cd infra/open-semantic-search/ && docker-compose build
#
#start-open-semantic-search:
#	@ echo "Start open-semantic-search"
#	@ cd infra/open-semantic-search/ && docker-compose up -d
#
#
#stop-open-semantic-search:
#	@ echo "Stop open-semantic-search"
#	@ cd infra/open-semantic-search/ && docker-compose down
#
#
#start-silk-service:
#	@ echo "Start silk service"
#	@ cd infra/silk/ && docker-compose up -d
#
#stop-silk-service:
#	@ echo "Stop silk service"
#	@ cd infra/silk/ && docker-compose down