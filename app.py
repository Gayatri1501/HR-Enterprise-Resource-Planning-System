import os
import urllib

import MySQLdb.cursors
from flask import *
from flask import Flask, render_template,request,session,url_for,redirect,flash, send_file
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from io import BytesIO

from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='Static', static_url_path='/Static')
# Assuming you have a static folder for file uploads
UPLOAD_FOLDER = 'static/upload_img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'Pob'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'erp'
mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == "POST":
        username = request.form['txtusername']
        password = request.form['txtpass']

        # Check if the provided username and password match your database records
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM signup WHERE uname = %s AND pass = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            user_status = user[12]  # Assuming the status is the third column in the 'signup' table

            if user_status == "Active":
                session['username'] = username
                flash("You are logged in successfully!!")

                user_dict = {'uname': user[0], 'uimg': user[1]}  # Adjust indices based on actual table structure

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (username,))
                ulist = cur.fetchall()
                cur.close()

                return render_template('user_index.html', uname=username, user=user_dict, ulist=ulist, error=error)
            else:
                flash("Your account is not active. Please contact support.")
        else:
            flash("Invalid username or password")

    return render_template('login.html')


# @app.route('/login',methods=['GET', 'POST'])
# def login():
#     error = None
#
#     if request.method == "POST":
#         username = request.form['txtusername']
#         password = request.form['txtpass']
#         check = "Active"
#
#         # Check if the provided username and password match your database records
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM signup WHERE uname = %s AND pass = %s AND status = %s", (username, password,check))
#         user = cur.fetchone()
#         cur.close()
#
#         if user:
#             print(user)
#             session['username'] = username
#             flash("You are Login Successfully!!")
#
#             user_dict = {'uname': user[0], 'uimg': user[1]}
#
#             cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (username,))
#             # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
#             ulist = cur.fetchall()
#             cur.close()
#
#             return render_template('user_index.html', uname=username, user=user_dict, ulist=ulist, error=error)
#
#         else:
#             flash("Invalid username and password")
#             # return "Invalid username or password"
#
#     return render_template('login.html')


@app.route('/signup',methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == "POST":
        fullname = request.form['txtfullname']
        username = request.form['txtusername']
        email = request.form['txtemail']
        profile = request.form['ddlprofile']
        password = request.form['txtpass']
        userimage = request.files['file']

        if not username or not email or not password or not fullname:
            flash("Please fill in all required fields.")
        else:
            # Check if the username is already taken
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM signup WHERE uname = %s", (username,))
            count = cur.fetchone()[0]
            cur.close()

            if count > 0:
                flash("Username is already taken. Please choose a different one.")
            else:
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO signup (fname,uname, email, profile, pass,uimg) VALUES (%s, %s, %s,%s, %s, %s)",
                                (fullname, username, email, profile, password, userimage.filename,))
                    mysql.connection.commit()
                    cur.close()

                    userimage.save('Static/upload_img/' + userimage.filename)

                    flash("Signup successful!!")  # You can redirect to another page or show a success message.

    return render_template('signup.html')


@app.route('/user-index')
def userindex1():
    profile_uname = session.get('username')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
    # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
    ulist = cur.fetchall()
    cur.close()

    # Query the database to retrieve products for the logged-in user
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM task WHERE ename = %s", (profile_uname,))
    total_user = cur.fetchall()
    cur.close()

    total_u = len(total_user)

    # Query the database to retrieve products for the logged-in user
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(tstatus) as total_submit FROM task WHERE tstatus=%s AND ename = %s ",("Approved", profile_uname))
    total_sub = cur.fetchall()
    totalsubmit = total_sub[0]['total_submit']

    cur.execute("SELECT COUNT(tstatus) as total_submit FROM task WHERE tstatus=%s AND ename = %s ",("Pending", profile_uname))
    total_p = cur.fetchall()
    total_pending = total_p[0]['total_submit']

    cur.execute("SELECT COUNT(tstatus) as total_submit FROM task WHERE tstatus=%s AND ename = %s ",("Reject", profile_uname))
    total_i = cur.fetchall()
    total_in = total_i[0]['total_submit']

    cur.close()
    return render_template('user_index.html', profile_uname=profile_uname, total_u=total_u, totalsubmit=totalsubmit, total_pending=total_pending, total_in=total_in, ulist=ulist)

# @app.route('/1')
# def userindex():
#     return render_template('user_index.html')

