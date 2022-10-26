from manager.database import DatabaseHandler

class Manager:
    def __init__(self) -> None:
        self._db_handler = DatabaseHandler()

    