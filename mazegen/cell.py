from dataclasses import dataclass


@dataclass
class Cell:
    """A single maze cell with a wall on each of its four sides."""

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
