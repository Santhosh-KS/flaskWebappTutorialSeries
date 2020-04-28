"""App entry point."""
from flask_pytorch_web_app import create_app

app = create_app()

#TODO don't forget to remove debug option during deployment
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
