from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from django.db import IntegrityError
from django.http import HttpResponseRedirect


# Create your views here.

#Reviewer table should  have an entry with Reviewer_Id = -1

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
#ADMIN_MODULE

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
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1]==1:
            if request.method=="POST":
                entered_data = request.POST
                for i in list(entered_data.values()):
                    if i=='':
                        return render(request, "admin_appoint_reviewer.html",{'error':'Kindly enter all values.'})
                # if len(entered_data.keys())<4:
                #     return render(request, "admin_appoint_reviewer.html",{'error':'Kindly enter all values.'})
                insert_query = "insert into magazine_reviewer values ('{}','{}')"
                reg_login_query = "insert into magazine_login_cred values ('{}','{}',2)"
                insert_query = insert_query.format(entered_data['username'],entered_data['name'])
                reg_login_query = reg_login_query.format(entered_data['username'],entered_data['password'])
                cursor = connection.cursor()
                try:
                    cursor.execute(reg_login_query)
                    cursor.execute(insert_query)
                except IntegrityError :
                    secret_password = "idonnohowtomakeasecretpassword"
                    get_password = "select password from magazine_login_cred where u_id = '{}'"
                    get_password = get_password.format(entered_data['username'])
                    cursor.execute(get_password)
                    password = cursor.fetchone()
                    if password[0] == secret_password:
                        change_password_query = "update magazine_login_cred set password = '{}' where u_id = '{}'"
                        change_password_query = change_password_query.format(entered_data['password'], entered_data['username'])
                        cursor.execute(change_password_query)
                        return render(request,"admin_appoint_reviewer_1.html")
                    else:
                        return  render(request, "admin_appoint_reviewer.html",{'error':'User already exists'})
                return render(request,"admin_appoint_reviewer_1.html")
            return render(request,"admin_appoint_reviewer.html")
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")
    

def remove_reviewer(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1]==1:
            if request.method=="POST":
                entered_data = request.POST
                # print(entered_data)
                if entered_data['username']=='':
                    return render(request, "admin_remove_reviewer.html",{'error':'Kindly enter a Reviewer ID.'})
                select_query = "select * from magazine_reviewer where reviewer_id = '{}'"
                select_query = select_query.format(entered_data['username'])
                # remove_query = "delete from magazine_reviewer where reviewer_id = '{}'"
                # remove_login_query = "delete from magazine_login_cred where u_id = '{}'"
                # remove_query = remove_query.format(entered_data['username'])
                # remove_login_query = remove_login_query.format(entered_data['username'])
                cursor = connection.cursor()
                cursor.execute(select_query)
                y = cursor.fetchall()
                if len(y)==0:
                    return render(request, "admin_remove_reviewer.html",{'error':"User doesn't exist."})
                secret_password = "idonnohowtomakeasecretpassword"
                change_password_query = "update magazine_login_cred set password = '{}' where u_id = '{}'"
                change_password_query = change_password_query.format(secret_password, entered_data['username'])
                change_name_query = "update magazine_reviewer set name='{}' where reviewer_id='{}'"
                change_name_query = change_name_query.format(secret_password, entered_data['username'])
                cursor.execute(change_password_query)
                cursor.execute(change_name_query)
                change_reviewer_query = "update magazine_article set reviewer_id=-1, status=1 where reviewer_id='{}' and status=2"
                change_reviewer_query = change_reviewer_query.format(entered_data['username'])
                cursor.execute(change_reviewer_query)
                # cursor.execute(remove_query)
                # cursor.execute(remove_login_query)
                return render(request, "admin_remove_reviewer_1.html")
            return render(request,"admin_remove_reviewer.html")
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")

'''
in remove reviewer
change password in login_cred
in articles where reviewer id = r_id and status = 2 change status to 1 and reviewer id to -1

in appoint reviewer
if user already exists,
check if password = secret password
then change password to new password
'''
    

