FROM python:3.8-slim-buster
EXPOSE 8000

WORKDIR /usr/src/api/id_manager
COPY . /usr/src/api/id_manager

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r infra/api/requirements.txt

ENTRYPOINT uvicorn --host 0.0.0.0 --port ${ID_MANAGER_API_PORT} ted_sws.notice_transformer.entrypoints.api.digest_service.main:app
