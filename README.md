<p align="center"><img alt="Logo" height="225" width="225" src=".github/images/logo.jpg"></p>

# ✈️ UnoTrip bot

Manage your travels with ease

**Technical task:** [link](https://centraluniversity.notion.site/Backend-Travel-agent-3-0-f2d4cbabbaa94a338d3ad6293a9f0b4f)

**Link:** [@uno_trip_bot](https://t.me/uno_trip_bot)

## Database Diagram

![ER Diagram](/.github/schemes/DatabaseScheme.png)

## ⚙️ Technologies

### [.NET (C#)](https://dotnet.microsoft.com/en-us/)

.NET 

.NET is the free, open-source, cross-platform framework for building modern apps and powerful cloud services.

All backend side of project written completely in C#. Telegram bot just invokes it.

*Version: 8.0*

### [Python](https://python.org/)

Python is used successfully in thousands of real-world business applications around the world, including many large and mission critical systems.

It's used to write bot's logic and behavior.

*Version: 3.12*

### [aiogram](https://aiogram.dev/)

aiogram is a modern and fully asynchronous framework for Telegram Bot API using asyncio and aiohttp.

*Version: 3.4*

### [httpx](https://www.sqlalchemy.org/)

HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

*Version: 0.27.0*

### [PostgreSQL](https://www.postgresql.org/)

PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

In project used as the main database.

*Version: 16.2*

### [Redis](https://redis.io/)

The in-memory data store used by millions of developers as a cache, vector database, document database, streaming engine, and message broker.

In project redis used as storage for states.

*Version: 7.2*

## 🤝 Integrations

### [OpenStreetMap API](https://wiki.openstreetmap.org/wiki/API)

OpenStreetMap is built by a community of mappers that contribute and maintain data about roads, trails, cafés, railway stations, and much more, all over the world.

In the project, the interaction with OpenStreetMap API is implemented using geopy lib.

### [GraphHopper](https://www.graphhopper.com/)

Service for conveniently building routes between points on the map. The user can view the route of a trip through webview that appears when clicking on the inline button.

### [FourSquare API](https://foursquare.com/)

This API used to get nearby sights, restaurants and etc. for location.

### [Open Weather Map API](https://openweathermap.org/)

API to easily get current weather in specified location.

## 🖥️ Demonstration

![Demo](/.github/gifs/demo.mp4)

## 🛠️ Local development & testing

### Clone repository with git

```bash
git clone https://github.com/fpetrov/UnoTrip
```

### Navigate to the project directory

```bash
cd ./UnoTrip
```

### Create virtual enviroment & activate it

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Linux

```bash
python -m venv venv
source venv/bin/activate
```

### Install dev requirements

```bash
pip install -r requirements/dev.txt
```


### Run bot in development mode

#### Run backend service
```bash
cd UnoTrip.Backend
dotnet run UnoTrip.Api
```

#### Run OpenStreetMap service
```bash
cd UnoTrip.OpenStreetMap
python -m app
```

#### Run bot
```bash
python -m UnoTrip.Bot
```

## 🚀 Deploying

This app uses Docker Compose for production deployment.

**Structure**:

```bash
uno_trip /
    postgres (starts at 5432 port in your local network)
    redis (starts at 6379 port in your local network)
    api (starts at 8080 port in your local network)
    bot
```

**NOTE**: You have to manually start `UnoTrip.OpenStreetMap` service because it uses Selenium to render maps.

### Clone repository with git

```bash
git clone https://github.com/fpetrov/UnoTrip
```

### Navigate to the project directory

```bash
cd UnoTrip
```

### Pull actual docker images

```bash
docker compose pull
```

### Start containers (in detached mode)

```bash
docker compose up -d --build
```
