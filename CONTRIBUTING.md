# Contributing

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Install dependencies and run tests with:

```bash
poetry install
poetry run pytest -q
```

For headless environments set:
```bash
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
```
Then run the front end using `--headless`.
