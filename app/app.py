from flask import Flask, request, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import arrow, datetime #human readable time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/redserver.db'

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

@app.route("/", methods=['GET', 'POST'])
def hello():
  if request.method == 'POST':
    app.logger.debug("!")
    android_id = request.form['android_id']
    time_sent = now()

    #Add to db
    newdata = User(android_id, time_sent)

    db.session.add(newdata)
    db.session.commit()

  else:
    app.logger.debug("x")

    #ask for a simple password here 

    #show all the users + count
    users = User.query.all()

    # rv = ""
    # for user in users:
    #   rv = rv + "android_id: " + str(user.android_id) + " | time_sent: " + str(user.time_sent) + "<br>"
    users_formatted = []
    for user in users:
      users_formatted.append({'android_id' : user.android_id, 'time_sent' : datetime.datetime.fromtimestamp(user.time_sent).strftime('%Y/%m/%d %H:%M:%S')})

    app.logger.debug(users_formatted)
    return render_template('index.html', users=users_formatted)

  return "Hello!"

@app.route('/d')
def d():
  d = User.query.all()
  for x in d:
    db.session.delete(x)
  db.session.commit()
 
  return "Deleted all users in sample db"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')