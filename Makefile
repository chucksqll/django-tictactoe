PROJECT_NAME=tictactoe_app
docker_build:
	docker build -t ${PROJECT_NAME} -f Dockerfile .
docker_run:
	docker run -p 8000:8000 -ti --rm ${PROJECT_NAME}