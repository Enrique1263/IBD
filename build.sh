docker build -f ./dockerfiles/mongo-starter -t vramososuna/mongo-starter .
docker build -f ./dockerfiles/milvus-starter -t vramososuna/milvus-starter .
docker build -f ./dockerfiles/worker -t vramososuna/worker .
docker build -f ./dockerfiles/Newsapiai -t vramososuna/newsapiai .
docker build -f ./dockerfiles/Gnewsapi -t vramososuna/gnews .
docker build -f ./dockerfiles/Newsapi -t vramososuna/newsapi .
docker build -f ./dockerfiles/jupyter-tester -t vramososuna/jupyter-tester .
docker build -f ./dockerfiles/user-milvus -t vramososuna/user-milvus .

