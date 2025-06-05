# BoidEatLine

This project provides an asynchronous boid simulation with an observer model.
Press `TAB` during the simulation to toggle the meta view overlay showing
centrality graphs.
Install dependencies and run the pygame front end as follows:

```bash
python -m pip install -r requirements.txt
python -m boid_art.ui.pygame_front
```

You can tweak the population size and memory capacity:

```bash
python -m boid_art.ui.pygame_front --swarm 150 --mem 512

# headless mode (no window, useful for CI)
python -m boid_art.ui.pygame_front --headless
```
