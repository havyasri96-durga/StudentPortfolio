from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="studentdb"
)

# ======================================================
# LOGIN
# ======================================================
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("userid")
    password = request.form.get("passwordid")

    cursor = db.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE BINARY username=%s
        AND BINARY password=%s
    """, (username, password))

    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template("success.html")
    return render_template("failure.html")


# ======================================================
# STUDENT MODULE
# ======================================================
@app.route("/registerstudent")
def registerstudent():
    return render_template("registerstudent.html")


@app.route("/savestudent", methods=["POST"])
def savestudent():

    data = request.form

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO studentdetails
        (student_name, student_age, student_college, student_phone, student_branch, password)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        data.get("student_name"),
        data.get("student_age"),
        data.get("student_college"),
        data.get("student_phone"),
        data.get("student_branch"),
        data.get("password")
    ))

    db.commit()
    cursor.close()

    return redirect("/getstudents")


@app.route("/getstudents")
def getstudents():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM studentdetails")
    students = cursor.fetchall()
    cursor.close()

    return render_template("getstudents.html", students=students)


@app.route("/findstudent")
def findstudent():
    return render_template("findstudent.html")


@app.route("/searchstudent", methods=["POST"])
def searchstudent():

    student_id = request.form.get("student_id")
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM studentdetails WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    cursor.close()

    
    return render_template("studentresult.html", student=student)

    

@app.route("/updatestudent")
def updatestudent():
    return render_template("updatestudent.html")


@app.route("/updaterecord", methods=["POST"])
def updaterecord():

    data = request.form

    cursor = db.cursor()

    cursor.execute("""
        UPDATE studentdetails
        SET student_name=%s,
            student_phone=%s
        WHERE student_id=%s
    """, (
        data.get("student_name"),
        data.get("student_phone"),
        data.get("student_id")
    ))

    db.commit()
    cursor.close()

    return redirect("/getstudents")

@app.route("/deletestudent")
def deletestudent():
    return render_template("deletestudent.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():

    student_id = request.form.get("student_id")

    cursor = db.cursor()
    cursor.execute("DELETE FROM studentdetails WHERE student_id=%s", (student_id,))
    db.commit()
    cursor.close()

    return redirect("/getstudents")


# ======================================================
# PRODUCT MODULE
# ======================================================
@app.route("/addproduct")
def addproduct():
    return render_template("addproduct.html")


@app.route("/saveproduct", methods=["POST"])
def saveproduct():

    data = request.form

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO products
        (product_name, price, quantity)
        VALUES (%s,%s,%s)
    """, (
        data.get("product_name"),
        float(data.get("price")),
        int(data.get("quantity"))
    ))

    db.commit()
    cursor.close()

    return redirect("/products")


@app.route("/products")
def products():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return render_template("products.html", products=products)


@app.route("/updateproduct")
def updateproduct():
    return render_template("updateproduct.html")


@app.route("/updateproductrecord", methods=["POST"])
def updateproductrecord():

    data = request.form

    cursor = db.cursor()

    cursor.execute("""
        UPDATE products
        SET price=%s,
            quantity=%s
        WHERE product_id=%s
    """, (
        float(data.get("price")),
        int(data.get("quantity")),
        data.get("product_id")
    ))

    db.commit()
    cursor.close()

    return redirect("/products")


@app.route("/deleteproduct")
def deleteproduct():
    return render_template("deleteproduct.html")


@app.route("/deleteproductrecord", methods=["POST"])
def deleteproductrecord():

    product_id = request.form.get("product_id")

    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
    db.commit()
    cursor.close()

    return redirect("/products")


@app.route("/searchproduct")
def searchproduct():
    return render_template("searchproduct.html")


@app.route("/findproductrecord", methods=["POST"])
def findproductrecord():

    product_id = request.form.get("product_id")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.close()

    if product:
        return render_template("productresult.html", product=product)

    return "Product Not Found"


