import io
import os
import hashlib
import sqlite3 as sql3
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, flash, render_template as render, request, url_for, redirect, session
from flask_humanize import Humanize
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from os.path import join
from PIL import Image
from tools.private import private_keys, decrypting_key
from instance.dbs import *


# ************** CONFIG APP STATIC FOLDER & SECRET_KEY *************
app = Flask(__name__, static_url_path='/static')
humanize = Humanize(app)
moment = Moment(app)
sec_config = private_keys()
app.secret_key = sec_config['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.path.join('static/images/')
app.config['DEBUG'] = sec_config['FLASK_DEBUG']
# host = sec_config['HOST']
# port = sec_config['PORT']
host = sec_config['HOST_TEST']
port = sec_config['PORT_TEST']

# ************** db *************
app.permanent_session_lifetime = timedelta(days=1)


# ************** HOME *************
@app.route("/")
def home():
    try:
        getUserInfo = personalData()
    except:
        return redirect(url_for('loadFile'))

    return render("home.html", title="Home", getUserInfo=getUserInfo)


# ************** EXPERIENCE *************
@app.route("/experience")
def experience():
    sklls = []
    experienceAll = []
    getUserInfo = personalData()
    conn = db_conn()
    getExperience = conn.execute("SELECT * FROM Experience").fetchall()
    conn.close()

    for item in getExperience:
        it = item[3].split("', '")
        for i in it:
            x = i.split(", ")
            for d in x:
                sklls.append(d)
        getExperience[3] = x
        experien = [item[0], item[1], item[2], x, item[4], item[5], item[6], item[7]]
        experienceAll.append(experien)

    return render("dashboard/experience/experience.html", title="Experience", getUserInfo=getUserInfo, experienceAll=experienceAll)


@app.route("/createExperience", methods=["POST", "GET"])
def createExperience():
    getUserInfo = personalData()
    if request.method == "POST":
        company = request.form['company']
        job = request.form['job']
        description = request.form['description']
        sk = request.form['skills']
        datein = request.form['datein']
        dateout = request.form['dateout']
        city = request.form['city']
        state = request.form['state']
        contry = request.form['contry']
        skills = str(sk.split(', '))
        datein = datetime.strptime(datein, '%Y-%m-%d').date()
        datein = datein.strftime('%B %d, %Y')
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Experience (company, job, description, skills, datein, dateout, city, state, contry)")
            conn.commit()
            conn.execute("INSERT INTO Experience (company, job, description, skills, datein, dateout, city, state, contry) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (company, job, description, skills, datein, dateout, city, state, contry))
            conn.commit()
            conn.close()
            return redirect(url_for('experience'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Experience (company, job, description, skills, datein, dateout, city, state, contry) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (company, job, description, skills, datein, dateout, city, state, contry))
            conn.commit()
            conn.close()
            return redirect(url_for('experience'))

    return render("dashboard/experience/create_experience.html", title="Experience", getUserInfo=getUserInfo)


# ************** EDUCATION *************
@app.route("/education")
def education():
    getUserInfo = personalData()
    conn = db_conn()
    getEducation = conn.execute("SELECT * FROM Education").fetchall()

    getCourse = conn.execute("SELECT * FROM Courses").fetchall()
    conn.close()

    return render("dashboard/education/education.html", title="Education", getUserInfo=getUserInfo, getEducation=getEducation, getCourse=getCourse)


@app.route("/createEducation", methods=["POST", "GET"])
def createEducation():
    getUserInfo = personalData()
    if request.method == "POST":
        institute = request.form['institute']
        title = request.form['title']
        description = request.form['description']
        datein = request.form['datein']
        dateout = request.form['dateout']
        city = request.form['city']
        state = request.form['state']
        contry = request.form['contry']
        datein = datetime.strptime(datein, '%Y-%m-%d').date()
        datein = datein.strftime('%B %d, %Y')
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Education (institute, title, description, datein, dateout, city, state, contry)")
            conn.commit()
            conn.execute("INSERT INTO Education (institute, title, description, datein, dateout, city, state, contry) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (institute, title, description, datein, dateout, city, state, contry))
            conn.commit()
            getEducation = conn.execute("SELECT * FROM Education").fetchall()
            conn.close()
            return redirect(url_for('education'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Education (institute, title, description, datein, dateout, city, state, contry) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (institute, title, description, datein, dateout, city, state, contry))
            conn.commit()
            getEducation = conn.execute("SELECT * FROM Education").fetchall()
            conn.close()
            return redirect(url_for('education'))
    return render("dashboard/education/create_education.html", title="Education", getUserInfo=getUserInfo)


@app.route("/createCourse", methods=["POST", "GET"])
def createCourse():
    getUserInfo = personalData()
    if request.method == "POST":
        institute = request.form['institute']
        title = request.form['title']
        duration = request.form['duration']
        dateout = request.form['dateout']
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Course (institute, title, duration, dateout)")
            conn.commit()
            conn.execute("INSERT INTO Course (institute, title, duration, dateout) VALUES (?, ?, ?, ?)", (institute, title, duration, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('education'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Course (institute, title, duration, dateout) VALUES (?, ?, ?, ?)", (institute, title, duration, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('education'))
    return render("dashboard/education/create_course.html", title="Education", getUserInfo=getUserInfo)


# ************** PROJECTS *************
@app.route("/project")
def project():
    getUserInfo = personalData()
    conn = db_conn()
    getProjects = conn.execute("SELECT * FROM Projects").fetchall()
    conn.close()

    return render("dashboard/project/project.html", title="Projects", getUserInfo=getUserInfo, getProjects=getProjects)


@app.route("/createProject", methods=["POST", "GET"])
def createProject():
    getUserInfo = personalData()
    if request.method == "POST":
        project = request.form['project']
        lenguaje = request.form['lenguaje']
        description = request.form['description']
        remarks = request.form['remarks']
        deploy = request.form['deploy']
        status = request.form['status']
        dateout = request.form['dateout']
        video = request.form['video']
        link = request.form['link']
        github = request.form['github']
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Project (project, lenguaje, description, remarks, deploy, status, dateout, video, link, github)")
            conn.commit()
            conn.execute("INSERT INTO Project (project, lenguaje, description, remarks, deploy, status, dateout, video, link, github) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (project, lenguaje, description, remarks, deploy, status, dateout, video, link, github))
            conn.commit()
            conn.close()
            return redirect(url_for('project'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Project (project, lenguaje, description, remarks, deploy, status, dateout, video, link, github) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (project, lenguaje, description, remarks, deploy, status, dateout, video, link, github))
            conn.commit()
            conn.close()
            return redirect(url_for('project'))
    return render("dashboard/project/create_project.html", title="Project", getUserInfo=getUserInfo)


# ************** SKILLS *************
@app.route("/skills")
def skills():
    getUserInfo = personalData()
    conn = db_conn()
    getSkills = conn.execute("SELECT * FROM Skills").fetchall()
    conn.close()

    return render("dashboard/skills/skills.html", title="Skills", getUserInfo=getUserInfo, getSkills=getSkills)


@app.route("/createSkill", methods=["POST", "GET"])
def createSkill():
    getUserInfo = personalData()
    if request.method == "POST":
        skill = request.form['skill']
        category = request.form['category']
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Skills (skill, category)")
            conn.commit()
            conn.execute("INSERT INTO Skills (skill, category) VALUES (?, ?)", (skill, category))
            conn.commit()
            conn.close()
            return redirect(url_for('skills'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Skills (skill, category) VALUES (?, ?)", (skill, category))
            conn.commit()
            conn.close()
            return redirect(url_for('skills'))
    return render("dashboard/skills/create_skills.html", title="Skills", getUserInfo=getUserInfo)


# ************** AWARD *************
@app.route("/awards")
def awards():
    getUserInfo = personalData()
    conn = db_conn()
    getAwards = conn.execute("SELECT * FROM Awards").fetchall()
    conn.close()

    return render("dashboard/awards/awards.html", title="Awards", getUserInfo=getUserInfo, getAwards=getAwards)


@app.route("/createAward", methods=["POST", "GET"])
def createAward():
    getUserInfo = personalData()
    if request.method == "POST":
        institution = request.form['institution']
        award = request.form['award']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        dateout = request.form['dateout']
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Awards (institution, award, city, state, country, dateout)")
            conn.commit()
            conn.execute("INSERT INTO Awards (institution, award, city, state, country, dateout) VALUES (?, ?, ?, ?, ?, ?)", (institution, award, city, state, country, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('awards'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Awards (institution, award, city, state, country, dateout) VALUES (?, ?, ?, ?, ?, ?)", (institution, award, city, state, country, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('awards'))
    return render("dashboard/awards/create_award.html", title="Awards", getUserInfo=getUserInfo)


# ************** ACHIVEMENTS *************
@app.route("/achivements")
def achivements():
    getUserInfo = personalData()
    conn = db_conn()
    getAchivements = conn.execute("SELECT * FROM Achivements").fetchall()
    conn.close()

    return render("dashboard/achivements/achivements.html", title="Achivements", getUserInfo=getUserInfo, getAchivements=getAchivements)


@app.route("/createAchivement", methods=["POST", "GET"])
def createAchivement():
    getUserInfo = personalData()
    if request.method == "POST":
        institution = request.form['institution']
        event = request.form['event']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        dateout = request.form['dateout']
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Achivements (institution, event, city, state, country, dateout)")
            conn.commit()
            conn.execute("INSERT INTO Achivements (institution, event, city, state, country, dateout) VALUES (?, ?, ?, ?, ?, ?)", (institution, event, city, state, country, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('achivements'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Achivements (institution, event, city, state, country, dateout) VALUES (?, ?, ?, ?, ?, ?)", (institution, event, city, state, country, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('achivements'))
    return render("dashboard/achivements/create_achivements.html", title="Achivements", getUserInfo=getUserInfo)


# ************** CERTIFICATIONS *************
@app.route("/certifications")
def certifications():
    getUserInfo = personalData()
    conn = db_conn()
    getCertifications = conn.execute("SELECT * FROM Certifications").fetchall()
    conn.close()

    return render("dashboard/certifications/certifications.html", title="Certifications", getUserInfo=getUserInfo, getCertifications=getCertifications)


@app.route("/createCertification", methods=["POST", "GET"])
def createCertification():
    getUserInfo = personalData()
    if request.method == "POST":
        institution = request.form['institution']
        description = request.form['description']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        dateout = request.form['dateout']
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Certifications (institution, description, city, state, country, dateout)")
            conn.commit()
            conn.execute("INSERT INTO Certifications (institution, description, city, state, country, dateout) VALUES (?, ?, ?, ?, ?, ?)", (institution, description, city, state, country, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('certifications'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Certifications (institution, description, city, state, country, dateout) VALUES (?, ?, ?, ?, ?, ?)", (institution, description, city, state, country, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('certifications'))
    return render("dashboard/certifications/create_certification.html", title="Volunteer", getUserInfo=getUserInfo)


# ************** VOLUNTEERING *************
@app.route("/volunteer")
def volunteer():
    getUserInfo = personalData()
    conn = db_conn()
    getVolunteer = conn.execute("SELECT * FROM Volunteering").fetchall()
    conn.close()

    return render("dashboard/volunteer/volunteer.html", title="Volunteer", getUserInfo=getUserInfo, getVolunteer=getVolunteer)


@app.route("/createVolunteer", methods=["POST", "GET"])
def createVolunteer():
    getUserInfo = personalData()
    if request.method == "POST":
        institution = request.form['institution']
        description = request.form['description']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        datein = request.form['datein']
        dateout = request.form['dateout']
        datein = datetime.strptime(datein, '%Y-%m-%d').date()
        datein = datein.strftime('%B %d, %Y')
        dateout = datetime.strptime(dateout, '%Y-%m-%d').date()
        dateout = dateout.strftime('%B %d, %Y')
        try:
            conn = db_conn()
            conn.execute("CREATE TABLE Volunteer (institution, description, city, state, country, datein, dateout)")
            conn.commit()
            conn.execute("INSERT INTO Volunteer (institution, description, city, state, country, datein, dateout) VALUES (?, ?, ?, ?, ?, ?, ?)", (institution, description, city, state, country, datein, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('volunteer'))
        except:
            conn = db_conn()
            conn.execute("INSERT INTO Volunteer (institution, description, city, state, country, datein, dateout) VALUES (?, ?, ?, ?, ?, ?, ?)", (institution, description, city, state, country, datein, dateout))
            conn.commit()
            conn.close()
            return redirect(url_for('volunteer'))
    return render("dashboard/volunteer/create_volunteer.html", title="Volunteer", getUserInfo=getUserInfo)


# ************** USER *************
@app.route('/enter', methods=['POST', 'GET']) 
def enter():
    getUserInfo = personalData()
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        try:
            conn = db_conn()
            getUser = conn.execute("SELECT * FROM users WHERE email =?", (email,)).fetchone()
            conn.commit()
            conn.close()
            
            if getUser[1] == passwordHash:
                session['user'] = getUser[0]
                session['loged'] = "Yes"
                return redirect(url_for('dashboard'))
            else:
                flash('Something went wrong, try again!')
                return render("userLog/enter.html", title="Volunteer", getUserInfo=getUserInfo)
        except:
            session['user'] = ""
            session['loged'] = "No"
            flash('Record not found, Register or try again!')
            return render("userLog/add_user.html", title="Volunteer", getUserInfo=getUserInfo)

    return render("userLog/enter.html", title="Login", getUserInfo=getUserInfo)


@app.route('/loadFile', methods=["POST", "GET"]) 
def loadFile():
    getUserInfo = personalData()
    if request.method == "POST":
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2:
            try:
                email = request.form['email']
                passwordHash = hashlib.sha256(password.encode()).hexdigest()
                conn = db_conn()
                conn.execute("CREATE TABLE users (email, passwordHash)")
                conn.commit()
                conn.execute("INSERT INTO users (email, passwordHash) VALUES (?, ?)", (email, passwordHash))
                conn.commit()
                conn.close()
            except:
                pass

            fileinn = request.files.get("fileinn")
            dfSheets = pd.ExcelFile(fileinn).sheet_names
            for sheet in dfSheets:
                if sheet != "keys":
                    df = pd.read_excel(fileinn, sheet)
                    df.to_sql(name=sheet, con=conn, if_exists="append", index=False)

            session['user'] = email
            session['loged'] = "Yes"
            flash('The register was successful and you are login to!')
            return redirect(url_for('dashboard'))
        else:
            flash('The passwords are not the same, try again!')
            return redirect(url_for('loadFile'))

    return render("userLog/loadFile.html")


@app.route("/logout") 
def logout():
    flash("You have been logged out", "info")
    session['user'] = ""
    session['loged'] = "No"
    return redirect(url_for('home'))


@app.route("/dashboard")
def dashboard():
    getUserInfo = personalData()
    if session['loged'] == "Yes":

        conn = db_conn()
        conn.row_factory = sql3.Row
        getExperience = conn.execute("SELECT * FROM Experience").fetchall()

        conn.row_factory = sql3.Row
        getEducation = conn.execute("SELECT * FROM Education").fetchall()

        conn.row_factory = sql3.Row
        getCourse = conn.execute("SELECT * FROM Courses").fetchall()

        conn.row_factory = sql3.Row
        getProjects = conn.execute("SELECT * FROM Projects").fetchall()

        conn.row_factory = sql3.Row
        getSkills = conn.execute("SELECT * FROM Skills").fetchall()

        conn.row_factory = sql3.Row
        getAwards = conn.execute("SELECT * FROM Awards").fetchall()

        conn.row_factory = sql3.Row
        getAchivements = conn.execute("SELECT * FROM Achivements").fetchall()

        conn.row_factory = sql3.Row
        getCertifications = conn.execute("SELECT * FROM Certifications").fetchall()

        conn.row_factory = sql3.Row
        getVolunteer = conn.execute("SELECT * FROM Volunteering").fetchall()

        conn.close()

        return render("dashboard.html", title="Dashboard", loged=session['loged'], getUserInfo=getUserInfo, 
                        getExperience=getExperience, getEducation=getEducation, getCourse=getCourse, 
                        getProjects=getProjects, getSkills=getSkills, getAwards=getAwards, 
                        getAchivements=getAchivements, getCertifications=getCertifications, getVolunteer=getVolunteer)

    else:
        flash('You are not authorized to enter!')
        return redirect(url_for('home'))


def personalData():
    conn = db_conn()
    getUserInfo = conn.execute("SELECT * FROM usersInfo").fetchone()
    conn.commit()
    conn.close()
    return getUserInfo


if __name__ == '__main__':
    app.run(host, port)
