import smtplib
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os


gmail = 'suhaibsaleem222@gmail.com'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'mysecretkey'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.Integer, nullable=True)

class All_Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    discount = db.Column(db.Integer, nullable=True)
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.Integer, nullable=True)

    
@app.route('/')
def home(): 
    po = Product.query.all()
    return render_template('index.html', products=po)
    

@app.route('/purchase/<int:id>', methods=['GET', 'POST'])
def purchase(id):
    po = Product.query.get_or_404(id)
    purchased_item = Purchase(title=po.title, description=po.description, price=po.price, filename=po.filename, discount=po.discount)
    db.session.add(purchased_item)
    db.session.commit()
    return redirect('/checkout')
    

@app.route('/remove/<int:id>')
def remove(id):
    po = Purchase.query.get_or_404(id)
    db.session.delete(po)
    db.session.commit()
    return redirect('/checkout')


@app.route('/shope/<int:id>')
def shope(id):
    po = All_Products.query.get_or_404(id)
    return render_template('shop.html', po=po)

@app.route('/shop/<int:id>')
def shop(id):
    po = Product.query.get_or_404(id)
    return render_template('shop.html', po=po)

@app.route('/product')
def product():
    home_pro = Product.query.all()
    po = All_Products.query.all()
    return render_template('product.html', po=po, home_pro=home_pro)
email = ""
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('msg')
        adress = request.form.get('adress')
        phone = request.form.get('phone')
        sending_message = msg + '\n' + phone + '\n' + email + '\n' + name + '\n' + adress
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login(gmail, 'Alphahour123')
        server.sendmail(email, gmail, sending_message)
        return redirect("/")
    return render_template('contact.html')

    

@app.route('/checkout')
def checkout():
    product = Purchase.query.all()
    sum_ = 0
    for i in product:
        sum_ = sum_ + i.price 
    return render_template('checkout.html', product=product, sum=sum_)


@app.route('/167Gkjafkjha&8927hjfna02916nfHGKJb87274989', methods=['POST', 'GET'])
def dashboard():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['des']
        price = request.form['price']
        pic = request.files['img']
        discount = request.form['discount']
        path = os.path.join(os.getcwd(), 'static\\images')
        filename = pic.filename
        if " " in filename:
            flash("No spaces allowed in file name", 'error')
        else:
            pic.save(os.path.join(path, pic.filename))
            po = All_Products(title=title, description=description, price=price, filename=filename, discount=discount)
            db.session.add(po)
            db.session.commit()
            return redirect('/')
    return render_template('dashboard.html')


@app.route('/for_main_page_only', methods=['POST', 'GET'])
def for_main_page():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['des']
        price = request.form['price']
        pic = request.files['img']
        discount = request.form['discount']
        path = os.path.join(os.getcwd(), 'static\\images')
        filename = pic.filename
        if " " in filename:
            flash("No spaces allowed in file name", 'error')
        else:
            pic.save(os.path.join(path, pic.filename))
            po = Product(title=title, description=description, price=price, filename=filename, discount=discount)
            db.session.add(po)
            db.session.commit()
            return redirect('/')
    return render_template('for_main_page_only.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'jalaldeen' and password == '112233':
            return redirect('/167Gkjafkjha&8927hjfna02916nfHGKJb87274989')
        else:
            flash('Invalid Username or Password', 'error')
    return render_template('admin.html')

@app.route('/kuch_delete_karo')
def kuch_delete_karo():
    main_page = Product.query.all()
    sari_products = All_Products.query.all()
    return render_template('kuch_delete_karo.html', main_page=main_page, sari_products=sari_products)

@app.route('/delete/<int:id>')
def delete(id):
    po = Product.query.get_or_404(id)
    db.session.delete(po)
    db.session.commit()
    return redirect('/')

@app.route('/delete_from_products/<int:id>')
def delete_from_products(id):
    po = All_Products.query.get_or_404(id)
    db.session.delete(po)
    db.session.commit()
    return redirect('/')

@app.route('/confirm_order/<int:id>', methods=['GET', 'POST'])
def confirm_order_please(id):
    if request.method == 'POST':
        order = Purchase.query.get_or_404(id)
        name = request.form.get('name')
        email = request.form.get('email')
        adress = request.form.get('adress')
        phone = request.form.get('phone')
        sending_message = f"  {phone}  '\n'  {email}  '\n'  {name}  '\n'  {adress}  '\n'  {order.title}    '\n'  {order.price} "
        server = smtplib.SMTP('smtp.gmail.com')
        server.starttls()
        server.login(gmail, 'Alphahour123')
        server.sendmail(email, gmail, sending_message)
        return redirect("/")
    return render_template('checkout.html')



if __name__ == '__main__':
    app.run(debug=True)