@app.route('/user-profile')
def userprofile():
    profile_uname = session.get('username')

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup WHERE uname=%s", (profile_uname,))
        profilelist = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
        # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
        ulist = cur.fetchall()
        cur.close()

        return render_template('user_profile.html', profilelist=profilelist, uname=profile_uname, ulist=ulist)
    except Exception as e:
        return f"Error: {str(e)}"
    #return render_template('user_profile.html')


@app.route('/user-profile-update',methods=['GET', 'POST'])
def userprofileupdate():
    profile_uname = session.get('username')

    if request.method == 'POST':
        fullname = request.form['txtfullname']
        email = request.form['txtemail']
        username = request.form['txtusername']
        password = request.form['txtpassword']
        desg = request.form['ddldes']
        gender = request.form['rdgen']
        exp = request.form['txtexperience']
        salary = request.form['txtsalary']
        mobile = request.form['txtmobile']
        total = request.form['txttotal']
        imgpro = request.files['file']
        profile = request.form['ddlprofile']

        if 'update' in request.form:
            try:
                cur = mysql.connection.cursor()

                if imgpro:  # Check if an image is provided
                    # Save the image to a subdirectory within 'static'
                    image_filename = secure_filename(imgpro.filename)
                    image_path = os.path.join('static', 'upload_img', image_filename)
                    imgpro.save(image_path)

                    print("Image saved as:", image_path)  # Debugging statement

                    cur.execute(
                        "UPDATE signup SET fname=%s, email=%s, uname=%s, pass=%s, uimg=%s, mobile=%s, des=%s, exp=%s, salary=%s, gender=%s , totalpro=%s, profile=%s WHERE uname=%s",
                        (fullname,  email, username,password, imgpro, mobile, desg, exp, salary, gender, total, profile, profile_uname))

                    print("SQL Query executed")  # Debugging statement
                else:
                    cur.execute(
                        "UPDATE signup SET fname=%s, email=%s, uname=%s, pass=%s, mobile=%s, des=%s, exp=%s, salary=%s, gender=%s , totalpro=%s, profile=%s WHERE uname=%s",
                        (fullname,  email, username, password, mobile, desg, exp, salary, gender, total,profile, profile_uname))

                mysql.connection.commit()
                cur.close()
                flash("Profile updated successfully")

            except Exception as e:
                return f"Error: {str(e)}"


        elif 'delete' in request.form:
            try:
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM signup WHERE uname = %s", (profile_uname,))
                mysql.connection.commit()
                cur.close()
                flash(" Profile Deleted successfully")
            except Exception as e:
                return f"Error: {str(e)}"

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup WHERE uname=%s", (profile_uname,))
        profilelist = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
        # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
        ulist = cur.fetchall()
        cur.close()

        return render_template('user_profile_update.html', profilelist=profilelist, uname=profile_uname, ulist=ulist)
    except Exception as e:
        return f"Error: {str(e)}"

    #return render_template('user_profile_update.html')

@app.route('/user-task-view')
def usertaskview():
    profile_uname = session.get('username')

    try:
        # Store the tid value in the session
        # session['tid_value'] = tid

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup WHERE uname=%s", (profile_uname,))
        profilelist = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
        # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
        ulist = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM task WHERE FIND_IN_SET(%s, tsend)", (profile_uname,))
        tasklist = cur.fetchall()
        cur.close()

        # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cur.execute("SELECT * FROM task WHERE tsend=%s", (profile_uname,))
        # tasklist = cur.fetchall()
        # cur.close()

        return render_template('user_task_view.html',tasklist=tasklist , profilelist=profilelist, uname=profile_uname, ulist=ulist)
    except Exception as e:
        return f"Error: {str(e)}"




