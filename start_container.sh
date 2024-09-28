DIR_TO_COPY="src"

docker build -t c-dev-env .
docker run -it --rm -v $(pwd)/$DIR_TO_COPY:/app/$DIR_TO_COPY c-dev-env