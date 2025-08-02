from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from datetime import time

TIME_FORMAT = "%I:%M %p"
COFFEE_RATINGS = [ "☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕" ]
STRENGTH_RATINGS = [ "✘️", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
OUTLET_RATINGS = [ "✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = URLField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = TimeField("Opening time e.g. 8:00 AM", validators=[DataRequired()])
    close = TimeField("Closing time e.g. 5:30 PM", validators=[DataRequired()]) 
    coffeeRating = SelectField("Coffee Rating", choices=COFFEE_RATINGS)
    strengthRating = SelectField("WiFi Strength Rating", choices=STRENGTH_RATINGS)
    outletRating = SelectField("Outlet Availability", choices=OUTLET_RATINGS)
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        formData = [
            form.data["cafe"],
            form.data["url"],
            form.data["open"].strftime(TIME_FORMAT),
            form.data["close"].strftime(TIME_FORMAT),
            form.data["coffeeRating"],
            form.data["strengthRating"],
            form.data["outletRating"],
        ]
        with open("cafe-data.csv", mode="a", newline="", encoding="utf-8") as csvFile:
            csvFile.write("\n" + ",".join(formData))

    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as csvFile:
        csvData = csv.reader(csvFile, delimiter=',')
        listOfRows = []
        for row in csvData:
            listOfRows.append(row)
    return render_template('cafes.html', cafes=listOfRows, numCafes=len(listOfRows))


if __name__ == "__main__":
    app.run(debug=True)