@app.route('/user-task-update', methods=['GET', 'POST'])
def usertaskedit():
    tid_value = request.args.get('tid')
    profile_uname = session.get('username')

    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
    ulist = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM task WHERE tid=%s", (tid_value,))
    tasklist = cur.fetchall()
    cur.close()

    error = None
    if request.method == "POST":
        taskfile = request.files['file']
        status = request.form['ddlstatus']

        if 'update' in request.form:
            try:
                cur = mysql.connection.cursor()

                if taskfile:  # Check if an image is provided
                    # Save the image to the upload folder
                    task_filename = secure_filename(taskfile.filename)
                    task_path=task_filename
                    # task_path = os.path.join(app.config['UPLOAD_FOLDER'], task_filename)
                    taskfile.save(task_path)

                    print("Image saved as:", task_path)  # Debugging statement
                    cur.execute("UPDATE task SET tstatus=%s, tupload=%s WHERE tid = %s", (status, task_path, tid_value))

                    print("SQL Query executed")  # Debugging statement
                else:
                    cur.execute("UPDATE task SET tstatus=%s WHERE tid = %s", (status, tid_value))

                mysql.connection.commit()
                cur.close()
                flash("Task Status updated successfully")

            except Exception as e:
                return f"Error: {str(e)}"

    return render_template('user_task_edit.html', date=x, ulist=ulist, tasklist=tasklist, uname=profile_uname)



@app.route('/user-status-view')
def userstatusview():
    profile_uname = session.get('username')
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM task WHERE ename=%s", (profile_uname,))
        tasklist = cur.fetchall()
        cur.close()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
        # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
        ulist = cur.fetchall()
        cur.close()

        return render_template('user_task_status.html',tasklist=tasklist, ulist=ulist )
    except Exception as e:
        return f"Error: {str(e)}"

#--------------------------------------------------------------------------------------

@app.route('/admin-index')
def adminindex():
    # Query the database to retrieve products for the logged-in user
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM task ")
    total_user = cur.fetchall()
    cur.close()

    total_u = len(total_user)

    # Query the database to retrieve products for the logged-in user
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(tstatus) as total_submit FROM task WHERE tstatus=%s ",("Approved",))
    total_sub = cur.fetchall()
    totalsubmit = total_sub[0]['total_submit']

    cur.execute("SELECT COUNT(profile) as total_submit FROM signup WHERE profile=%s ",("Employee",))
    total_p = cur.fetchall()
    total_pending = total_p[0]['total_submit']
    #total_pending = len(total_p)

    cur.execute("SELECT COUNT(profile) as total_submit FROM signup WHERE profile=%s ", ("Interns",))
    total_interns = cur.fetchall()
    total_in = total_interns[0]['total_submit']
    # total_pending = len(total_p)

    # cur.execute("SELECT COUNT(tstatus) as total_submit FROM task WHERE tstatus=%s ",("In Progress",))
    # total_i = cur.fetchall()
    # total_in = len(total_i)

    return render_template('admin_index.html', total_u=total_u, totalsubmit=totalsubmit, total_pending=total_pending, total_in=total_in)


@app.route('/admin-login',methods=['GET', 'POST'])
def adminlogin():
    error = None

    if request.method == "POST":
        username = request.form['txtusername']
        password = request.form['txtpass']


        if (username=='admin' and password=='star' ):
            session['username'] = username
            flash("You are Login Successfully!!")

            return redirect('/admin-index')

        else:
            error = "Invalid username and password"
            # return "Invalid username or password"

    return render_template('admin_login.html')


@app.route('/admin-view-emp')
def adminviewemp():

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup ")
        profilelist = cur.fetchall()
        cur.close()


        return render_template('admin_view_emp.html', profilelist=profilelist, )
    except Exception as e:
        return f"Error: {str(e)}"
    #return render_template('user_profile.html')

@app.route('/admin-delete-user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM music WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash("Music deleted successfully")
        return redirect(url_for('adminviewsong'))

    except Exception as e:
        return f"Error: {str(e)}"


import datetime
@app.route('/admin-add-task',methods=['GET', 'POST'])
def adminaddtask():
    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT uname, profile FROM signup ")
    profilelist = cur.fetchall()
    cur.close()

    error = None
    if request.method == "POST":
        profile = request.form['ddlprofile']
        interns_list = request.form.getlist('interns[]')
        send = ', '.join(interns_list)
        taskname = request.form['txtname']
        des = request.form['txtdes']
        ldate = request.form['txtldate']
        ltime = request.form['txttime']
        cdate = request.form['txtsdate']



        cur = mysql.connection.cursor()

        for intern in interns_list:
            cur.execute("INSERT INTO task (tprofile, tsend, tname, tdes, tldate, tltime, ttdate) VALUES ( %s, %s,%s, %s, %s, %s, %s)",
                        (profile, intern, taskname, des, ldate, ltime, cdate))
            mysql.connection.commit()
        cur.close()


        flash("Admin Task Add successful!!")  # You can redirect to another page or show a success message.

    return render_template('admin_add_task.html', date=x, profilelist=profilelist)



@app.route('/admin-add-task-interns', methods=['GET', 'POST'])
def adminaddtaskinterns():
    profile_uname = session.get('username')
    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT uname, profile FROM signup ")
    profilelist = cur.fetchall()
    cur.close()

    if request.method == "POST":
        profile = request.form['ddlprofile']
        send = request.form['ddluser'] if profile == 'Employee' else None
        taskname = request.form['txtname']
        des = request.form['txtdes']
        ldate = request.form['txtldate']
        ltime = request.form['txttime']
        cdate = request.form['txtsdate']
        ename = profile_uname

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO task (tprofile, tsend, tname, tdes, tldate, tltime, ttdate, ename) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (profile, send, taskname, des, ldate, ltime, cdate, ename))
            mysql.connection.commit()
            cur.close()
            flash("Employee Leave Application Sent successfully!!")
        except Exception as e:
            flash(f"Error: {str(e)}")

    return render_template('admin_add_task_intern.html', date=x, profilelist=profilelist, uname=profile_uname)




