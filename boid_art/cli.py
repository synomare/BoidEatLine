import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--swarm", type=int, default=35)
    parser.add_argument("--mem", type=int, default=256, dest="mem_capacity")
    parser.add_argument("--headless", action="store_true")
    return parser
