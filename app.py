from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
# db = SQLAlchemy(app)

# tables
# class Url(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     longurl = db.Column(db.String(700), nullable=False)
#     shorturl = db.Column(db.String(100), nullable=False)
#     uniq = db.Column(db.String(100), nullable=True)

@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3333', debug=True)

