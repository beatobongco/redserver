from flask import Flask, request, Response, render_template, url_for
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import arrow, datetime #human readable time
import config

app = Flask(__name__)

app.config.from_object(config)

db = SQLAlchemy(app)

def now():
    return arrow.now().timestamp

class User(db.Model):
  # A user
  android_id = db.Column(db.String(255), primary_key=True)
  time_sent = db.Column(db.Integer)

  def __init__(self, android_id, time_sent):
    self.android_id = android_id
    self.time_sent = time_sent

  def __repr__(self):
    return '<User %r>' % self.android_id

#Basic auth
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['USERNAME'] and password == app.config['PASSWORD']

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=['GET', 'POST'])
@requires_auth
def index():
  #show all the users + count
  users = User.query.all()

  users_formatted = []
  for user in users:
    users_formatted.append({'android_id' : user.android_id, 'time_sent' : datetime.datetime.fromtimestamp(user.time_sent).strftime('%Y/%m/%d %H:%M:%S')})

  return render_template('index.html', users=users_formatted)

@app.route('/receive', methods=['POST'])
def receive(): 
  try:
    android_id = request.form['android_id']
    time_sent = now()

    #Add to db
    newdata = User(android_id, time_sent)

    db.session.add(newdata)
    db.session.commit()
  except IntegrityError:
    return "Already exists"
  return "Received"

@app.route('/d')
def d():
  d = User.query.all()
  for x in d:
    db.session.delete(x)
  db.session.commit()
 
  return "Deleted all users in sample db"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')