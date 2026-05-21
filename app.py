from flask import Flask, render_template, jsonify
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'someRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return f'User {self.username}'


class ShippingInfo(db.Model):
    ship_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"{self.full_name}'s address is {self.address}."


def seed_shipping_info():
    db.create_all()

    shipping_records = [
        {
            "full_name": "Claudia Reyes",
            "address": "Amsterdam 210, CDMX, Mexico",
            "user_id": 2
        },
        {
            "full_name": "Roy Latte",
            "address": "Beau St, Bath BA1 1QY, UK",
            "user_id": 1
        }
    ]

    for record in shipping_records:
        existing_record = ShippingInfo.query.filter_by(
            full_name=record["full_name"],
            address=record["address"],
            user_id=record["user_id"]
        ).first()

        if existing_record is None:
            new_shipping_record = ShippingInfo(
                full_name=record["full_name"],
                address=record["address"],
                user_id=record["user_id"]
            )

            db.session.add(new_shipping_record)

    db.session.commit()


with app.app_context():
    seed_shipping_info()


@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')


@app.route('/inventory', methods=['GET'])
def inventory():
    return render_template('inventory.html', beans=["arabica", "robusta"])


@app.route("/shop", methods=["GET"])
def shop():
    cart = ["12oz Medium Roast", "24oz French Roast", "96oz Whole Beans"]
    return render_template("shop.html", cart=cart)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    message = ""

    if form.validate_on_submit():
        username = form.username.data
        password = form.pwd.data

        user_match = User.query.filter_by(username=username).first()

        if user_match is None:
            new_user = User(
                username=username,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            message = f"Successfully registered {username}!"
        else:
            message = "That username already exists. Please choose another username."

    return render_template(
        "register.html",
        form=form,
        message=message
    )


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/admin", methods=["GET"])
def admin():
    db_users = User.query.all()
    db_shippers = ShippingInfo.query.all()

    users = []

    for db_user in db_users:
        users.append({
            "username": db_user.username,
            "id": db_user.id
        })

    shippers = []

    for db_shipper in db_shippers:
        shippers.append({
            "full_name": db_shipper.full_name,
            "address": db_shipper.address,
            "user_id": db_shipper.user_id
        })

    return jsonify({
        "users": users,
        "shippers": shippers
    })


if __name__ == '__main__':
    app.run(debug=True)