def view_unassigned_articles(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            fetched_data=get_articles_list(1)
            articles = []
            reviewers = get_list_of_reviewers()
            for i in fetched_data:
                details = {'article_id' : i[0], 'title' : i[1], 'author' : i[2]}
                articles.append(details)
            
            if request.method=="POST":
                to_be_sent = request.POST
                my_list=list(to_be_sent.values())[1:]
                for i in my_list:
                    stri=i
                    # print(stri)
                    j=0
                    r_id=""
                    a_id=""
                    while(j<len(stri) and stri[j]!='*'):
                        r_id=r_id+stri[j]
                        j=j+1
                    r_id=r_id
                    j=j+1
                    while(j<len(stri)):
                        a_id=a_id+stri[j]
                        j=j+1
                    a_id=a_id
                    num=int(a_id)
                    send_for_review(num,r_id)
                    return HttpResponseRedirect(request.path_info)

            return render(request,"admin_unassigned_articles_list.html",{"articles":[articles,reviewers]})
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")

def view_pending_articles(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            fetched_data=get_articles_list(2)
            # print(fetched_data)
            articles = []
            for i in fetched_data:
                details = {'article_id' : i[0], 'title' : i[1], 'author' : i[2],'reviewer':get_reviewer_name(i[6])}
                articles.append(details)

            return render(request,"admin_pending_articles_list.html",{"articles":articles})
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")



def view_reviewed_articles(request):
    # select articles from this, give publish option
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            cursor = connection.cursor()
            query = "select article_id,title,author,reviewer_id,rating from magazine_article where status=3 order by rating desc;"
            cursor.execute(query)
            fetched_data = cursor.fetchall()
            articles = []
            for i in fetched_data:
                details = {'article_id' : i[0], 'title' : i[1], 'author' : i[2], 'reviewer_id': i[3]}
                for j in range(0,11):
                    temp = 'checked' + str(j)
                    if i[4] == j:
                        details[temp] = 'checked'
                    else :
                        details[temp] = ''
                articles.append(details)
            if request.method=="POST":
                to_be_published = request.POST
                article_id_list=list(to_be_published.values())[1:]
                for i in article_id_list:
                    publish(i)
                return HttpResponseRedirect(request.path_info)
            # details = {'title' : article[0], 'author' : article[1], 'content' : article[2], 'status': article[3]}
            # revert()
            return render(request,"admin_reviewed_articles_list.html",{"articles":articles})
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")

def admin_view_article(request,article_id = None):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 1:
            if article_id == None:
                return redirect('../')
            cursor = connection.cursor()
            query = "select title,author,content,status,reviewer_id,rating from magazine_article where article_id = '{}';"
            query = query.format(article_id)
            cursor.execute(query)
            article = cursor.fetchall()

            if len(article) == 0:
                return redirect('../')

            article = article[0]

            details = {'title' : article[0], 'author' : article[1], 'content' : article[2], 'status': article[3], 'reviewer':'N/A'}
            
            if details['status'] >= 2 :
                query = "select name from magazine_reviewer where reviewer_id = '{}';"
                query = query.format(article[4])
                cursor.execute(query)
                reviewer_name = cursor.fetchall()[0][0]
                details['reviewer'] = reviewer_name
                if details['status'] >= 3:
                    details['rating'] = article[5]
            
            if details['status'] == 1:
                details['status'] = 'Unassigned'
            elif details['status'] == 2:
                details['status'] = 'Unreviewed'
            elif details['status'] == 3:
                details['status'] = 'Reviewed'
            else:
                details['status'] = 'Published'    

            for i in range(0,11):
                temp = 'checked' + str(i)
                if article[3] >= 3 and article[5] == i:
                    details[temp] = 'checked'
                else :
                    details[temp] = ''

            return render(request,"admin_view_article.html", details)
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")


"***************************************************************************************************************"
#REVIEWER_MODULE

def reviewer_module(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            return render(request,"reviewer_module.html",{'username' : get_reviewer_name(user_details[0])})
        else:
            return redirect("../login")
    else:
        return redirect("../login")

def reviewer_reviewed_articles_list(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            cursor = connection.cursor()
            query = "select article_id,title,author,rating from magazine_article where reviewer_id = '{}' and status >= 3;"
            query = query.format(user_details[0])
            cursor.execute(query)
            result = cursor.fetchall()
            reviewed_list = []
            for article in result:
                dict = {}
                dict['article_id'] = article[0]
                dict['title'] = article[1]
                dict['author'] = article[2]
                for i in range(0,11):
                    temp = 'checked' + str(i)
                    if article[3] == i:
                        # print(i)
                        dict[temp] = 'checked'
                    else :
                        dict[temp] = ''
                reviewed_list.append(dict)
            return render(request,"reviewer_reviewed_articles_list.html",{'username' : get_reviewer_name(user_details[0]), 'articles': reviewed_list})
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")

def reviewer_pending_articles_list(request):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            cursor = connection.cursor()
            query = "select * from magazine_article where reviewer_id = '{}' and status = 2;"
            query = query.format(user_details[0])
            cursor.execute(query)
            result = cursor.fetchall()
            pending_list = []
            for article in result:
                dict = {}
                dict['article_id'] = article[0]
                dict['title'] = article[1]
                dict['author'] = article[2]
                pending_list.append(dict)
            return render(request,"reviewer_pending_articles_list.html",{'username' : get_reviewer_name(user_details[0]), 'articles': pending_list})
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")

"***************************************************************************************************************"

def view_magazine(request):
    article_list = get_articles_list(4)
    sno_article_list = []
    for i,article in enumerate(article_list):
        sno_article_list.append((i+1,article[0],article[1],article[2]))
    return render(request,'magazine.html',{'articles':sno_article_list})

def create_article(request):
    if request.method=="POST":
        info=request.POST
        title=info["title"]
        content=info["content"]
        author=info["author"]
        title = title.replace("'","''")
        content = content.replace("'","''")
        author = author.replace("'","''")        
        add_new_post(title,author,content)

    return render(request,"create_article.html")

"*********************************KD_FUNCTIONS******************************************************************"

def get_article(a_id):
    cursor =  connection.cursor()
    query="select * from magazine_article where article_id={}"
    query=query.format(a_id)
    cursor.execute(query)
    y=cursor.fetchone()
    return y

def publish(a_id):
    cursor =  connection.cursor()
    query="update magazine_article set status=4 where article_id={}"
    query=query.format(a_id)
    cursor.execute(query)

def revert():
    cursor = connection.cursor()
    query = "update magazine_article set status=3"
    cursor.execute(query)

def get_articles_list(status):
    cursor =  connection.cursor()
    query="select * from magazine_article where status={}"
    query=query.format(status)
    cursor.execute(query)
    y=cursor.fetchall()
    return y

def get_list_of_reviewers():
    secret_password = "idonnohowtomakeasecretpassword"
    cursor =  connection.cursor()
    query="select * from magazine_reviewer where reviewer_id!='-1' and name != '{}'"
    query = query.format(secret_password)
    cursor.execute(query)
    y=cursor.fetchall()

    return y

def send_for_review(a_id,r_id):
    cursor =  connection.cursor()
    query="update magazine_article set reviewer_id={},status=2 where article_id={}"
    query=query.format(r_id,a_id)
    cursor.execute(query)

def send_for_review(a_id,r_id):
    cursor =  connection.cursor()
    query="update magazine_article set reviewer_id='{}',status=2 where article_id={}"
    query=query.format(r_id,a_id)
    cursor.execute(query)

def get_reviewer_name(r_id):
    cursor =  connection.cursor()
    query="select * from magazine_reviewer where reviewer_id='{}'"
    query=query.format(r_id)
    cursor.execute(query)
    y=cursor.fetchall()
    return y[0][1]

def add_new_post(title,author,content):
    cursor =  connection.cursor()
    query="select max(article_id) from magazine_article"
    cursor.execute(query)
    y=cursor.fetchall()
    a_id=y[0][0]+1
    query="INSERT INTO magazine_article  VALUES ('{}','{}','{}','{}',1,-1,'-1');"
    # print(a_id,title,author,content)
    query=query.format(a_id,title,author,content)
    cursor.execute(query)

def atoi(stri):
    j=0
    num=0
    while(j<len(stri)):
        num=num*10+int(stri[j])
        j=j+1
    return num


"***************************************************************************************************************"

def magazine_article(request, article_id = None):
    if article_id == None:
        return redirect('../')
    cursor = connection.cursor()
    query = "select title,author,content,status from magazine_article where article_id = '{}';"
    query = query.format(article_id)
    cursor.execute(query)
    article = cursor.fetchall()
    if len(article) == 0 or article[0][3] != 4:
        return redirect('../')
    
    article = article[0]
    
    details = {'title' : article[0], 'author' : article[1], 'content' : article[2]}
    return render(request,"magazine_article.html",details)

def reviewer_view_article(request,article_id=None):
    if request.session.has_key('user'):
        user_details = request.session['user']
        if user_details[1] == 2:
            if article_id == None:
                return redirect('../')
            cursor = connection.cursor()
            query = "select title,author,content,status,rating,reviewer_id from magazine_article where article_id = '{}';"
            query = query.format(article_id)
            cursor.execute(query)
            article = cursor.fetchall()
            
            if len(article) == 0:
                return redirect('../')
            article = article[0]
            if article[5] != user_details[0]:
                return redirect('../')

            details = {'username' : get_reviewer_name(user_details[0]), 'title' : article[0], 'author' : article[1], 'content' : article[2], 'status' : article[3], 'disabled' : '', 'reviewable' : ''}
            
            if details['status'] == 2:
                details['reviewable'] = 'reviewable'
                details['status'] = 'Unreviewed'
            elif details['status'] == 3:
                details['disabled'] = 'disabled'
                details['status'] = 'Reviewed'
            else:
                details['disabled'] = 'disabled'
                details['status'] = 'Published'

            final_status = article[3]
            final_rating = article[4]
            if request.method == 'POST':
                res = request.POST
                if details['status'] == 'Unreviewed':
                    query = "update magazine_article set rating = '{}', status = 3 where article_id = '{}';"
                    query = query.format(res['rating'],article_id)
                    cursor.execute(query)
                    details['status'] = 'Reviewed'
                    details['disabled'] = 'disabled'
                    final_status = 3
                    final_rating = int(res['rating'])
                else :
                    details['error'] = 'Article cannot be re-rated.'

            for i in range(0,11):
                temp = 'checked' + str(i)
                if final_status >= 3 and final_rating == i:
                    details[temp] = 'checked'
                else :
                    details[temp] = ''

            return render(request,"reviewer_view_article.html",details)
                
        else:
            return redirect("../../login")
    else:
        return redirect("../../login")


"***************************************************************************************************************"



def give_rating(a_id,rating):
    cursor =  connection.cursor()


    if(rating>10):
        return -1
    else:
        query="update article set rating={},status=3 where article_id={}"
        query=query.format(rating,a_id)
        cursor.execute(query)


def get_reviewer_articles(r_id,status):
    cursor =  connection.cursor()


    query="select * from article where status={},reviewer_id={}"
    query=query.format(status,r_id)
    cursor.execute(query)
    y=cursor.fetchall()
    return y