@app.route('/admin-task-view',methods=['GET', 'POST'])
def admintaskview():


    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM task ")
        tasklist = cur.fetchall()
        cur.close()

        return render_template('admin_task_view.html',tasklist=tasklist )
    except Exception as e:
        return f"Error: {str(e)}"


import datetime
@app.route('/admin-task-update', methods=['GET', 'POST'])
def admintaskedit():
    tid_value = request.args.get('tid')
    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM task WHERE tid=%s", (tid_value,))
    tasklist = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT uname FROM signup")
    profilelist = cur.fetchall()
    cur.close()

    # Set a default value for filename
    filename = "default_filename.png"

    if request.method == "POST":
        sug = request.form['txtsug']
        status = request.form['ddlstatus']

        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE task SET tstatus=%s, tsug=%s WHERE tid = %s", (status, sug, tid_value))
            mysql.connection.commit()
            cur.close()

            flash("Admin Task Edit successful!", "success")
            # return redirect(url_for('admin_dashboard'))  # Redirect to another page after a successful update

        except Exception as e:
            flash(f"Error: {str(e)}", "error")

    # # Extract the filename from the first dictionary in the list
    # if tasklist and 'tupload' in tasklist[0]:
    #     # Decode the bytes-like object to a string
    #     filename = tasklist[0]['tupload'].decode('utf-8').split("'")[1]

    # Pass the filename to the template
    return render_template('admin_task_update.html', date=x, tasklist=tasklist, profilelist=profilelist, filename=filename)




@app.route('/admin-status-view')
def adminstatusview():

    try:

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM task ")
        tasklist = cur.fetchall()
        cur.close()

        return render_template('admn_task_status.html',tasklist=tasklist )
    except Exception as e:
        return f"Error: {str(e)}"



import matplotlib.pyplot as plt
import numpy as np
import io
import base64

