from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from config import DevelopmentConfig # DevelopmentConfig ProductionConfig, TestingConfig


# load environment variables from the .env file
load_dotenv(find_dotenv())


app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig)


# If you want to use different configurations based on an environment variable:
# app.config.from_object(os.environ.get('FLASK_CONFIG', 'config.DevelopmentConfig'))

# Initialize your extensions like SQLAlchemy, Bcrypt, etc., here
# Example:
# db.init_app(app)
# bcrypt.init_app(app)


debug = DebugToolbarExtension(app)











if __name__ == "__main__":
    app.run()
