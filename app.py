from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

app.secret_key = "tZ350KsDn78"

# TODO: add comments

@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        myUser = db_session.query(User).where((User.username == username) & (User.password == password)).first()
        if myUser is not None and myUser.username == username and myUser.password == password:
            session["username"] = username 
            return redirect(url_for("myprofile"))
        else:
            flash("Incorrect username or password. Try again", "error")
            return redirect(url_for("login"))

#Create an account with Username, Password, Email, and Mentor/Student
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        usertype = request.form["user-type"]
        usernameExists = db_session.query(User).where(User.username == username).first()
        #only create new user if username isn't already taken
        if usernameExists is None:
            db_session.add(User(username, password, email, usertype))
            db_session.commit()
            return redirect(url_for("login"))
        else:
            flash("Username already exists. Please create another one", "error")
            return redirect(url_for("signup"))

#
def match():
    myUser = db_session.query(User).where(User.username == session["username"]).first()
    finalList = []
    mentorList = db_session.query(User).where(User.usertype == "mentor").all()
    studentList = db_session.query(User).where(User.usertype == "student").all()
    if(myUser.usertype == "student"):
        for mentor in mentorList:
            for time in mentor.times:
                if(time in myUser.times):
                    for subject in mentor.subjects:
                        if(subject in myUser.subjects):
                            appendString = mentor.username + "," + str(subject) + "," + str(time) + "," + mentor.email
                            finalList.append(appendString)
    elif(myUser.usertype == "mentor"):
        for student in studentList:
            for time in student.times:
                if(time in myUser.times):
                    for subject in student.subjects:
                        if(subject in myUser.subjects):
                            appendString = student.username + "," + str(subject) + "," + str(time) + "," + student.email
                            finalList.append(appendString)
    return finalList


#Displays a users subjects and availabilities as well as the results of the time matching
@app.route("/myprofile")
def myprofile():
    myUser = db_session.query(User).where(User.username == session.get("username")).first()
    usrnm = myUser.username
    subjects = myUser.subjects
    timelist = myUser.times
    userList = match()
    splitList = []
    for string in userList:
        splitList.append(string.split(","))
    return render_template("myprofile.html", username = usrnm, subjectlist = subjects, timelist = timelist, userlist = splitList)

#can add/delete subjects and times
@app.route("/addinfo", methods = ["GET", "POST"])
def addinfo():
    if request.method == "GET":
        return render_template("myinfo.html")
    elif request.method == "POST":
        if "subject_submit" in request.form:
            subject = request.form["subject"]
            myUserID = db_session.query(User.id).where(User.username == session["username"]).first()[0]
            subjectExist = db_session.query(Subject.name).where(Subject.name == subject).first()
            #add the subject if it doesn't exist, otherwise just link the user and subject
            if subjectExist is None:
                db_session.add(Subject(subject))
                db_session.commit()
            currSubjectID = db_session.query(Subject.id).where(Subject.name == subject).first()[0]
            db_session.add(TutorSubject(currSubjectID, myUserID))
            db_session.commit()
            return redirect(url_for("myprofile"))
        elif "subject_delete_submit" in request.form:
            subject = request.form["delete-subject"] 
            subjectDeleteID = db_session.query(Subject.id).where(Subject.name == subject).first()[0]
            myUserID = db_session.query(User.id).where(User.username == session["username"]).first()[0]
            if subjectDeleteID is None:
                flash("This subject was not added", "info")
                return redirect(url_for("addinfo"))
            TutorSubjectToDelete = db_session.query(TutorSubject).where((TutorSubject.subject_id == subjectDeleteID) & (TutorSubject.user_id == myUserID)).first()
            db_session.delete(TutorSubjectToDelete)
            db_session.commit()
            return redirect(url_for("myprofile"))
        elif "time_submit" in request.form:
            timeString = request.form["add-time"]
            timelist = timeString.split(" ")
            day_of_week = timelist[0]
            time = timelist[1]
            myUserID = db_session.query(User.id).where(User.username == session["username"]).first()[0]
            timeExist = db_session.query(Time).where((Time.day_of_week == day_of_week) & (Time.time == time)).first()
            if timeExist is None:
                db_session.add(Time(day_of_week, time))
                db_session.commit()
            currTimeID = db_session.query(Time.id).where((Time.day_of_week == day_of_week) & (Time.time == time)).first()[0]
            db_session.add(Availability(myUserID, currTimeID))
            db_session.commit()
            return redirect(url_for("myprofile"))
        elif "time_delete_submit" in request.form:
            timeString = request.form["delete-time"]
            timelist = timeString.split(" ")
            day_of_week = timelist[0]
            time = timelist[1]
            myUserID = db_session.query(User.id).where(User.username == session["username"]).first()[0]
            timeDeleteID = db_session.query(Time.id).where((Time.day_of_week == day_of_week) & (Time.time == time)).first()[0]
            if timeDeleteID is None:
                flash("This time was not added", "info")
                return redirect(url_for("addinfo"))
            AvailabilityToDelete = db_session.query(Availability).where((Availability.time_id == timeDeleteID) & (Availability.user_id == myUserID)).first()
            db_session.delete(AvailabilityToDelete)
            db_session.commit()
            return redirect(url_for("myprofile"))


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")  
        flash("You've been logged out", "info")
    return redirect(url_for("login"))


@app.before_first_request
def setup():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
