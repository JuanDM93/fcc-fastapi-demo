# fcc-fastapi-demo

freeCodeCamp FastAPI [demo](https://youtu.be/0sOvCWFmrtA)

## Usage

### Run server locally

Install requirements.

```bash
pip install -r requirements.txt
```

Configure local database and create .env file with the variables as described in the [example](.env_example) file.

Start  db with head revision [alembic](https://alembic.sqlalchemy.org/en/latest/):

```bash
alembic upgrade head
```

Run service:

```bash
uvicorn app.main:app
```

### Run from web server

Gunicorn [service file](gunicorn.service)), don't forget to setup db from alembic and .env file.

### Dockerize

Once cloned, run [docker-compose](https://docs.docker.com/compose/overview/) to build and run the service

"""bash
docker-compose -f docker-compose-{env}.yml up
"""

env:

- dev: local .env file required

- prod: [DockerHub](https://hub.docker.com/r/juandm93/ffc-fastapi)

## Enabled enpoints

CRUD

```bash
../login

../users
../users/{id}

../posts
../posts/{id}

../vote
```

API docs

```bash
../docs
../redoc
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
