from dataclasses import dataclass


@dataclass # struct gibi kullanım için ve print edebiliyorsun
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
