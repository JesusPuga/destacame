# destacame-backend

> Backend api to be used with REST FRAMEWORK, tested with frontend [Traveling](https://github.com/JesusPuga/destacame-front)
- CRUD with driver, passenger, travel, travel_plan, bus and journey
- ERD.pdf in root path includes the entity relationship diagram

# Prerequisites

- docker 20.10.10
- docker-compose 1.29.2

# Build Setup

In the project directory, you can run:

```sh
cd traveling
docker-compose build
docker-compose up
```

Runs the app.\
Open [http://localhost:8000](http://localhost:8000) to view it in the browser.

The page will reload if you make edits.

# Features

## CRUD routes are served on /api/

Base ROUTES  [http://localhost:8000/api/](http://localhost:8000/api/) 

## Driver routes structure example

- Create POST  [http://localhost:8000/api/driver/](http://localhost:8000/api/driver/) 
- Update PATCH  [http://localhost:8000/api/driver/:id](http://localhost:8000/api/driver/:id) 
- List GET  [http://localhost:8000/api/driver/](http://localhost:8000/api/) 
- Delete (disable)  DELETE [http://localhost:8000/api/:id/](http://localhost:8000/api/:id/) 

# Assumptions

- The goal of the project is manage the travels in X company, that does not include customers, reports, complex users, etc
- The system allows to add differents travels
- Every travel has buses in differents schedules, it means that the bus can be used to go to differents places but not in the same schedule
- Every bus has just one driver and some passengers in their own seat, that does not mean that the bus can only travel with specific passengers but with differents schedules 
- The limit of seats in every bus is by default 10
- Every seat has a number from 1-10, if there is any passenger with a seat reserved it cannot be set again
- The system can save the data of divers to specific bus, add passenger to travel with specific schedule
