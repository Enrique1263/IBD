docker build -f ./dockerfiles/starter-mongo -t vramososuna/mongo-starter .
docker build -f ./dockerfiles/worker -t vramososuna/worker .
docker build -f ./dockerfiles/Newsapiai -t vramososuna/newsapiai .
docker build -f ./dockerfiles/Gnewsapi -t vramososuna/gnews .
docker build -f ./dockerfiles/Newsapi -t vramososuna/newsapi .
docker build -f ./dockerfiles/jupyter-tester -t vramososuna/jupyter-tester .

