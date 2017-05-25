"""Example"""

from implements import Interface, implements


class Flyable(Interface):
    def fly(self):
        pass


class Quackable(Interface):
    def quack(self):
        pass


class Animal:
    def __init__(self, name):
        self.name = name


@implements(Flyable)
class BaldEagle(Animal):
    def fly(self):
        pass


@implements(Flyable)
@implements(Quackable)
class MallardDuck(Animal):
    def fly(self):
        pass

    def quack(self):
        print("quack!")


if __name__ == '__main__':
    duck = MallardDuck("Mallory")
    eagle = BaldEagle("Murica")
