from config.databases import CONNECTIONS


def create_configuration() -> "Configuration":
    return Configuration(database=Database())


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):
    __database: "Database"

    def __init__(self, database: "Database"):
        self.__database = database

    @property
    def database(self) -> "Database":
        return self.__database


class Database:
    __uri: str
    __database: str

    def __init__(self):
        self.__uri = CONNECTIONS["default"]["DB_URI"]
        self.__database = CONNECTIONS["default"]["DB_NAME"]

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def database(self) -> str:
        return self.__database
