from flask import *

# create app
app=Flask(__name__)
app.secret_key='jjbhugggggggggery'
# defibne connection
import pymysql
import mysql.connector
connection=pymysql.connect(host="localhost",user='root',password='',database='mayar_projectdb') 
# home page
@app.route('/')
def main():
    return render_template('index.html')

# create save vendor route
@app.route('/save_vendor', methods=['POST','GET'])
def save_vendor():
    # check if user has posted any data
    if request.method=='POST':
        # TODO
        # get data from the form
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        location=request.form['location'] 
        desc=request.form['desc']
        # get the image
         #check if image has been uploaded
        if 'image' not in request.files:
            return render_template('signup.html',message='image not uploaded')
   
        image=request.files['image']  
        # store the image inside static folder 
        image.save ('static/images/'+image.filename)
        img_name=image.filename 
        #input validation
        if not name or not email or not password or not phone or not location:
            return render_template('signup.html.html',message='You must fill all the fields')
        
        # create cursor
        cursor=connection.cursor()
        sql='insert into vendors(vendor_name,vendor_email,vendor_password,vendor_contact,vendor_location,profile_image,vendor_desc) values(%s,%s,%s,%s,%s,%s,%s)'
        try:
             #execute
            cursor.execute(sql,(name,email,password,phone,location,img_name,desc))
            connection.commit()
            cursor.close()
            return render_template("signup.html",message="Vendor saved successfully")
        except:
            return render_template('signup.html',message='Failed:Vendor not saved')
        
       
    else:
        return render_template("signup.html")
    # pass
@app.route("/signin",methods=['POST','GET'])
def sign_in():
    # check if the user has posted any records
    if 'key' in session:
        return redirect("/signin")
    else:  
    # check if the user has posted any records
        if request.method=='POST':
            #get data from the form
            username=request.form['username']
            password=request.form['password']
            # create a cursor function
            cursor=connection.cursor()
            sql='select * from vendors where vendor_name=%s and vendor_password=%s'
            # execute
            # values=(username,password)
            # cursor.execute(sql,(values)) 
            cursor.execute(sql,(username,password))
            #   check if theuser exists
            if cursor.rowcount=='0':
                return render_template('signup.html',message='user does not exist')
            else:
                session['key']=username
                #fetch the records of the vendors
                data=cursor.fetchone()
                # other sessions
                
                session['id']=data[0]
                session['email']=data[2]
                session['desc']=data[5]
                session['location']=data[6]
                session['image']=data[7]
                print(data)
                return render_template('vendor.html',vendor=data) 
            

        else:
            return render_template('signup.html')  

@app.route('/signin',methods=['POST','GET'])  
def signin():
    
        if request.method=='POST':
            #get data from the form
            username=request.form['username']
            password=request.form['password']
            # create a cursor function
            cursor=connection.cursor()
            sql='select * from vendors where vendor_name=%s and vendor_password=%s'
            # execute
            # values=(username,password)
            # cursor.execute(sql,(values)) 
            cursor.execute(sql,(username,password))
            #   check if theuser exists
            if cursor.rowcount=='0':
                return render_template('signup.html',message='user does not exist')
            else:
                session['key']=username
                #fetch the records of the vendors
                data=cursor.fetchone()
                # other sessions
                session['id']=data[0]
                session['email']=data[2]
                session['desc']=data[5]
                session['location']=data[6]
                session['image']=data[7]
                # print(session['email'])
                # print('success')
                return render_template('vendor.html',vendor=data)
        # else:
        #     return render_template('signup.html')  
#logout route vendor
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')

#logout route user
@app.route('/logout/user')
def logout_user():
    session.clear()
    return redirect('/login')    

