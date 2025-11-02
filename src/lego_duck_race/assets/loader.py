from pathlib import Path


def load_asset(name: str) -> str:
    path = Path(__file__).parent.resolve().joinpath(name)
    with open(path) as asset:
        sprite = asset.read()
        return sprite
