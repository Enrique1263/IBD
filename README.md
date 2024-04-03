# Big Data Infrastructure

This repository serves as a comprehensive news collector, leveraging JSON-returning APIs. The codebase is designed for scalable deployment, both horizontally (utilizing multiple API keys) and vertically (utilizing multiple APIs).

The primary objective of this project is to establish a robust news aggregation system capable of populating a database (MongoDB, currently in progress), with potential future applications. News articles are categorized by user-defined topics, enabling efficient API request management and topic-based data segregation.

## Gathering Structure

To enhance accessibility, this project is supported by containerization. The structural components include:

- **Dockerfile**: Used to build images executing Python code for each API, necessitating one image per API.
- **docker-compose.yml (Collector)**: Creates containers for news collection, with one container per API image.
- **docker-compose.yml (MongoDB)**: Orchestrates containers for the MongoDB database.
- **requirements.txt**: Lists dependencies required for code execution.
- **src**: Contains various .py files utilized by the images.
- **.env**: Safely stores API keys to prevent exposure in the code.

While it's feasible to run this system on a single machine, utilizing a cluster of machines is recommended to accommodate scalability. For this project, Docker's macvlan approach facilitates scalability.

## Data

Leveraging the RESTful nature of news APIs, data is acquired in JSON format, enabling seamless integration with MongoDB. Data scalability is achieved through multiple APIs and API keys, facilitating concurrent requests and higher request rates. Data availability is contingent upon API uptime.

With MongoDB, data management is delegated to the database, necessitating sufficient replicas to match the pace of API data retrieval. Data retrieval can be facilitated using MongoDB interfaces such as Compass or Python library pymongo. The way 

## Big Data Dimensions

Considering the 5 V's of Big Data:

- **Volume**: MongoDB's storage capacity enables handling extensive data volumes, with scalability options.
- **Velocity**: Multi-API data collection allows for high-speed data acquisition, subject to API daily limits (more keys, more data).
- **Variety**: While sacrificing variety, data uniformity is maintained as APIs adhere to a consistent structure, streamlining data processing.
- **Veracity**: The credibility of data sourced from news articles ensures high data reliability.
- **Value**: The collected data is versatile, serving as a valuable resource for diverse applications beyond database population.

## Commands

Useful Docker deployment commands:

- docker network create mongo-net
- docker build -t recollector-app .
###### gnews or newsapi, keyword any, FROM (start date), TO (end date), apikey
- docker run --network mongo-net -e SOURCE=gnews -e KEYWORD=technology -e FROM=2023-01-01 -e TO=2023-01-31 -e 
  APIKEY=your_api_key_here recollector-app
  
mongo connection string:
- mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0

----
From Docker Hub https://hub.docker.com/search?q=vramososuna use:

- docker pull vramososuna/mongo-starter
- docker pull vramososuna/mongo-raw-extractor
- docker pull vramososuna/newsapiai
- docker pull vramososuna/gnews
- docker pull vramososuna/newsapi

