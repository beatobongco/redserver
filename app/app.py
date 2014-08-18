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

  def __init__(self, google_id, stripe_id):
    self.android_id = android_id
    self.time_sent = time_sent

  def __repr__(self):
    return '<User %r>' % self.android_id

@app.route("/", methods=['GET', 'POST'])
def hello():
  if request.method == 'POST':
    android_id = request.args.get('android_id')
    time_sent = request.args.get('time_sent')

    #Add to db
    newdata = User(android_id, time_sent)

    db.session.add(newdata)
    db.session.commit()

  else:
    #show all the users
    users = User.query.all()

    rv = ""
    for user in users:
      rv = rv + "android_id: " + user.android_id + " | time_sent: " + user.time_sent + "<br>"

    return rv# render_template('userlist', users=users)

  return ""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')