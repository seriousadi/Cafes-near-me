import html.parser
import http

from flask import Flask, jsonify, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "alksdjflkasjdf;lkasdjf#@;lkjasd*lkfjew#@$o;#@#@irjoQ32R023U42EJ*FDLKSN*CKJSDGH #@#@UV4TOI#@ XN,NX, "
csrf = CSRFProtect(app)
Bootstrap(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# WTF FORMS
class AddCafeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    map_url = StringField('map_url', validators=[DataRequired()])
    img_url = StringField('img_url', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    seats = StringField('seats', validators=[DataRequired()])
    has_toilet = SelectField('has_toilet', choices=[(1, "True"), (0, "False")], default="False")
    has_wifi = SelectField('has_wifi', choices=[(1, "True"), (0, "False")], default="False")
    has_sockets = SelectField('has_sockets', choices=[(1, "True"), (0, "False")], default="False")
    can_take_calls = SelectField('can_take_calls', choices=[(1, "True"), (0, "False")], default="False")
    coffee_price = StringField('coffee_price')
    submit_cafe = SubmitField('Submit_cafe')


class RemoveCafe(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit_cafe = SubmitField("Submit_cafe")


## HTTP GET - records and set to site
@app.route("/")
def home():
    cafes = db.session.execute(db.select(Cafe).order_by()).scalars()
    return render_template("index.html", cafes=cafes)


## HTTP POST - Create Record
@app.route('/add-cafe-form', methods=['POST', 'GET'])
def add_cafe_form():
    form = AddCafeForm()
    if request.method == 'POST' and form.validate():
        data = request.form
        print(data)
        cafe_name = db.session.execute(db.select(Cafe).filter_by(name=data['name'])).scalar_one_or_none()

        if cafe_name != None:
            print("its's none")
            flash("This cafe already exists in our database.")
        else:
            cafe = Cafe(
                name=data['name'],
                map_url=data['map_url'],
                img_url=data['img_url'],
                location=data['location'],
                seats=data['seats'],
                has_toilet=int(data['has_toilet']),
                has_wifi=int(data['has_wifi']),
                has_sockets=int(data['has_sockets']),
                can_take_calls=int(data['can_take_calls']),
                coffee_price=data['coffee_price']
            )
            db.session.add(cafe)
            db.session.commit()
            flash("Thanks! Cafe added to the database")

        redirect(url_for("add_cafe_form"))
    return render_template("add_cafe.html", form=form)


## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete cafe
@app.route("/delete-cafe", methods=['POST', 'GET'])
def delete_cafe():
    form = RemoveCafe()

    if request.method == 'POST' and form.validate():
        data = request.form
        cafe_name = db.session.execute(db.select(Cafe).filter_by(name=data['name'])).scalar_one_or_none()
        if cafe_name == None:
            flash("Sorry,This cafe doesn't exists in our database.")
        else:
            db.session.delete(cafe_name)
            db.session.commit()
            flash("successfully deleted the cafe from our database")
        redirect(url_for('delete_cafe'))
    return render_template("delete.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
