from threading import Lock

from injector import Injector, singleton

from app.configuration import Configuration, create_configuration


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Container(metaclass=SingletonMeta):
    __injector: Injector

    def __init__(self):
        self.__injector = Injector([Container.__configure])

    def injector(self) -> Injector:
        return self.__injector

    @staticmethod
    def __configure(binder) -> None:
        binder.bind(Configuration, to=create_configuration(), scope=singleton)
