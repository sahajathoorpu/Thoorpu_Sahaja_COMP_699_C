from flask import Flask
from website import create_app
from website.models import init_db

app = create_app()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
