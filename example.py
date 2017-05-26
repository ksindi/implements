"""Example"""
from enum import Enum

from implements import Interface, implements


class Direction(Enum):
    N = 'North'
    W = 'West'
    S = 'South'
    E = 'East'


class Flyable(Interface):
    def fly(self):
        pass

    def migrate(self) -> Direction:
        pass


class Quackable(Interface):
    echoes = None

    def quack(self):
        pass


class Animal:
    def __init__(self, name):
        self.name = name


@implements(Flyable)
class BaldEagle(Animal):
    def fly(self):
        pass

    def migrate(self) -> Direction:
        return Direction.W


@implements(Flyable)
@implements(Quackable)
class MallardDuck(Animal):
    echoes = True

    def fly(self):
        pass

    def quack(self):
        print("quack!")

    def migrate(self) -> Direction:
        return Direction.S
