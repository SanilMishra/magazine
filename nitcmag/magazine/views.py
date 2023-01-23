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
    

def view_assigned_articles(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def send_for_review(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def view_pending_articles(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def view_reviewed_articles(request):
    # select articles from this, give publish option
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

"***************************************************************************************************************"

def reviewer_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def reviewed_articles_reviewer(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def pending_articles_reviewer(request):
    #review article option
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"base.html")
        else:
            return redirect("../login")
    else:
        return redirect("../login")


"***************************************************************************************************************"

def view_magazine(request):
    return render(request,'magazine.html')