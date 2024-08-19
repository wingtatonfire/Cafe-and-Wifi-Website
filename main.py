from flask import Flask, render_template, url_for, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import os

SECRET_KEY = os.urandom(32)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    map_url: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    has_sockets: Mapped[str] = mapped_column(nullable=False)
    has_toilet: Mapped[str] = mapped_column(nullable=False)
    has_wifi: Mapped[str] = mapped_column(nullable=False)
    can_take_calls: Mapped[str] = mapped_column(nullable=False)
    seats: Mapped[str] = mapped_column(nullable=False)
    coffee_price: Mapped[str] = mapped_column(nullable=False)

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = StringField('Map Url', validators=[DataRequired()])
    img_url = StringField('Img Url', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = BooleanField('Has Socket?')
    has_toilet = BooleanField('Has Toilet?')
    has_wifi = BooleanField('Has Wifi?')
    can_take_calls = BooleanField('Can Take Calls?')
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Price of Coffee', validators=[DataRequired()])
    submit = SubmitField("Add Cafe")

with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap5(app)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all_cafe")
def all_cafe():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return render_template("all_cafe.html", cafes=cafes)


@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    form = MyForm()
    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=bool(form.has_sockets.data),
            has_toilet=bool(form.has_toilet.data),
            has_wifi=bool(form.has_wifi.data),
            can_take_calls=bool(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('all_cafe'))

    return render_template("add_cafe.html", form=form)


app.run(debug=True)
