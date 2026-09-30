from server import create_server
from database_init import DataBase

if __name__ == "__main__":
    db = DataBase()
    server = create_server(db)
    server.serve_forever()

    db.connection.close()