# add product route
@app.route('/add_product',methods=['POST','GET'])
def Add_product():
    if 'key' not in session:
        return redirect("/signin")
    else:    
        if request.method=='POST':
            # TODO
            # get data from form
            name=request.form['product_name']
            vendor_id=request.form['vendor_id']
            category=request.form['product_category']
            brand=request.form['product_brand']
            cost=request.form['product_cost']
            discount=request.form['product_discount']
            desc=request.form['product_desc']

            # input validation
            if not name or not vendor_id or not category or not brand or not cost or not discount or not desc:
                return "Please provide all the products details"
                # get the image
            image=request.files['product_image']
            image.save('static/images/'+image.filename)
            image_url=image.filename
            # create cursor function
            cursor=connection.cursor()
            sql='insert into products (vendor_id,product_name,product_desc,product_cost,product_discount,product_category,product_brand,image_url) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            # execute sql query
            cursor.execute (sql,(vendor_id,name,category,brand,cost,discount,desc,image_url))
            connection.commit()
            return 'Product saved \n <a href="/signin">Go back</a'
            
            






        
        else: 
            return render_template('add_product.html')
                    
            
    # getproducts
@app.route('/getproducts',methods=['GET'])
def GetProducts():
        # create the cursor
        # electronics
        cursor_electronics=connection.cursor()
        # toiletries

        cursor_toiletries=connection.cursor()
        
        sql_electronics='select * from products where product_category="Electronics"'
        sql_toiletries='select * from products where product_category="toiletries"'
        # execute the sql query

        cursor_electronics.execute(sql_electronics)
        cursor_toiletries.execute(sql_toiletries)
        # fetch all the products
        
        
        electronics=cursor_electronics.fetchall()
        toiletries=cursor_toiletries.fetchall()
       
        # check if there are products to display
        if cursor_electronics.rowcount==0:
            return render_template('getproducts.html',message='No products to display')
            
        else:
            print(toiletries)
            # products=jsonify(products) convert products into json format
            # return products
            return render_template("getproducts.html" ,data=electronics,toiletries=toiletries) 
              


           
# Fetch products by vendors
@app.route("/vendor_products/<vendor_id>",methods=['GET'])
def Vendor_products(vendor_id):
    if 'key' not in session:
        return redirect("/signin")
    else:    
        sql='select * from products where  vendor_id=%s'
        # execute the sql query 
        cursor=connection.cursor()
        cursor.execute(sql,vendor_id)


        Vendor_products=cursor.fetchall()
        #check if there are products to display
        if cursor.rowcount==0:
            return render_template('vendor_products.html',error='No products available')
        else:
            return render_template("vendor_products.html",data=Vendor_products)   

# delete product  
@app.route("/delete/<product_id>",methods=['POST','GET','DELETE'])
def Delete_product(product_id): 
    if 'key' not in session:
        return redirect('/signin')
    else:
        sql='delete from products where product_id=%s'
        cursor=connection.cursor()
        #execute 
        cursor.execute(sql,product_id)
        connection.commit()
        return "Product Deleted"    
               

# sign in for the user
@app.route("/login",methods=['POST','GET'])
def Login():
    if request.method=='POST':
        #TODO
        # get the posted data 
        data=request.form['username']
        password=request.form['password']
        # create cursor
        cursor=connection.cursor() 
        # sql
        sql='select * from users where (username=%s or email=%s or phone=%s) and password=%s'
        # execute the sql query
        values=(data,data,data,password)
        cursor.execute(sql,values)
        # check if user exists
        if cursor.rowcount==0:
            return render_template('signin.html',message='wrong login credentials')
        else:
            # fetch
            user=cursor.fetchone()
            username=user[0]
            session['user']=username

            return redirect('/getproducts') 
              

    
    else:
        return render_template('signin.html')   

