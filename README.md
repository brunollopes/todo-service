# TODO Service


## What is this demo about ?

#### Web API backend service to manage Boards and Tasks:

- CRUD operations for Boards and Tasks
- Retrieving Users from external API service (Centralized User Service) using the API from https://randomuser.me/api
- Webhook endpoint to receive events when an user is removed from the user external API
- Storage using MongoDB
- Unit/Integration tests
- Dockerfile to build docker image
- Docker compose file to run both containers (Todos and Mongo) within same network


## How to run it
==============================================

clone the repo and on the root directory run: docker-compose up

## How to access and consume the API

Accessing the OpenAPI: http://localhost:8000/docs

## Tech stack
- Python3 3.11.1
- Docker 20.10.21
- Docker-compose 2.13.0

## Notes
To add new tasks with a user that can later be found when getting a board, please select the UUID from the list returned from randomuser using: https://randomuser.me/api/?results=10&seed=123
