# Keydo

Thesis Topic : Continuous User Authentication based on Keystroke Dynamics

This is an implementation of the server that is going to manage the data of our Users Keystroke.

Docker Desktop is mandatory, clone repo and run the following: 

```
docker-compose -f local.yml build 

docker-compose -f local.yml up db
docker-compose -f local.yml up broker
docker-compose -f local.yml up kafka_consumer
docker-compose -f local.yml up app
```




