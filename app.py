from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb .db'
db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__= 'url'
    id = db.Column(db.Integer, primary_key=True)
    longurl = db.Column(db.String(700), nullable=False)
    shorturl = db.Column(db.String(100), nullable=False)
    uniq = db.Column(db.String(100), nullable=True)

    def __init__(self, id , longurl,shorturl,uniq):
        self.id = id
        self.longurl= longurl
        self.shorturl=shorturl
        self.uniq = uniq
# db.drop_all()
@app.route('/', methods=['POST','GET'])
def index():
    if request.method =='POST':
        lurl = request.form.get('lurl')
        dbfile = open('db_id_file.txt','r')
        lastid = str(dbfile.read())
        lastid = int(lastid)
        newid = lastid +1
        dbfile = open('db_id_file.txt', 'w')
        dbfile.write(str(newid))
        item = Url(newid,lurl,'http://test.com/123', 'itisuniq')   
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    else:    
        return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/what_new')
def feature():
    return render_template('feature.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3333', debug=True)

