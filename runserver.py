from src import create_app, db
from src.config.config import Config

app = create_app(Config)

if __name__ == '__main__':
    #db.create_all(app = create_app())
    app.run()