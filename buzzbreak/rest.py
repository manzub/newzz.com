import os
from flask import session
from flask_restful import Resource
from buzzbreak import db,mail
from buzzbreak.models import Tokens, User,Accounts,Transactions,Cashouts
from flask_mail import Message
from werkzeug.security import generate_password_hash

def sendUserMail(type,recipient):
    sender = ('NEWZZ$-AdMIN','no-reply@newzz.com')
    subject = 'New Mail From NEWZZ$'
    token = generate_password_hash(recipient)
    new_token_entry = Tokens(
        user_email=recipient,
        token=token
    )
    db.session.add(new_token_entry)
    db.session.commit()
    msg_body3 = "Your  cashout request has been rejected,\n Try again later"
    msg_body2 = "Your cashout request could not be processed \n\n Insufficent account balance"
    msg_body1 = "Your cashout request is being processed \n\n you will get a mail from us once your request has sccessfully been processed,\r\n\n Use the below to confirm if your payment email was paypal or payoneer acount\n http://newzz.com/verify/{}".format(token)
    msg_body = "Your cashout request has been processed \n\n\n Thanks from the newzz$ team"
    with mail.connect() as conn:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            sender=sender,
            body=msg_body1 if type == 1 else msg_body if type == 2 else msg_body3 if type == 4 else msg_body2
        )
        conn.send(msg)
    return True

def sendAdminMail(recipient,amount,payout_type):
    msg_body = "Cashout request has been placed\n\n user\'s email == {}".format(recipient)
    with mail.connect() as conn:
        msg = Message(
            subject='New Mail from NEWZZ$',
            recipients=['jeddachppc@gmail.com'],
            sender=('Admin','no-reply@newzz.com'),
            body=msg_body
        )
        conn.send(msg)
    new_cashout_entry = Cashouts(
        user_email=recipient,
        amount=amount,
        payout_type=payout_type
    )
    db.session.add(new_cashout_entry)
    db.session.commit()
    return True

def payout_amount(index):
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','config/payopt.txt'))
    file = open(filepath,"r")
    opts = file.readlines()
    file.close()
    return int(opts[0] if index == 1 else opts[1])

def optToAmount(opt):
    if opt == 1:
        return 200000
    elif opt == 2:
        return 500000
    else:
        return 1000000

class AddBalance(Resource):
    def get(self,type):
        if type is not None and type < 3 and session.get('user_email') is not None:
            amount = payout_amount(1) if type == 1 else payout_amount(2)
            alert = 'Recieved {} from reading newzz'.format(str(amount)) if type == 1 else 'Recieved {} from clicking Ads'.format(str(amount))
            user = User.query.filter_by(email=session['user_email']).first()
            if user is not None:
                for account in user.account:
                    account.balance = int(account.balance)+amount
                    account.t_balance = int(account.t_balance) + amount
                new_transaction = Transactions(alert,amount,user.id)
                db.session.add(new_transaction)
                db.session.commit()
                return {'status':1,'message':alert}
        return {'status':0}


class UCashOut(Resource):

    def get(self,opt):
        # check balance if he has sufficeinf funds 
        # and proceed if he does. 
        # then subtract from his balance and then send me a mail 
        # with his email for me to check out
        # and send him a mail as well
        # assuring him that his transaction will be processed
        # and ask him to verify its a paypal or payoneer account 
        # and once its done, send him a mail that it has been
        # processed and send the money to his or her paypal oor payooner  
        if opt is not None and session.get('user_email') is not None:
            user = User.query.filter_by(email=session['user_email']).first()
            if user is not None:
                account_balance = [account.balance for account in user.account][0]
                # t_balance = [account.t_balance for account in user.account][0]
                new_balance = int(account_balance) - optToAmount(opt)
                if new_balance > 0:
                    payout_extras = [payopt.extras for payopt in user.payopt][0]
                    payout_type = payout_extras if payout_extras != "" else None
                    sendAdminMail(
                        recipient=user.email,
                        amount=optToAmount(opt),
                        payout_type=payout_type
                    )
                    sendUserMail(
                        type=1,
                        recipient=user.email
                    )
                    return {'status':1,'message':'Processing Request'}
                return {'status':2,'message':'Insufficient Account Balance'}
        return {'status':0,'message':'An error occured'}

class AllCashouts(Resource):
    def get(self,index):
        if index is not None and session.get('is_admin') is not None:
            cashouts = Cashouts.query.all()
            all_cashouts = []
            for cashout in cashouts:
                all_cashouts.append({
                    'id':cashout.id,
                    'user_email':cashout.user_email,
                    'amount':cashout.amount,
                    'payout_type':cashout.payout_type
                })
            total_cashouts = len(all_cashouts)
            # indexes = round(total_cashouts/10)
            from_param = index
            to_param = index+10
            return all_cashouts[from_param:to_param]
        return {'status':0,'message':'Not Admin'}

class ActionCashout(Resource):
    def post(self,c_id):
        if c_id is not None and session.get('is_admin') is not None:
            c_request = Cashouts.query.filter_by(id=c_id).first()
            user = User.query.filter_by(email=c_request.user_email).first()
            amount_to_deduct = c_request.amount
            user_account = Accounts.query.filter_by(user_id=user.id).first()
            if int(user_account.balance) > int(amount_to_deduct):
                user_account.balance = int(user_account.balance) - int(amount_to_deduct)
                db.session.delete(c_request)
                db.session.commit()
                sendUserMail(2,user.email)
                return {'status':1,'message':'Success'}
            else:
                sendUserMail(3,user.email)
                db.session.delete(c_request)
                db.session.commit()
                return {'status':1,'message':'Could not deduct balance'}
        return {'status':0,'message':'Error occured'}

    def delete(self,c_id):
        if c_id is not None and session.get('is_admin') is not None:
            c_request = Cashouts.query.filter_by(id=c_id).first()
            user = User.query.filter_by(email=c_request.user_email).first()
            db.session.delete(c_request)
            db.session.commit()
            sendUserMail(4,user.email)
            return {'status':1,'message':'Success'}
        return {'status':0,'message':'Error occured'}

class PagesCashout(Resource):
    def get(self):
        cca = Cashouts.query.all()
        pages = round(len(cca)/10)
        return {'pages':pages}