from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="studentdb"
)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form["userid"]
    password = request.form["passwordid"]

    cursor = db.cursor()

    query = "SELECT * FROM users WHERE BINARY username=%s AND BINARY password=%s"

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    if user:
        return render_template("success.html")
    else:
        return render_template("failure.html")
    
@app.route("/registerstudent")
def registerstudent():
    return render_template("registerstudent.html")

@app.route("/savestudent", methods=["POST"])
def savestudent():

    student_name = request.form["student_name"]
    student_age = request.form["student_age"]
    student_college = request.form["student_college"]
    student_phone = request.form["student_phone"]
    student_branch = request.form["student_branch"]
    password = request.form["password"]

    cursor = db.cursor()

    query = """
    INSERT INTO studentdetails
    (student_name,
     student_age,
     student_college,
     student_phone,
     student_branch,
     password)
    VALUES(%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            student_name,
            student_age,
            student_college,
            student_phone,
            student_branch,
            password
        )
    )

    db.commit()

    cursor.close()

    return "Student Registered Successfully"

@app.route("/getstudents")
def getstudents():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM studentdetails")

    students = cursor.fetchall()

    cursor.close()

    return render_template(
        "getstudents.html",
        students=students
    )

@app.route("/findstudent")
def findstudent():
    return render_template("findstudent.html")

@app.route("/searchstudent", methods=["POST"])
def searchstudent():

    student_id = request.form["student_id"]

    cursor = db.cursor()

    query = """
    SELECT * FROM studentdetails
    WHERE student_id=%s
    """

    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    cursor.close()

    if student:
        return render_template(
            "studentresult.html",
            student=student
        )
    else:
        return "Student Not Found"

if __name__ == "__main__":
    app.run(debug=True)