import os
from random import randint
import newsapi
from buzzbreak import app,db
from flask import (
    render_template,
    redirect,
    url_for,
    session,
    flash,
    json,
    request,
    jsonify,
    abort,
    send_from_directory
)
import requests
import datetime
from flask_login import login_user,login_required,logout_user
from buzzbreak.models import Cashouts, Tokens, User,PayOpt,Accounts
from buzzbreak.forms import AdminLogin, LoginForm,RegisterForm,AddPayOptForm, UpdatePayInfo,VerifyPayOptForm
from flask_restful import Api
from buzzbreak.rest import ActionCashout, AddBalance, AllCashouts,UCashOut
from newsapi import NewsApiClient
# payment_option1 = {'id':1,'name':"Paypal"}
# payment_option2 = {'id':2,'name':"Payooner"}
# 1000pts = 0.01 || 0.001 = 100
api = Api(app)
api.add_resource(AddBalance,'/api/add_balance/<int:type>')
api.add_resource(UCashOut,'/api/cashout/<int:opt>')
api.add_resource(AllCashouts,'/api/all_cashouts/<int:index>')
api.add_resource(ActionCashout,'/api/cashout_actions/<int:c_id>')
def newsApi(count=None):
    newsapi = NewsApiClient(api_key='d09a1c4e05634552afe6771f90a78718')
    dt = datetime.datetime.utcnow()
    month = '0'+str(dt.month) if dt.month < 10 else dt.month
    raw_day = dt.day-1 if dt.day > 1 else dt.day
    day = '0'+str(raw_day) if raw_day < 10 else raw_day
    yesterday = "{}-{}-{}".format(dt.year,month,day)
    print(yesterday)
    try:
        # if there was page var
        # articles_raw = requests.get('http://newsapi.org/v2/everything?q=apple&from={}&to={}&sortBy=popularity&apiKey=d09a1c4e05634552afe6771f90a78718'.format(yesterday,yesterday)).json()['articles']
        articles_raw = newsapi.get_everything(
            q='celebrity',
            from_param=yesterday,
            to=yesterday,
            language='en',
            sort_by='relevancy',
            # page=
        )
        jsonData = []
        i=0
        for articles in articles_raw['articles']:
            i+=1
            jsonData.append({
                'id':len(articles['url'])+i,
                'title':articles['title'],
                'description':articles['description'],
                'urlToImage':articles['urlToImage'],
                'publishedAt':articles['publishedAt'],
                'content':articles['content']
            })
        if count is not None:
            for elem in jsonData:
                if int(count) == int(elem['id']):
                    return elem
        else:
            return jsonData
    except requests.RequestException:
        return 501


def isAdmin(email,password):
    if email == 'no-reply@newzz.com' and password == '123456654321':
        return True
    return False

@app.route('/')
@login_required
def index():
    jsonData = newsApi()
    # test out this line
    # if is_read > 20 -- ajax to get new page
    if jsonData == 501:
        abort(404,description="Could not connect to server")
    return render_template('home.html',articles_raw=jsonData)

@app.route('/read/<count>')
@login_required
def read(count):
    article = newsApi(count)
    return render_template('read.html', article=article)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            session['user_email'] = user.email
            flash("Logged In Successfully!")
            next = request.args.get('next')
            if next == None or not next[0] == "/":
                next = url_for('index')
            return redirect(next)
        else:
            flash("Invalid User Details.")
    return render_template('login.html',form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   form = RegisterForm()
   if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        new_account = Accounts(
            balance='0',
            t_balance='0',
            user_id=user.id
        )
        db.session.add(new_account)
        db.session.commit()
        flash("Thanks for joining!")
        return redirect(url_for('login'))
   return render_template("signup.html", form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = AddPayOptForm()
    user = User.query.filter_by(email=session['user_email']).first()
    payopt = PayOpt.query.filter_by(user_id=user.id).first()
    has_opt = False if payopt is None else True
    if form.validate_on_submit():
        if not has_opt:
            new_payopt = PayOpt(
                '0',
                form.payment_email.data,
                user.id,
                ''
            )
            db.session.add(new_payopt)
            db.session.commit()
        flash("Payment Option Added!.")
    return render_template('dashboard.html',form=form,user=user,has_opt=has_opt)

@app.route('/cashout')
@login_required
def cashout():
    user = User.query.filter_by(email=session['user_email']).first()
    return render_template('cashout.html',user=user)

@app.route('/verify/<token>', methods=['GET', 'POST'])
def verify(token):
    form = VerifyPayOptForm()
    user_token = Tokens.query.filter_by(token=token).first()
    if user_token is not None:
        user = User.query.filter_by(email=user_token.user_email).first()
        payopt = PayOpt.query.filter_by(user_id=user.id).first()
        # check datetime here
        if form.validate_on_submit():
            payopt.extras = form.payment_type.data
            payout_reqs = Cashouts.query.all()
            for reqs in payout_reqs:
                if reqs.user_email == user.email:
                    reqs.payout_type = form.payment_type.data
            db.session.commit()
            flash("Payment Info Updated")
        return render_template('verify.html',form=form)
    else:
        abort(404,description='Invalid User Token')

@app.route('/guide')
def how_to():
    return render_template('how_to.html')

@app.route('/admin/<token>', methods=['GET','POST'])
def admin(token):
    if token == 'mynewzzadmin':
        cashouts = Cashouts.query.all()
        pages = round(len(cashouts)/10)
        form = AdminLogin()
        payopt_form = UpdatePayInfo()
        payopt_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__),'config/payopt.txt'))
        payopt_file = open(payopt_filepath,'r')
        payopts = payopt_file.readlines()
        payopt_file.close()
        if form.validate_on_submit():
            if isAdmin(form.admin_email.data,form.password.data):
                session['is_admin'] = True
                return redirect(url_for('admin',token='mynewzzadmin'))
            else:
                flash('Invalid Login Details!.')
        elif payopt_form.validate_on_submit():
            payopt_file = open(payopt_filepath,'w')
            lines = [payopt_form.read_payopt.data+"\n",payopt_form.onclick_payopt.data]
            payopt_file.writelines(lines)
            payopt_file.close()
            return redirect(url_for('admin',token='mynewzzadmin'))
        return render_template('admin.html',form=form,pages=range(1,pages),payopt_form=payopt_form,payopts=payopts)
    elif token == 'mynewzzadmin-logout':
        session.pop('is_admin')
        return redirect(url_for('admin',token='mynewzzadmin'))
    else:
        abort(404,description="Invalid Admin Token")

@app.route('/logout')
@login_required
def logout():
   logout_user()
   flash("Logged Out successfully!")
   return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html",err=e)

if __name__ == '__main__':
    mode = "dev"
    app.run(debug=True if mode == "dev" else None,host="0.0.0.0",port="5000")