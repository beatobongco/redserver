from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import arrow #human readable time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/redserver.db'

db = SQLAlchemy(app)

class User(db.Model):
  # A user

  def now():
    return arrow.now().timestamp

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
    time_sent = request.form['time_sent']

    #Add to db
    newdata = User(android_id, time_sent)

    db.session.add(newdata)
    db.session.commit()

  else:
    app.logger.debug("x")
    #show all the users
    users = User.query.all()

    rv = ""
    for user in users:
      rv = rv + "android_id: " + str(user.android_id) + " | time_sent: " + str(user.time_sent) + "<br>"

    return rv# render_template('userlist', users=users)

  return "Hello!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')