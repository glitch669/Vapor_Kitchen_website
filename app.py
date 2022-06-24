from flask import Flask, render_template, request, url_for
import json
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate(#ADD YOUR REALTIME DATABASE CREDENTIALS)
firebase_admin.initialize_app(cred, {"databaseURL": #ADD YOUR DATABASE URL})
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
        fdb= db.reference().child('userdata').get()
        data = []
        slno=0
        for email in fdb.keys():
            slno+=1
            name = fdb[email]['name']
            gender = fdb[email]['gender']
            phone = fdb[email]['phone']
            order_details= fdb[email]['order-details']
            items = fdb[email]['cart-details']['items']
            prices = fdb[email]['cart-details']['prices']
            data.append([slno,name,gender,phone,order_details,items,prices])
        return render_template("shopkeeper.html",data=data)
    return render_template("payment_page.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