@app.route('/admin-view-user-profile', methods=['GET', 'POST'])
def adminviewuserprofile():

    username_name = request.args.get('uname')

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup WHERE uname=%s", (username_name,))
        profilelist = cur.fetchall()
        cur.close()

        if request.method == 'POST':
            # Check if the "View Progress Report" button is clicked
            if 'view_progress_report' in request.form:
                try:
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT tstatus FROM task WHERE tsend=%s", (username_name,))
                    tasklist = cur.fetchall()
                    cur.close()

                    flash("Progress report is being generated. Please wait a moment.")
                    # Calculate the counts for each status
                    status_counts = {'Submit': 0, 'Pending': 0, 'Progress': 0, '':0}
                    for task in tasklist:
                        status_counts[task['tstatus']] += 1

                    # Create a pie chart
                    labels = list(status_counts.keys())
                    sizes = list(status_counts.values())

                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                    # Save the plot to a bytes buffer
                    buffer = io.BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)

                    # Encode the bytes buffer to base64
                    plot_data = base64.b64encode(buffer.getvalue()).decode()

                    return render_template('admin_view_emp_profile.html', profilelist=profilelist, plot_data=plot_data)

                except Exception as e:
                    flash(f"Error: {str(e)}")

        return render_template('admin_view_emp_profile.html', profilelist=profilelist)

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/admin-view-emp-ud')
def adminviewempud():

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup ")
        profilelist = cur.fetchall()
        cur.close()


        return render_template('admin_view_emp_update.html', profilelist=profilelist, )
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/admin-update-profile', methods=['GET', 'POST'])
def adminupdateuserprofile():
    username_value = request.args.get('uname')

    if request.method == 'POST':
        fullname = request.form['txtfullname']
        email = request.form['txtemail']
        username = request.form['txtusername']
        password = request.form['txtpassword']
        desg = request.form['ddldes']
        gender = request.form['rdgen']
        exp = request.form['txtexperience']
        salary = request.form['txtsalary']
        mobile = request.form['txtmobile']
        total = request.form['txttotal']
        imgpro = request.files['file']
        profile = request.form['ddlprofile']

        if 'update' in request.form:
            try:
                cur = mysql.connection.cursor()

                if imgpro:  # Check if an image is provided
                    # Save the image to a subdirectory within 'static'
                    image_filename = secure_filename(imgpro.filename)
                    image_path = os.path.join('static', 'upload_img', image_filename)
                    imgpro.save(image_path)

                    print("Image saved as:", image_path)  # Debugging statement

                    cur.execute(
                        "UPDATE signup SET fname=%s, email=%s, uname=%s, pass=%s, uimg=%s, mobile=%s, des=%s, exp=%s, salary=%s, gender=%s , totalpro=%s, profile=%s WHERE uname=%s",
                        (fullname, email, username, password, imgpro, mobile, desg, exp, salary, gender, total, profile,
                         username_value))

                    print("SQL Query executed")  # Debugging statement
                else:
                    cur.execute(
                        "UPDATE signup SET fname=%s, email=%s, uname=%s, pass=%s, mobile=%s, des=%s, exp=%s, salary=%s, gender=%s , totalpro=%s, profile=%s WHERE uname=%s",
                        (fullname, email, username, password, mobile, desg, exp, salary, gender, total, profile,
                         username_value))

                mysql.connection.commit()
                cur.close()
                flash("Admin Employee updated successfully")

            except Exception as e:
                return f"Error: {str(e)}"


        elif 'delete' in request.form:
            try:
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM signup WHERE uname = %s", (username_value,))
                mysql.connection.commit()
                cur.close()
                flash("Employee Deleted successfully")
            except Exception as e:
                return f"Error: {str(e)}"

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup WHERE uname=%s", (username_value,))
        profilelist = cur.fetchall()
        cur.close()

        # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cur.execute("SELECT uname, uimg FROM signup WHERE uname=%s", (profile_uname,))
        # # cur.execute("SELECT * FROM signup WHERE uname=%s", (uname,))
        # ulist = cur.fetchall()
        # cur.close()

        return render_template('admin_edit_emp.html', profilelist=profilelist,)
    except Exception as e:
        return f"Error: {str(e)}"


from flask import send_from_directory

# Constant file path
UPLOAD_FOLDER = "static/upload_img/"

@app.route('/download_file/<filename>')
def download_file(filename):
    # file_path = UPLOAD_FOLDER + filename
    file_path = filename
    return send_file(file_path, as_attachment=True)


@app.route('/admin-status-emp')
def adminstatusemp():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM signup ")
        profilelist = cur.fetchall()
        cur.close()

        return render_template('admin_emp_status.html', profilelist=profilelist, )
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/admin/request/active/<uname>', methods=['GET', 'POST'])
def update_status_a(uname):
    # uname = request.args.get('uname')
    print(uname)
    try:
        # Update the status of the road request in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE signup SET status = %s WHERE uname = %s", ("Active", uname))  # Note: using 3 instead of "3" as it's an integer
        mysql.connection.commit()
        cur.close()

        # Redirect back to the admin dashboard page after updating
        return redirect(url_for('adminstatusemp'))
    except Exception as e:
        # Handle any potential errors
        return str(e), 500  # Returning the error message with status code 500

@app.route('/admin/request/Inactive/<uname>', methods=['GET', 'POST'])
def update_status_i(uname):
    # uname = request.args.get('uname')
    try:
        # Update the status of the user in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE signup SET status = %s WHERE uname = %s", ("Inactive", uname))
        mysql.connection.commit()
        cur.close()

        # Redirect back to the admin dashboard page after updating
        return redirect(url_for('adminstatusemp'))
    except Exception as e:
        # Handle any potential errors
        return str(e), 500  # Returning the error message with status code 500




if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development