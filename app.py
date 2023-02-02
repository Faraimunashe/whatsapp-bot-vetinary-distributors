from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from models import *
from menus.menu import *
 
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

                reply.body(quotations())
        
        elif bot.menu == "main-general":
            if msg == "1":
                bot.menu = 'main-general-machinery'
                db.session.commit()

                reply.body(machinery())

        elif bot.menu == "main-branch":
            if msg == "1":
                bot.menu = 'main-general-machinery'
                db.session.commit()

                reply.body(machinery())


 
    



    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)