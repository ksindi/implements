"""Example"""

from implements import implements, Interface


class Vehicle(Interface):
    wheels = None

    def start_engine(self):
        pass

    def drive(self):
        pass

    @staticmethod
    def make_car_sound():
        pass


@implements(Vehicle)
class Car:
    wheels = 4

    def start_engine(self):
        pass

    def drive(self):
        pass

    @staticmethod
    def make_car_sound():
        print('Vrooom!')


if __name__ == '__main__':
    car = Car()
