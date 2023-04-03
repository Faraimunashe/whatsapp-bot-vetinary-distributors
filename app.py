from flask import Flask, request, render_template, make_response
from twilio.twiml.messaging_response import MessagingResponse
from models import *
from menus.menu import *
from distance import find
from decimal import Decimal
from wiki import wikibot
import re
from get_int import integer
import pdfkit
import os
import string
import random
from datetime import datetime
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ProfessorSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/vet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)


with app.app_context():
    db.create_all()

GREETING_INPUTS = ("hi", "hello", "hey", "helloo", "hellooo", "g morning",  "gmorning",  "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g'day", "howdy",)
GREETING_RESPONSES = ["hi", "hey", "hellooo", "hi there", "hello", "I am glad! You are talking to me", "Great, hope you're good!", "I am ok", "Hey! How may i help you?"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

PRODUCT_LISTING = ("products", "list", "list products", "products list", "product listing","list available products", "show me products", "show products", "can i have your product list",)
PRODUCT_RESPONSES = ["Well! here you are", "This is the product list"]
def list_products(sentence):
    for word in sentence.split():
        if word.lower() in PRODUCT_LISTING:
            return random.choice(PRODUCT_RESPONSES)
    
LOCATION_LISTING = ("location", "neareast", "nearest branch", "closest branch", "near branch", "close branch", "my branch", "where to find help", "close location", "close office", "branch in my area", "branch around", "where can i find you", "visit", "in my area", "where are you located",)
LOCATION_RESPONSES = ["Ok! Send me your location and i tell you.", "Fine, Send me your location.", "Send your location.", "May you please send me your location", "Where are you? send me location", "If you send me your location i can tell you."]
def list_locations(sentence):
    for word in sentence.split():
        if word.lower() in LOCATION_LISTING:
            return random.choice(LOCATION_RESPONSES)
        

QUOTE_LISTING = ("quotation", "quotations", "how to take quotation", "how do i take a quotation", "i want a quotation", "give me a quotation", "see quotation", "i need a quotation",)
QUOTE_RESPONSES = ["Ok! It's easy, just include the word quote and the names of the products you want, include quantity after every product eg Product x4.", "Fine, Send me the word quote followed by your Product x any quantity."]
def list_quotes(sentence):
    for word in sentence.split():
        if word.lower() in QUOTE_LISTING:
            return random.choice(QUOTE_RESPONSES)


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

 
@app.route("/wa")
def wa_hello():
    render = render_template('quote.html')
    return "Hello, World!"
 
@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    phone = request.form.get('WaId')
    name = request.form.get('ProfileName')
    bot = Bot.query.filter(phone==phone).first()

    if bot is None:
        new_bot = Bot(name, phone, 'main')
        db.session.add(new_bot)
        db.session.commit()
 
    msg = request.form.get('Body').lower() # Reading the message from the whatsapp
 
    
    resp = MessagingResponse()
    reply=resp.message()
    print(reply)
    # Create reply
 
    # Text response
    if msg == "cancel":
        bot.menu = 'main'
        db.session.commit()

        reply.body("The process has been cancelled.")

    elif msg == "help":
        reply.body(help())
    
    elif "quote" in msg:
        #string = "This is a test string with Bmamectin x1, Penstrep x3, Multidip x6"
        string = msg
        pattern = r"[Xx][1-9][0-9]*"
        total_price = 0.00
        quotations = []
        randomstring = randomword(16)
        docname = str(randomstring) + '.pdf'
        css = 'static/style.css'
        

        matches = re.findall(pattern, string)
        prodpattern = rf'(\w+)\s*(?:\b(?:{"|".join(matches)})\b)'
        prodmatch = re.findall(prodpattern, string)
        #print(prodmatch, matches)

        if prodmatch:
            i=0
            for sch in prodmatch:
                quote = {}
                prod = Product.query.filter(Product.name.like(sch)).first()
                if prod != None:
                    price = prod.price * int(integer(matches[i]))
                    total_price = Decimal(total_price) + Decimal(price)
                    quote = {'name':prod.name, 'unit':prod.price, 'qty':matches[i], 'total':price}
                    quotations.append(quote)
                    i=i+1
                    
                else:
                    i=i+1
                
        else:
            custom_quote = "\n Could not locate products in your request. \n"
        

        current_dateTime = datetime.now()
        pdf_content = render_template('quote.html', quotations=quotations, total=total_price, name=name, phone=phone, current_dateTime=current_dateTime) 
        configpath = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

        static_dir = os.path.abspath('static')
        pdf_file = pdfkit.from_string(pdf_content, configuration=configpath, css=css)
        with open(os.path.join(static_dir, docname), 'wb') as f:
            f.write(pdf_file)


        reply.media("static/"+docname)
    else:
        if(list_products(msg) != None):

            message = "*Product List*\n"
            products = Product.query.all()
            for product in products:
                message = message+"*"+product.code+"* "+product.name+" $"+str(product.price)+"\n"

            message = message+"\n_Now you can request a quotation by specifying product name and quantity e.g PRODUCT x3_"
            reply.body(message)

        elif(list_locations(msg) != None):
            bot.menu = 'main-branch'
            db.session.commit()

            reply.body(list_locations(msg))

        elif bot.menu == "main-branch":
            latitude = request.form.get('Latitude')
            longitude = request.form.get('Longitude')

            if latitude == None or longitude == None:
                reply.body("*Please us a valid location*")
            else:
                branches = Branch.query.all()
                result = branches_schema.dump(branches)
                # print(branches)
                # print("\n New Line here \n")
                # print(result)
                user_location = (latitude, longitude)
                distance_array = []
                for res in branches:
                    branch_location = (res.latitude, res.longitude)
                    distance = find(user_location, branch_location)
                    distance_array.append(distance)
                
                pos = distance_array.index(min(distance_array))
                print(branches[pos].name)
                bot.menu = 'main'
                db.session.commit()
                reply.body("*THE NEAREST BRANCH:*\n *"+branches[pos].name+"*\n *address:* "+branches[pos].address+"\n *telephone:* "+branches[pos].telephone+"\n *mobile:* "+branches[pos].mobile+"\n *email:* "+branches[pos].email)

        elif(greeting(msg) != None):
            bot.menu = 'main'
            db.session.commit()

            reply.body(greeting(msg))

        elif(list_quotes(msg) != None):
            bot.menu = 'main'
            db.session.commit()

            reply.body(list_quotes(msg))

        else:
            qstn = msg.replace(' ', '_')
            answer = wikibot(qstn)

            answer = answer + "\n\n"
            print(answer)
            reply.body(answer)


    #print(request.form)
    print(msg)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)