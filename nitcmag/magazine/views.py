from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection


# Create your views here.

def redirect_modules(role):
    if role==1:
        return redirect('../admin_module')
    if role==2:
        return redirect('../reviewer_module')

def home(request):
    if request.session.has_key('user'):
    #Deleting session variable
        del request.session['user']
    return render(request,'index.html')

def login(request):
    dict2 = {'admin':1,'reviewer':2}
    dict1={'name':'','password':'','role':''}
    if request.method=="POST":
        dict1=request.POST
        cursor =  connection.cursor()
        query = "select password,r_id from magazine_login_cred where u_id = '{}'"
        query = query.format(dict1['name'])
        cursor.execute(query)
        y = cursor.fetchall()
        if (len(y)!=0):
            #checking if password and role id matches with username
            if (y[0][0]==dict1['password'] and y[0][1]==dict2[dict1['role']]):
                role = dict2[dict1['role']]
                request.session['user'] = [dict1['name'],role]
                return redirect_modules(role)
            else:
                return render(request, "login.html",{'error':"Wrong credentials or user doesn't exist"})
        else:
            return render(request, "login.html",{'error':"Wrong credentials or user doesn't exist"})  
    elif request.session.has_key('user'):
        role = request.session['user'][1]
        return redirect_modules(role)
    return render(request,"login.html")

def change_password(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if request.method=="POST":
            entered_details = request.POST
            for i in entered_details.values():
                if i=='':
                    return render(request, "change_password.html",{'error':'Kindly enter all values.'})
            if (entered_details['n_pass'] != entered_details['re_n_pass']):
                return render(request, "change_password.html",{'error':"Passwords doesn't match."})
            if (entered_details['c_pass'] == entered_details['re_n_pass'] == entered_details['n_pass']):
                return render(request, "change_password.html",{'error':"New password cannot be same as old password."})
            get_password_query = "select password from magazine_login_cred where u_id = '{}'"
            get_password_query = get_password_query.format(user_details[0])
            cursor = connection.cursor()
            cursor.execute(get_password_query)
            y = cursor.fetchall()
            if y[0][0] != entered_details['c_pass']:
                return render(request, "change_password.html",{'error':"Password incorrect."})
            else:
                change_password_query = "update magazine_login_cred set password='{}' where u_id='{}'"
                change_password_query = change_password_query.format(entered_details['n_pass'],user_details[0])
                cursor.execute(change_password_query)
                return render(request, "change_password_1.html")
        return render(request,'change_password.html')
    else:
        return redirect("../login")

"***************************************************************************************************************"

def admin_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"admin_module.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def appoint_reviewer(request):
    return render(request,"admin_dash_base.html")

def remove_reviewer(request):
    return render(request,"admin_dash_base.html")
    

def view_assigned_articles(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"admin_dash_base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def send_for_review(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"admin_dash_base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def view_pending_articles(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"admin_dash_base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def view_reviewed_articles(request):
    # select articles from this, give publish option
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"admin_dash_base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

"***************************************************************************************************************"

def reviewer_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"reviewer_module.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def reviewed_articles_reviewer(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"reviewer_dash_base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def pending_articles_reviewer(request):
    #review article option
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"reviewer_dash_base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")


"***************************************************************************************************************"

def published_article(request, article_id):
    cursor = connection.cursor()
    query = "select title,author,content,name from article, reviewer where article_id = {} and article.reviewer_id = reviewer.reviewer_id;"
    query = query.format(article_id)
    cursor.execute(query)
    article = cursor.fetchall()[0]
    details = {'title' : article[0], 'author' : article[1], 'content' : article[2], 'reviewer' : article[3]}
    return render(request,"published_article.html",details)


def admin_article(request,article_id):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            cursor = connection.cursor()
            query = "select title,author,content,status,reviewer,rating from article where article_id = {};"
            query = query.format(article_id)
            cursor.execute(query)
            article = cursor.fetchall()[0]
            details = {'title' : article[0], 'author' : article[1], 'content' : article[2], 'status': article[3]}
            if details['status'] == 1 :
                query = "select name from reviewer;"
                cursor.execute(query)
                reviewers = cursor.fetchall()
                details['reviewers' : reviewers]
            else:
                details['reviewer'] = article[4]
                if details['status'] >= 3:
                    details['rating'] = article[5]
            return render(request,"admin_article.html",details)
        else:
            return redirect("../login.html")
    else:
        return redirect("../login.html")


def reviewer_artcile(request,article_id):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            cursor = connection.cursor()
            query = "select title,author,content,status,rating from article, reviewer where article_id = {};"
            query = query.format(article_id)
            cursor.execute(query)
            article = cursor.fetchall()[0]
            details = {'title' : article[0], 'author' : article[1], 'content' : article[2], 'status' : article[3]}
            if details['status'] >= 3:
                details['rating'] = article[4]
            return render(request,"reviewer_article.html",details)
        else:
            return redirect("../login.html")
    else:
        return redirect("../login.html")


"***************************************************************************************************************"

def view_magazine(request):
    return render(request,'magazine.html')

def send_for_review(a_id,r_id):
    cursor =  connection.cursor()


    query="update article set reviewer_id={},status=2 where article_id={}"
    query=query.format(r_id,a_id)
    cursor.execute(query)


def give_rating(a_id,rating):
    cursor =  connection.cursor()


    if(rating>10):
        return -1
    else:
        query="update article set rating={},status=3 where article_id={}"
        query=query.format(rating,a_id)
        cursor.execute(query)


def publish(a_id):
    cursor =  connection.cursor()


    query="update article set status=4 where article_id={}"
    query=query.format(a_id)
    cursor.execute(query)


def get_articles_list(status):
    cursor =  connection.cursor()


    query="select * from article where status={}"
    query=query.format(status)
    cursor.execute(query)
    y=cursor.fetchall()
    return y


def get_article(a_id):
    cursor =  connection.cursor()


    query="select * from article where article_id={}"
    query=query.format(a_id)
    cursor.execute(query)
    y=cursor.fetchall()
    return y


def get_reviewer_articles(r_id,status):
    cursor =  connection.cursor()


    query="select * from article where status={},reviewer_id={}"
    query=query.format(status,r_id)
    cursor.execute(query)
    y=cursor.fetchall()
    return y


def add_new_post(title,author,content):
    cursor =  connection.cursor()


    query="select * from article"
    cursor.execute(query)
    y=cursor.fetchall()
    a_id=len(y)+1


    query="INSERT INTO article  VALUES ({},{},{},{},NULL,1,NULL);"
    query=query.format(a_id,title,author,content)
    cursor.execute(query)


def get_reviewer_name(r_id):
    cursor =  connection.cursor()


    query="select * from reviewer where reviewer_id={}"
    query=query.format(r_id)
    cursor.execute(query)
    y=cursor.fetchall()


    return y[0][1]
