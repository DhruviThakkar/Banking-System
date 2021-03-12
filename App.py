from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'I am superman'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:dhruvi07@localhost/test'
db = SQLAlchemy(app)

class Customers(db.Model):
    account_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email_id = db.Column(db.String(100))
    balance = db.Column(db.Integer)

    def __init__(self, account_no, name, email_id, balance):
        self.account_no = account_no
        self.name = name
        self.email_id = email_id
        self.balance = balance

class History(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    sender_acc = db.Column(db.Integer)
    receiver_acc = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(50))
    time = db.Column(db.String(50))

    def __init__(self, sender_acc, receiver_acc, amount, status, time):

                self.sender_acc = sender_acc
                self.receiver_acc = receiver_acc
                self.amount = amount
                self.status = status
                self.time = time


@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/customers')
def customers():
    customers = Customers.query.filter_by().all()
    #print (customers)
    return render_template('customers.html',customers=customers)

@app.route('/history')
def history():
    history = History.query.filter_by().all()
    return render_template('history.html', history=history)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'GET':
        return render_template('transfer.html')
    else:
        sender = int(request.form.get('sender_acc'))
        receiver = int(request.form.get('receiver_acc'))
        amount = float(request.form.get('amount'))
        sender_data = Customers.query.filter_by(account_no = sender).first()
        receiver_data = Customers.query.filter_by(account_no=receiver).first()
        if sender_data.balance >= amount:
            sender_data.balance = sender_data.balance-amount
            receiver_data.balance = receiver_data.balance+amount
            try:
                db.session.commit()
                flash('Transaction Done Successfully', 'success')
                history = History(sender_data.account_no, receiver_data.account_no, amount, 'Success', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                db.session.add(history)
                db.session.commit()
            except IntegrityError:
                flash('Transaction Failed', 'danger')
                history = History(sender_data.account_no, receiver_data.account_no, amount, 'Failed', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                db.session.add(history)
                db.session.commit()
            return render_template('transfer.html')
        else:
            flash('Insufficient Funds', 'danger')
            history = History(sender_data.account_no, receiver_data.account_no, amount, 'Failed', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            db.session.add(history)
            db.session.commit()
            return render_template('transfer.html')


if __name__ == '__main__':
    app.run(debug=True)