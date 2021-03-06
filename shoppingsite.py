"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
from customers import customers
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types

    ordered_melons = {}
    total = 0

    if 'cart' in session:
        for melon_id in set(session['cart']):

            ordered_melons[melon_id] = {}
            ordered_melons[melon_id]['quantity'] = session["cart"].count(melon_id)
            melon = melons.get_by_id(melon_id)
            ordered_melons[melon_id]['name'] = melon.common_name
            ordered_melons[melon_id]['price'] = melon.price
            total = total + (ordered_melons[melon_id]['quantity'] * ordered_melons[melon_id]['price'])        

    # flash(ordered_melons) # Test code to see dictionary

    return render_template("cart.html", ordered_melons=ordered_melons, total=total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session

    session['cart'] = session.get('cart', [])
    session['cart'].append(id)

    # flash(session['cart']) # Test code to see contents of session['cart']
    # Add melon name to flash message later
    flash("Melon added to cart")


    return redirect("/melons")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    if 'logged_in_customer_email' not in session: 
        return render_template("login.html")
    else:
        flash("You are logged in")
        return redirect("/melons")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    # TODO: Need to implement this!

    if email in customers and customers[email].pw == password:
        session['logged_in_customer_email'] = email
        flash("Success! You are logged in.")
        return redirect("/melons")
    elif email in customers and customers[email].pw != password:
        flash("Incorrect password.")
        return redirect("/login")
    else:
        flash("No such email.")
        return redirect("/login")


    # return "Oops! This needs to be implemented"

@app.route('/logout')
def process_logout():
    """Log customer out of session and delete session key"""

    del session['logged_in_customer_email']
    flash('You have successfully logged out.')
    return redirect("/melons")

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    app.run()