#single item
@app.route('/single_item/<product_id>',methods=['POST','GET'])
def Single_item(product_id):
    sql='select * from products where product_id=%s'
    # cursor
    cursor=connection.cursor()
    cursor.execute(sql,product_id)  
    # fetch the product
    product=cursor.fetchone()
    print(product)
    category=product[6]
    sql_similar='select * from products where product_category=%s'
    cursor_similar=connection.cursor()
    cursor_similar.execute(sql_similar,category)
    similar_product=cursor_similar.fetchall() 
    print(similar_product)
    return render_template('single_item.html',product=product,similar=similar_product)

#register route
@app.route('/register',methods=['POST','GET'])
def Register():
    return render_template('register.html')

# mpesa intergration route
import requests 
import base64
import datetime
from requests.auth import HTTPBasicAuth
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href="/" class="btn btn-dark btn-sm">Back to Products</a>'


    else:
        return render_template("single_item.html")


@app.route('/edit/<username>',methods=['POST','GET']) 
def Edit(username):
    if request.method=='POST':
         #TODO  
         name=request.form['username']
         email=request.form['email']
         password=request.form['password']
         phone=request.form['phone']
         #sql query update
         sql_update='update users set username=%s,email=%s,password=%s,phone=%s where username=%s'
         cursor_update=connection.cursor()
         cursor_update.execute(sql_update,(name,email,password,phone,username)) 
         connection.commit()
         return "Records updated " 

    else:
        sql='select * from users where username=%s'
        cursor=connection.cursor()
        cursor.execute(sql,username)
        user=cursor.fetchone()
        return render_template('edit.html',user=user)

@app.route('/feedback',methods=['POST','GET']) 
def feedback():
    if request.method=='POST':
        #TODO
        # get the posted data 
        feedback_desc=request.form['feedback_desc']
        
        # create cursor
        cursor=connection.cursor() 
        # sql
        sql='insert into feedback(feedback_desc) values(%s)'
        cursor.execute(sql,(feedback_desc))
        connection.commit()
        cursor.close()
        return render_template('feedback.html',message='Feedback sent successfully')

    else:
        return render_template('feedback.html',message='Opps!feedback not sent.Something is wrong')    
    
@app.route('/viewfeedback',methods=['POST','GET'])
def view_feedback():
    
    sql='select * from feedback'
    
    # cursor
    cursor=connection.cursor()
    cursor.execute(sql)  
    # fetch the product
    
    
    
    if cursor.rowcount=='0':
                return render_template('view_feedback.html')
    else:
        
                #fetch the records of the vendors
                data=cursor.fetchone()
                # other sessions
                session['feedback_id']=data[0]
                session['feedback_desc']=data[1]
                session['feedback_date']=data[2]
                
               
                return render_template('view_feedback.html',feedback=data)

       
import functions
@app.route('/change_password',methods=['GET','POST'])   
def change_password():
    if request.method=='POST':
        # TODO
        # get the posted data
        email=request.form['email']
        password=request.form['password']
        confirm=request.form['confirm']

        # check if password is equal to confirm
        if password != confirm:
            return render_template('change_password.html',message='Passwords do not match')
        else:
           
          #check if vendor exists
           cursor_vendor=connection.cursor()
           sql_vendor='select * from vendors where vendor_email=%s'
           cursor_vendor.execute(sql_vendor,email)
           vendor= cursor_vendor.fetchall()
           if cursor_vendor.rowcount==0:
             return render_template('change_password.html',message='User does not exist')
           else:
            # create OTP
            # TODO
            OTP=functions.generate_random()

            sql_update='update vendors set vendor_password=%s where vendor_email=%s '
            # using OTP
            sql_update='update vendors set vendor_password=%s where vendor_email=%s '

            cursor_update=connection.cursor()
            cursor_update.execute(sql_update,(OTP,email))
            connection.commit()
            functions.send_sms('+254798734353',f'Your new password is {OTP}')
            return render_template('change_password.html',message='Passwords updated successfully')



    else:
        return render_template('change_password.html')    
    

        
        
    



     
   
              

    # run app
if __name__== "__main__":
    app.run(debug=True,port=7001)    