docker network create mongo-net
docker network create milvus-net

docker volume create raw-data

docker run --rm -v raw-data:/mnt ubuntu:latest sh -c "mkdir -p /mnt/gnews /mnt/newsapi /mnt/newsapiai mnt/processed"