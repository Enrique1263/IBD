# Big Data Infrastructure

This repository serves as a comprehensive news collector, leveraging JSON-returning APIs. The codebase is designed for scalable deployment, both horizontally (utilizing multiple API keys) and vertically (utilizing multiple APIs).

The primary objective of this project is to establish a robust news aggregation system capable of populating a database (MongoDB, currently in progress), with potential future applications. News articles are categorized by user-defined topics, enabling efficient API request management and topic-based data segregation.

## Gathering Structure

To enhance accessibility, this project is supported by containerization. The structural components include:

- **dockerfiles**: Contains various dockerfiles utilized by the containers in case Docker Hub is down.
- **collector-compose.yml (Collector)**: Creates containers for news collection, with one container per API image.
- **mongo-compose.yml (MongoDB)**: Orchestrates containers for the MongoDB database. A replicaset of 3 mongodb instances. Also includes a jupyter notebook container to run commands in the replica-set if needed (as well as testing).
- **requirements.txt**: Lists dependencies required for code execution.
- **src**: Contains various .py files utilized by the images.
- **.env (MUST BE CREATED BY THE USER FOLLOWING .env.example)**: Safely stores API keys to prevent exposure in the code. Can be modified by the user to select topics as well as timeframe for the extraction. Language determines the language of the articles and newsapi-ai tokes per api indicates teh number of call allows per apikey of that API. 
- **notebooks**: Jupyter notebook files are saved here.

While it's feasible to run this system on a single machine, utilizing a cluster of machines is recommended to accommodate scalability. For this project docker swarm was contemplated, but difficulty in node connections forced us to reduce the scale to one node.

## Data

Leveraging the RESTful nature of news APIs, data is acquired in JSON format, enabling seamless integration with MongoDB. Data scalability is achieved through multiple APIs and API keys, facilitating concurrent requests and higher request rates. Data availability is contingent upon API uptime.

With MongoDB, data management is delegated to the database, necessitating sufficient replicas to match the pace of API data retrieval. Data retrieval can be facilitated using MongoDB interfaces such as Compass or Python library pymongo.  

## Big Data Dimensions

Considering the 5 V's of Big Data:

- **Volume**: MongoDB's storage capacity enables handling extensive data volumes, with scalability options (Can be adapted to great volumes of data).
- **Velocity**: Multi-API data collection allows for high-speed data acquisition, subject to API daily limits (more keys, more data).
- **Variety**: While sacrificing variety, data uniformity is maintained as APIs adhere to a consistent structure, streamlining data processing.
- **Veracity**: The credibility of data sourced from news articles ensures high data reliability.
- **Value**: The collected data is versatile, serving as a valuable resource for diverse applications beyond database population.

## Commands

Useful Docker deployment commands:
#### Initiate communication network for the whole infrastructure
- docker network create mongo-net
#### Initiate mongo replica-set
- docker compose -f mongo-compose.yml
#### Initiate news collectors (mongo replica-set must be healthy)
- docker compose -f mongo-compose.yml
#### Extract raw json data from the replica-set
- docker run -f --env-file ./.env --network mongo-net --name raw-collector vramososuna/mongo-raw-extractor

----
From Docker Hub https://hub.docker.com/search?q=vramososuna these images are used:

- vramososuna/mongo-starter
- vramososuna/mongo-raw-extractor
- vramososuna/newsapiai
- vramososuna/gnews
- vramososuna/newsapi
- vramososuna/jupyter-mongo

## Functionability

The objective is to design a container-based digital infrastructure to support a system that works with Big Data. In this case, three MongoDB instances are deployed and configured to run on a replica set, providing redundancy and high availability. Storing data in persistent volumes ensures data durability beyond the lifecycle of the containers. These services are essential for storing and managing data collected from news sources. Then, the newsapi-collector, gnews-collector, newsapiai-collector are designed to connect to different APIs (NewsAPI, GNews, and NewsAPI.ai) to collect news. Each service has its own container, allowing for separation of responsibilities and scalability. Using .env files to configure these services facilitates customization and security by not hardcoding API keys in the code or container. The starter service plays an important role in the initial setup of the MongoDB database that is used to store the collected news data, where high availability and fault tolerance for the database is ensured. After verifying the existence of the database and creating the necessary collections, the script closes the connection to MongoDB. This is a good practice to free resources and avoid possible connection leaks. The service of jupyter provides a web-accessible Jupyter Notebook environment, allowing interactive analysis of the collected data. The inclusion of a Jupyter environment underlines the importance of data analysis in this project, facilitating the exploration and visualization of data stored in MongoDB.

The news gathering services are adapted to the peculiarities of each API, such as the handling of rate limits or pagination of results, allowing then to process the raw data received and store the results in MongoDB. So, MongoDB acts as the centralized data store for this project (**Recolection**). The MongoDB replica set structure provides a robust solution for managing the data, ensuring its availability and consistency (**Storage**). Also, the Jupyter service provides a platform for data analysis, allowing users to explore and visualize the data collected directly from the MongoDB database. This is crucial for extracting insights and value from the collected data (**Data Analysis**). Finally, the use of an external Docker network (mongo-net) shared between all services facilitates efficient communication between containers, especially important to allow news gathering services to interact with MongoDB instances. The external network ensures that containers can find and communicate with each other no matter which node in the cluster they are running on.

**Availability and Reliability**

- MongoDB Replica Set: Configuring the MongoDB server in a replica set is critical to ensure high availability and fault tolerance. In the event that one node fails, the other nodes can continue to operate, ensuring that the database remains accessible. In addition, replicas allow reading from secondary nodes, thus distributing the load of read operations.

- Automatic Container Restart: The always-on restart policy in the container services configuration ensures that, if a container fails for any reason, Docker will attempt to restart it automatically, minimizing downtime.

**Scalability**

- Docker Swarm and Overlay Networks: Although the proposed project does not explicitly use of Docker Swarm, the mention of an external network (mongo-net) suggests future readiness for a distributed environment, such as Docker Swarm. Docker Swarm facilitates horizontal scalability by allowing services to scale across multiple nodes in the cluster. Overlay networking supports communication between distributed containers on different hosts, maintaining network consistency.

- Separate Services for Data Collection: The microservices architecture, with separate container services for different news sources, allows each data collection service to scale independently based on the specific load or demand of each API source.

**Efficiency and Load Management**

- MongoDB Load Balancing and Optimized Queries: The MongoDB replica set not only serves for availability, but also enables effective load balancing, especially with read queries distributed across secondary nodes. Query optimization and proper indexing of collections are essential to maintain data access efficiency.

- Control of Connections and Requests: The code implemented in the collection services carefully manages connections to external APIs and to MongoDB, using best practices such as connection reuse and proper handling of rate limits. This ensures efficient resource utilization and avoids potential outages due to API or database overload.

**Design Decisions and Quality Principles**

The design decisions made in the proposed infrastructure reflect a commitment to quality principles for virtual infrastructures:

- Decoupling and Modularity: Separation of functionality into distinct containers improves maintainability and facilitates the upgradeability and scalability of each component individually.

- Automation and Self-Healing: The use of restart policies and database auto-initialization design promote a self-healing infrastructure that minimizes manual intervention and increases resiliency.

- Resource Optimization: The architecture enables efficient resource management, using the capabilities of Docker and MongoDB to adapt to varying workloads and optimize the use of the underlying infrastructure.
