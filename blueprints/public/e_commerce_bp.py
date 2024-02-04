from flask import Blueprint, session, redirect, url_for

# Create the e-commerce blueprint
e_commerce_bp = Blueprint("e_commerce_bp", __name__)


# Route for adding a product to the cart
@e_commerce_bp.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Get the product details based on the product_id
    # Add the product to the cart
    # You can store the cart as a list of dictionaries or any other data structure

    # Check if 'cart' key exists in the session
    if "cart" not in session:
        # If 'cart' key does not exist, create an empty cart
        session["cart"] = []

    # Add the product to the cart
    session["cart"].append(product_id)

    # Redirect the user to the cart page
    return redirect(url_for("ecommerce.cart"))


# Route for displaying the cart page
@e_commerce_bp.route("/cart", methods=["GET"])
def cart():
    # Retrieve the cart from the session
    cart = session.get("cart", [])

    # Render the cart template and pass the cart data to the template
    return render_template("cart.html", cart=cart)
