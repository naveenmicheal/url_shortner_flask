from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64, datetime, binascii, string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb .db'
db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__= 'url'
    id = db.Column(db.Integer, primary_key=True)
    longurl = db.Column(db.String(700), nullable=False)
    shorturl = db.Column(db.String(100), nullable=False)
    uniq = db.Column(db.String(100), nullable=True, primary_key = True)

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
        
        # --------For uniq Key generation -----------#
        raw_str = string.ascii_lowercase
        raw_num = string.digits
               
        str_key1 = random.choice(raw_str)
        str_key2= random.choice(raw_str)
        str_key3 = random.choice(raw_str)
        n_key1 = random.choice(raw_num)
        n_key2 = random.choice(raw_num)
        n_key3 = random.choice(raw_num)
        now = datetime.datetime.utcnow()
        r_tuniq = random.randint(0, 100)
        tuniq = ( r_tuniq + now.minute) 
        uniqkey = str_key1 + str_key2 +str(tuniq) + str_key3 + str(n_key1) + str(n_key3) + str(n_key2) 

        # -----------Uniq ID Generation------------------#
        now= datetime.datetime.utcnow()
        month = str(now.month)
        day = str(now.day)
        min = str(now.minute)
        sec = str(now.microsecond)
        r = str(random.randint(0,100))
        id_key = month + day + min + sec + r 

        try:
            item = Url(id_key,lurl,'http://localhost:3333/'+uniqkey, uniqkey)
            s_url = 'http://localhost:3333/'+uniqkey
            print(s_url)   
            db.session.add(item)
            db.session.commit()
        except:
            return redirect(url_for('dberrror'))    
        return render_template('home.html', data = s_url)
    else:    
        return render_template('home.html')

@app.route('/error')
def dberrror():
    return render_template('error.html')
 


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

