#!flask/bin/python
from app import app

app.logging.info("Starting app")
app.run(debug=True, threaded=True)
app.logging.info("running app")