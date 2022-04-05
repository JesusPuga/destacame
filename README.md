# destacame-backend

> Backend api to be used with REST FRAMEWORK, tested with frontend [Traveling](https://github.com/JesusPuga/destacame-front)
- CRUD with driver, passenger, travel, travel_plan, bus and journey

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
