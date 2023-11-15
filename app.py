from config.config import app
from routes.routes import *

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
