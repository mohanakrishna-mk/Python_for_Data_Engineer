class DatabaseContext:

    def __enter__(self):
        print("Database connection opened")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Database connection closed")