from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64, datetime, binascii, string, random, requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb .db'
db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__= 'url'
    id = db.Column(db.Integer, primary_key=True)
    longurl = db.Column(db.String(700), nullable=False)
    shorturl = db.Column(db.String(100), nullable=False)
    uniq = db.Column(db.String(100), nullable=False,unique=True, primary_key = True)
    count =db.Column(db.Integer, nullable=False)

    def __init__(self, id , longurl,shorturl,uniq, count):
        self.id = id
        self.longurl= longurl
        self.shorturl=shorturl
        self.uniq = uniq
        self.count = count

class Data(db.Model):
    __tablename__= 'data'
    random_id = db.Column(db.String(100), primary_key =True)
    longurl = db.Column(db.String(700), nullable=False)
    shorturl = db.Column(db.String(100), nullable=False)
    uniq = db.Column(db.String(100), nullable=False)
    # useragent = db.Column(db.String(500), nullable=True)
    browser = db.Column(db.String(50), nullable=True)
    device = db.Column(db.String(50), nullable=True)
    # location = db.Column(db.String(30), nullable=True)
    isp = db.Column(db.String(30), nullable=True)

    def __init__(self,random_id,longurl,shorturl,uniq,browser,device,isp):
        self.random_id = random_id
        self.longurl=longurl
        self.shorturl = shorturl
        self.uniq = uniq
        # self.useragent = useragent
        self.browser=browser
        self.device = device   
        # self.location = location  
        self.isp = isp    
# db.drop_all()
# db.create_all()

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
            item = Url(id_key,lurl,'http://localhost:3333/'+uniqkey, uniqkey, 0)
            s_url = 'http://localhost:3333/'+uniqkey   
            db.session.add(item)
            db.session.commit()
            return render_template('home.html', data = s_url)
        except:
            return redirect(url_for('dberrror'))    
         
    else:    
        return render_template('home.html')

@app.route('/error')
def dberrror():
    return render_template('error.html')
 
@app.route('/<s_url>')
def surl(s_url):
    # query to database
    # try: 
    print(s_url)
    data = Url.query.filter_by(uniq = s_url).first()
    # print('Before Count ' + str(data.count))
    data.count = data.count+1
     # print('After ' + str(data.count)) 
    db.session.commit()
    # For the DATA_URL table
    raw_c = string.ascii_lowercase
    raw_n = string.digits
    random_id = ''
    global random_id
    # random_id = random.randint(0,9999999) / random.randint(1,5) * random.choice(raw_n)
    random_id = str(random_id)
    random_id =  random.choice(raw_c)+random.choice(raw_c)+random.choice(raw_c) +random.choice(raw_c) + random.choice(raw_c)+ random.choice(raw_c) + random.choice(raw_c) + random.choice(raw_c) 

    longurl = data.longurl
    shorturl =  data.shorturl
    uniq = data.uniq
    browser = request.user_agent.browser
    #locaton updated after deployed
    device = request.user_agent.platform
    # location = 'Mars Near on Earth'
    #isp updated after deployed
    isp = 'Space X on Mars ISP'
    # Add URL_DATA on Data table

    item = Data(random_id,longurl,shorturl,uniq,browser,device,isp)
    db.session.add(item)
    db.session.commit()
    return redirect(longurl)
       
        # addr = request.environ['REMOTE_ADDR']
        # location = ''
        # ispname = ''
        # url = 'http://ip-api.com/json/8.8.8.8'
        # isp_raw = requests.get(url)
        # isp_raw = isp_raw.json()
        # # print(isp_raw.text)
        # status = isp_raw['status']
        # print (status)
        # if isp_raw['status'] == 'fail':
        #         location = 'Not Available'
        #         ispname = 'Not Available'
        # else:
        #         location = isp_raw['country']
        #         ispname = isp_raw['isp']

    # except:
    #     return 'No record Found'
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

