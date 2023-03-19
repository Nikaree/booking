from flask import Flask


app = Flask(__name__)
config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 150,
    "SECRET_KEY": '12345'
}
app.config.from_mapping(config)



import controllers.index