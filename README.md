# BoidEatLine

This project provides an asynchronous boid simulation with an observer model.
Install dependencies and run the pygame front end as follows:

```bash
python -m pip install -r requirements.txt
python -m boid_art.ui.pygame_front
```

You can tweak the population size and memory capacity:

```bash
python -m boid_art.ui.pygame_front --swarm 150 --mem 512
```

## Running without a terminal

The project now includes a `pyproject.toml` with a GUI entry point. After
installing the package you can create a standalone executable using
[PyInstaller](https://pyinstaller.org/):

```bash
python -m pip install . pyinstaller
pyinstaller --onefile --windowed -n BoidEatLine -m boid_art
```

This produces a `BoidEatLine` executable in the `dist` directory that can be
launched directly without opening a console window.