# ======================================================
# ORDER MODULE
# ======================================================
@app.route("/buyproduct")
def buyproduct():
    return render_template("buyproduct.html")


@app.route("/saveorder", methods=["POST"])
def saveorder():

    data = request.form

    student_name = data.get("student_name")
    product_name = data.get("product_name")
    quantity = int(data.get("quantity"))

    cursor = db.cursor(buffered=True)

    cursor.execute("""
        SELECT price, quantity
        FROM products
        WHERE product_name=%s
    """, (product_name,))

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product Not Found"

    price, available_qty = product

    if quantity > available_qty:
        cursor.close()
        return "Insufficient Stock"

    total = price * quantity
    remaining = available_qty - quantity

    cursor.execute("""
        INSERT INTO orders
        (student_name, product_name, quantity, total_amount)
        VALUES (%s,%s,%s,%s)
    """, (student_name, product_name, quantity, total))

    cursor.execute("""
        UPDATE products
        SET quantity=%s
        WHERE product_name=%s
    """, (remaining, product_name))

    db.commit()
    cursor.close()

    return redirect("/orders")


@app.route("/orders")
def orders():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()

    return render_template("orders.html", orders=orders)


# ======================================================
# CART MODULE
# ======================================================
@app.route("/addtocart")
def addtocart():
    return render_template("addtocart.html")


@app.route("/savecart", methods=["POST"])
def savecart():

    data = request.form

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO cart
        (student_name, product_name, quantity)
        VALUES (%s,%s,%s)
    """, (
        data.get("student_name"),
        data.get("product_name"),
        data.get("quantity")
    ))

    db.commit()
    cursor.close()

    return redirect("/viewcart")

@app.route("/viewcart")
def viewcart():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM cart")
    items = cursor.fetchall()

    total = 0

    cart_with_price = []

    for item in items:
        cart_id = item[0]
        student_name = item[1]
        product_name = item[2]
        quantity = item[3]

        # 🔥 Get price from products table
        cursor.execute(
            "SELECT price FROM products WHERE product_name=%s",
            (product_name,)
        )

        result = cursor.fetchone()

        if result:
            price = result[0]
            subtotal = price * quantity
            total += subtotal

            cart_with_price.append((
                cart_id,
                student_name,
                product_name,
                price,
                quantity,
                subtotal
            ))

    cursor.close()

    return render_template(
        "viewcart.html",
        cart=cart_with_price,
        total=total
    )

@app.route("/deletecart/<int:cart_id>")
def deletecart(cart_id):

    cursor = db.cursor()
    cursor.execute("DELETE FROM cart WHERE cart_id=%s", (cart_id,))
    db.commit()
    cursor.close()

    return redirect("/viewcart")


# ======================================================
# DASHBOARD MODULE
# ======================================================
@app.route("/studentservices")
def studentservices():
    return render_template("studentservices.html")


@app.route("/storemanagement")
def storemanagement():
    return render_template("storemanagement.html")


@app.route("/customershopping")
def customershopping():
    return render_template("customershopping.html")


@app.route("/reports")
def reports():

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM studentdetails")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_amount) FROM orders")
    revenue = cursor.fetchone()[0] or 0

    cursor.close()

    return render_template(
        "reports.html",
        total_students=total_students,
        total_products=total_products,
        total_orders=total_orders,
        revenue=revenue
    )


@app.route("/dashboard")
def dashboard():
    return render_template("success.html")

@app.route("/browseproducts", methods=["GET", "POST"])
def browseproducts():

    cursor = db.cursor()

    if request.method == "POST":
        search = request.form.get("search")

        cursor.execute("""
            SELECT product_name, price 
            FROM products
            WHERE product_name LIKE %s
        """, ('%' + search + '%',))

    else:
        cursor.execute("SELECT product_name, price FROM products")

    products = cursor.fetchall()
    cursor.close()

    return render_template("browseproducts.html", products=products) 

# ======================================================
# RUN APP
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)