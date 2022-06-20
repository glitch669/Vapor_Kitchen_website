

from flask import Flask, render_template, request, url_for
import json
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "vapor-kitchen-aws6",
  "private_key_id": "31f6b10295989cb0e9c72be15172df665339895b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDmu0uwWbAOrfFM\nbf/6kdLsVwVgUdW5u0WP4jfHjjImxGu44vuzPJzjUwuC1H6CR/PjxxW+e1OsvNi8\n1ld/v7IKZtifYbqxp5165Lg1ht4JQR16s/l8cgEuRGIPdfcA2jMwvEuLhinI6yZf\nRkga4YEmIFfVs1yPPIaB8laeTQ9MN8KxLVHo0nD4tR2zTeBYAv+64ePISbkzGgYZ\n5mvl4CQ1Rdq3fnzJ9zASrFwhibtv/tW/AJ6/DSSGnZk6AgX410KqWO5L0qcX0ekA\n8pXsZMOGiUc5ibw97UHziGtYyv0Lub+vRJvYpnt1PWav5MfoKplcs3cp6CxZSjIY\nAEkczaorAgMBAAECggEAI45YBZ8XRcvW/tjctPe6h000Y47ONBxV20HDKBoTmcHJ\nz+i6sk5JkbEpzvQsDVZFO/lhXRnoNRsM/gdnMyU5Vz0DbjGYnD6g7V/zEIdDZC2y\npfFiJaPz5qCxySwmmkJbLSF3NX3BUVhbcMcwiWPti7s5jecMASQUnlCCufZUwIEe\n8KourY4sXAn0J0H/0VIxK8YcLC+MefKxZymBUopPGbFnKhIQ3lIWSgUJ7Nx7EE+O\nLPsuX1BI6vylLFFlktDbMaz7U8pmHVs4oHVWCC0sb4Gi0iP8Huycobm95LNdilH7\nGy+jW9TBcO8JMBNarrgSOdNeOHJOL94Z4cMTX5EMYQKBgQD/xIh0B5XXOw4YF40y\nMFEdj7j5SXypN1BeGwXEO7mU7LR49JBl5ffgXGE4Wa8vT7Mca0UaL6rZVegHUa49\nsLgfxqpSLCEuea6bfbpklHgMK3JrtG3Xv6rataiFCr5nKTc+zzdjltUaBH4E7GqG\nkrRNDBHlPhfeV3f9Yf+nAaIlqQKBgQDm8PEQLWUb8NS6chOKqvs+4FVPffI9a5go\nwFQ2rZcmDfeMFuLLSt6yuC+yj6v55csYRJLb2MaVDndpfrZScOM2ftNW3qxwDmWH\nlcIouHQyActPwW8ldoSfwnhWJZhmbI0ltdp1dgyYeIadn/FJv2GxACtYRGJHBgWI\nr0CiTz3NswKBgA8ja8wqUsUderUUV8gbsgFk61bd8aH2YyxevxWhT1ewNvJdz1oo\npWZDMYHrVQIg3oIVG070eVFJ02TzgbOnDQ7cbGJWuFQO4bXUWD7xxrU5sRkM4d9+\nObeePu4495IVj26JR0b+u3hBwc+6yodSkZdp2nlOFo2TcceukDorT5SZAoGAUS2u\nvy4F1Z2BWYyR+/OAX6jBtDCkfxycHu8Eazf34qOUOcUtsaI+x/ngolbIcA5rprss\nGGWJ4Il2RjoJYs9VvykzptydJsKYw+FLn76+8XkZ+44WQMf5dKMKY9XRTWeo8fGL\nujBl2w662xuG2JKSh4J0uhFHromaVmKsSKGsKusCgYEA8BsjFLegyjqLjGRCkaKG\n1yOjbDOG1+553sU0VlOaNWe4mh8QnBrII9Y/7VQZKevJ7/w1z4C6Fl5Kkmi7zv5f\nJHnZPr7DpaanB55X0+IjWmj/OT0OwlR9eIRnU5UjgJM6t6CoIYVKSbS7DgGGK19b\nilMfexsGPr+yzKKQpHxHLS8=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-9akyx@vapor-kitchen-aws6.iam.gserviceaccount.com",
  "client_id": "111078690815716852922",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9akyx%40vapor-kitchen-aws6.iam.gserviceaccount.com"
})

firebase_admin.initialize_app(cred, {"databaseURL":"https://vapor-kitchen-aws6-default-rtdb.firebaseio.com/"})

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('signup.html')


@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        srn = request.form['SRN']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        
       
        fdb = db.reference('userdata')
        fdb.update({
                email:{
        'name': name,
        'srn' : srn,
        'gender': gender,
        'phone': phone,
        'password': password
            }
        }
        )
        msg= "Registration Complete. Please Login to your account !"
    
        return render_template('login.html', msg=msg)
    return render_template('signup.html')

@app.route('/login')
def login():    
    return render_template('login.html')

@app.route('/signup')
def index2():    
    return render_template('signup.html')

@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        global email 
        email = request.form['email']
        password = request.form['password']
        
        fdb = db.reference('userdata')

        """if(email.lower() or email.upper() == 'd@gmail'):
            return render_template("shopkeeper.html")"""

        if((email.lower() or email.upper()) in fdb.get()):
            fdb = db.reference('userdata/{}'.format(email))
            name = fdb.get()['name']
            if password == fdb.get()["password"]:
            
                return render_template("home.html",name = name)
        return render_template("login.html")

@app.route('/confirmcart',methods = ['post'])
def confirmcart():
    if request.method=='POST':
        cart_json=request.get_json()
        cart = json.loads(cart_json) 
        cart = [json.loads(i) for i in cart]

        print("here", cart)
        items=[]
        prices=[]
        for i in range(len(cart)):
            items.append(cart[i]['productname'])
            prices.append(cart[i]['price'])
        
        fdb= db.reference('userdata/{}'.format(email))
        fdb.update({
            "cart-details":
            {
            'items':items,
            'prices':prices,
                }
            }
        )
        return "Done"
        

@app.route('/order',methods = ['post','get'])
def order():
    if request.method=='POST' and request.form['Order Now']=='order':
        place = request.form['place']
        blockname = request.form['blockname']
        roomnumber = request.form['roomnumber']
        
        fdb= db.reference('userdata/{}'.format(email))
        fdb.update({
            "order-details":
            {
            'place': place,
            'block name' : blockname,
            'room number': roomnumber,
           
                }
            }
        )
        return render_template("payment_page.html")
    


@app.route('/get_orders', methods = ['post'])
def get_orders():
    if request.method=='POST' and request.form['Confirm Payment']=='pay':
        fdb= db.reference('userdata')
        data = fdb.get()
        return render_template("shopkeeper.html",data = data)
    return render_template("payment_page.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

