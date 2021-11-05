# fcc-fastapi-demo

freeCodeCamp FastAPI [demo](https://youtu.be/0sOvCWFmrtA)

## Installation

Install requirements.

```bash
pip install -r requirements.txt
```

## Usage

### Run server locally

Create .env file with the variables as described in the [example](.env_example) file.

Run service:

```bash
uvicorn app.main:app --reload
```

## Enabled enpoints

CRUD

```bash
../posts
../posts/{id}
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
