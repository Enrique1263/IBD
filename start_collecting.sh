#!/bin/bash

# Run 1: newapi with technology
docker run --network mongo-net -e SOURCE=newapi -e KEYWORD=technology -e APIKEY=c14142ee09054d3bbbb550eb004d90ed recollector-app

# Run 2: gnews with health
docker run --network mongo-net -e SOURCE=gnews -e KEYWORD=health -e APIKEY=dacbe7a5ac6f3bd66f5a217372e43ca8 recollector-app

# Run 3: newapi with finance
docker run --network mongo-net -e SOURCE=newapi -e KEYWORD=finance -e APIKEY=0fe2a84717664cad80f32b720258cedd recollector-app

# Run 4: gnews with sports
docker run --network mongo-net -e SOURCE=gnews -e KEYWORD=sports -e APIKEY=eb6d8b1c0cf1c2daf6d6710d120352b5 recollector-app

# Run 5: newapi with education
docker run --network mongo-net -e SOURCE=newapi -e KEYWORD=education -e APIKEY=3e6d17be36d94789b262e4e444fddc5b recollector-app

# Run 6: gnews with environment
docker run --network mongo-net -e SOURCE=gnews -e KEYWORD=environment -e APIKEY=76357433dca2f5a22351ae5ecb681ce6 recollector-app
