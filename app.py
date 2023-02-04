from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from models import *
from menus.menu import *
from distance import find
from decimal import Decimal
from wiki import wikibot
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ProfessorSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/vet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)


# with app.app_context():
#     db.create_all()
 
@app.route("/wa")
def wa_hello():
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
    # Create reply
 
    # Text response
    if msg == "cancel":
        bot.menu = 'main'
        db.session.commit()

        reply.body("The process has been cancelled.")

    elif msg == "help":
        reply.body(help())
 
    else:
        if msg == "menu":
            bot.menu = 'main'
            db.session.commit()

            reply.body(main_menu())

        if bot.menu == "main":
            if msg == "1":
                bot.menu = 'main-general'
                db.session.commit()

                reply.body(general_agric_info())

            elif msg == "2":
                bot.menu = 'main-branch'
                db.session.commit()

                reply.body(nearest_branch())

            elif msg == "3":
                bot.menu = 'main-quote'
                db.session.commit()

                message = "*GET QUOTATION*\n"
                products = Product.query.all()
                results = products_schema.dump(products)
                for product in products:
                    #print(product)
                    message = message+"*"+product.code+"* "+product.name+" $"+str(product.price)+"\n"

                message = message+"\n_Select the product code and seperate with a comma to  generate a custom quote eg *1001,1002,1009* no spaces allowed._ \n*cancel* to exit, *help* for help."
                reply.body(message)
        
        elif bot.menu == "main-general":
            qstn = msg.replace(' ', '_')
            answer = wikibot(qstn)

            answer = answer + "\n\n *cancel* to exit, *help* for help."
            print(answer)
            reply.body(answer)

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

        elif bot.menu == "main-quote":
            options = msg.split(',')
            quote = Product.query.filter(Product.code.in_(options)).all()
            total_price = 0.00
            custom_quote = "*CUSTOM QUOTE - "+name+"*\n\n"
            for q in quote:
                custom_quote = custom_quote + "*"+q.code+"* "+q.name+" $"+str(q.price)+"\n"
                total_price = Decimal(total_price) + Decimal(q.price)
            
            custom_quote = custom_quote + "\n*Price* $"+str(total_price)+"\n*Discount* $0.00\n*Total Price* $"+str(total_price)+"\n"
            
            custom_quote = custom_quote + "\n*cancel* to exit, *help* for help."
            reply.body(custom_quote)


 
    



    #print(request.form)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)