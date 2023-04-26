from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from django.core.mail import send_mail
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from MyApp.models import Mentor, Startup

global guser
user = None

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Logout(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def StartupRegister(request):
    if request.method == 'GET':
        # print(request.session['poc_email'])
        return render(request, 'StartupRegister.html', {})
    

def MentorRegister(request):
    if request.method == 'GET':
       return render(request, 'MentorRegister.html', {})

@csrf_exempt
def SuggestionAction(request):
    if request.method == 'POST':
        status = "Error in adding suggestion"
        qid = request.POST.get('t1', False)
        suggestion = request.POST.get('t2', False)
        # company_name = request.POST.get('t2', False)
        # smail = request.POST.get('t3', False)
        # query = request.POST.get('t4', False)
        # suggestion= request.POST.get('t5', False)
        print(str(qid)+" "+" "+str(suggestion))
        mentor_mail = None
        db_connection =  pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        db_cursor = db_connection.cursor()

        #get  mentor mail before inserting into DB
        db_cursor.execute("select mentor_mail, email, query from queries where query_id='"+qid+"'")
        rows = db_cursor.fetchall()
        for row in rows:
            mentor_mail = row[0]
            smail = row[1]
            query = row[2]


        #student_sql_query = "INSERT INTO suggestion(query_id,expert_name,suggestion) VALUES('"+qid+"','"+guser+"','"+suggestion+"')"
        #student_sql_query = "INSERT INTO suggestion(query_id, mentor_mail, email, query, suggestion) VALUES('"+qid+"','"+mentor_mail+"','"+smail+"','"+query+"','"+suggestion+"')"
        db_cursor = db_connection.cursor()
        insert_query = "insert into suggestions(query_id, mentor_mail, email, query, suggestion) values('"+qid+"', '"+mentor_mail+"', '"+smail+"', '"+query+"', '"+suggestion+"')"
        db_cursor.execute(insert_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Your suggestion accepted'
        context= {'data':status}
        #return render(request, 'MentorScreen.html', context)    
        return ViewProfile(request, context)



#done maximum work 
def PostQueries(request):
    if request.method == 'GET':
        # output = '<tr><td><font size="" color="black">Choose&nbsp;Domain/Group</b></td><td><select name="t2">'
       # output = '<tr><td><font size="" color="black">Choose&nbsp;Mentor</b></td><td><select name="t2">'
        output=''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            mentors_sub = {}
            cur = con.cursor()
            cur.execute("select mentor_email from subscribe where email='"+user.email+"'")
            rows = cur.fetchall()
            for row in rows:
                cur.execute("select fname, lname from mentor where email='"+row[0]+"'")
                rows1 = cur.fetchall()
                print(rows1)
                name = str(rows1[0][0])+" "+str(rows1[0][1])
                mentors_sub[row[0]] = name
            for mentor_email, mentor_name in mentors_sub.items():
                output+='<option value="'+mentor_email+'">'+mentor_name+'</option>'
            # for row in rows:
            #     output+='<option value="'+row[0]+'">'+row[0]+'</option>'
        context= {'data':output}
        return render(request, 'PostQueries.html', context)

#needs some work to be done
def PostQueriesAction(request):
    if request.method == 'POST':
        status = "Error in posting query"
        query = request.POST.get('t2')
        mentor_email = request.POST.get('t1')
        count = 0
        print(type(query), query)
        print(type(mentor_email), mentor_email)
        # print(type(user.company_name))
        # print(type(user.email))
        count = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select count(*) from queries")
            rows = cur.fetchall()
            for row in rows:
                count = row[0]
        count += 1
        today = date.today()
        print(type(today))
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        db_cursor = db_connection.cursor()
        # student_sql_query = "INSERT INTO queries(query_id,username,domain,query,query_date) VALUES('"+str(count)+"','"+guser+"','"+group+"','"+query+"','"+str(today)+"')"
        insert_squery_query = "INSERT INTO queries(query_id,mentor_mail,company_name,email,query,query_date) VALUES('"+str(count)+"', '"+mentor_email+"', '"+user.company_name+"', '"+user.email+"', '"+query+"', '"+str(today)+"')"
        print(insert_squery_query)
        db_cursor.execute(insert_squery_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Your query posted successfully'
        context= {'data':status}
        #return render(request, 'StartupScreen.html', context)    
        return ViewProfile(request, context)
    

def ViewSuggestions(request): #should dynamically give the list of mentors like present in postqueries
    if request.method == 'GET':
        output = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        # with con:
        #     cur = con.cursor()
        #     cur.execute("select group_name from subscribe where username='"+guser+"'")
        #     rows = cur.fetchall()
        #     for row in rows:
        #         output+='<option value="'+row[0]+'">'+row[0]+'</option>'
        with con:
            mentors_sub = {}
            cur = con.cursor()
            cur.execute("select mentor_email from subscribe where email='"+user.email+"'")
            rows = cur.fetchall()
            for row in rows:
                cur.execute("select fname, lname from mentor where email='"+row[0]+"'")
                rows1 = cur.fetchall()
                print(rows1)
                name = str(rows1[0][0])+" "+str(rows1[0][1])
                mentors_sub[row[0]] = name
            for mentor_email, mentor_name in mentors_sub.items():
                output+='<option value="'+mentor_email+'">'+mentor_name+'</option>'
        context= {'data':output}
        return render(request, 'SuggestionView.html', context)


def getExperience(expert):
    output = ""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select experience from mentorregister where email='"+expert+"'")
        rows = cur.fetchall()
        for row in rows:
            output = str(row[0])
    return output    

def getQueryDetails(qid):
    details = []
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select expert_name,suggestion from suggestion where query_id='"+str(qid)+"'")
        rows = cur.fetchall()
        for row in rows:
            details.append(row[0])
            details.append(row[1])
            experience = getExperience(row[0])
            details.append(experience)
    return details

def getGroupDetails(owner):
    details = []
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select avg(rating) from rating where mentor='"+owner+"'")
        rows = cur.fetchall()
        for row in rows:
            details.append(row[0])            
    return details      

def ViewRatings(request):
    if request.method == 'GET':
        output = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select Group_owner,group_name from formgroup")
            rows = cur.fetchall()
            for row in rows:
                owner = row[0]
                group = row[1]
                details = getGroupDetails(owner)
                if len(details) > 0:
                    output+='<tr><td><font size="" color="black">'+owner+'</td><td><font size="" color="black">'+group+'</td>'
                    output+='<td><font size="" color="black">'+str(details[0])+'</td></tr>'
        context= {'data':output}
        return render(request, 'ViewRatings.html', context)

def SuggestionView(request):  #this is similar view mentors
    if request.method == 'POST':
        # group = request.POST.get('t1', False)
        # output = ""
        # con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'scaleup',charset='utf8')
        # with con:
        #     cur = con.cursor()
        #     cur.execute("select * from queries where domain='"+group+"'")
        #     rows = cur.fetchall()
        #     for row in rows:
        #         qid = row[0]
        #         startup = row[1]
        #         domain = row[2]
        #         query = row[3]
        #         date = row[4]
        #         details = getQueryDetails(qid)
        #         if len(details) > 0:
        #             output+='<tr><td><font size="" color="black">'+str(qid)+'</td><td><font size="" color="black">'+startup+'</td>'
        #             output+='<td><font size="" color="black">'+domain+'</td><td><font size="" color="black">'+query+'</td>'
        #             output+='<td><font size="" color="black">'+str(date)+'</td>'
        #             output+='<td><font size="" color="black">'+str(details[0])+'</td>'
        #             output+='<td><font size="" color="black">'+str(details[2])+'</td>'
        #             output+='<td><font size="" color="black">'+str(details[1])+'</td>'
        #             output+='<td><a href=\'Rating?t1='+startup+'&t2='+details[0]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
 # this is the way data is put into the html page, data is displayed on html page
 # check SuggestionView.html line number 77 ***
        mentor_mail = request.POST.get('t1', False)
        tmentor_name = ""
        tdomain = ""
        Rating='<input type="number" placeholder="1-5" min="1" max="5">'
        output = ""
        table = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            mentors_sub = {}
            cur = con.cursor()
            cur.execute("select mentor_email from subscribe where email='"+user.email+"'")
            rows = cur.fetchall()
            for row in rows:
                cur.execute("select fname, lname from mentor where email='"+row[0]+"'")
                rows1 = cur.fetchall()
                print(rows1)
                name = str(rows1[0][0])+" "+str(rows1[0][1])
                mentors_sub[row[0]] = name
            for mentor_email, mentor_name in mentors_sub.items():
                output+='<option value="'+mentor_email+'">'+mentor_name+'</option>'
        
            cur = con.cursor()
            cur.execute("select fname, lname, domain_name from mentor where email='"+mentor_mail+"'")
            rows = cur.fetchall()
            for row in rows:
                tmentor_name = row[0]+" "+row[1]
                tdomain = row[2]
            

            cur = con.cursor()
            cur.execute("select query_id, query, suggestion from suggestions where mentor_mail='"+mentor_mail+"'")
            rows = cur.fetchall()
            for row in rows:
                table+='<tr><td>'+str(row[0])+'</td>'
                table+='<td>'+tmentor_name+'</td>'
                table+='<td>'+tdomain+'</td>'
                table+='<td>'+row[1]+'</td>'
                table+='<td>'+row[2]+'</td>'
                table+='<td>'+Rating+'</td></tr>'
                

        context= {'data':output,'table':table}
        return render(request, 'SuggestionView.html', context)


def Rating(request):
    if request.method == 'GET':
        startup = request.GET.get('t1', False)
        expert = request.GET.get('t2', False)
        output = '<tr><td><b>Startup&nbsp;ID</b></td><td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value="'+startup+'" readonly/></td></tr>'
        output += '<tr><td><b>Mentor&nbsp;ID</b></td><td><input type="text" name="t2" style="font-family: Comic Sans MS" size="30" value="'+expert+'" readonly/></td></tr>'
        context= {'data':output}
        return render(request, 'Rating.html', context)

def RatingAction(request):
    if request.method == 'POST':
        status = "Error in adding rating";
        startup = request.POST.get('t1', False)
        expert = request.POST.get('t2', False)
        rating = request.POST.get('t3', False)
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO rating(startUp,mentor,rating) VALUES('"+startup+"','"+expert+"','"+rating+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = 'Your rating accepted for mentor '+expert;
        context= {'data':status}
        return render(request, 'StartupScreen.html', context)  

def Suggestions(request):
    if request.method == 'GET':
        qid = request.GET.get('t1', False)
        #output = '<tr><td><b>Query&nbsp;ID</b></td><td><input type="text" name="t1" style="font-family: Comic Sans MS" value='+qid+' readonly/></td></tr>'
        output = '<tr><td><input type="hidden" name="t1" value='+qid+' ></td></tr>'
        context= {'data':output}
        return render(request, 'Suggestions.html', context)

@csrf_exempt
def ViewQueries(request):
    if request.method == 'GET':
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
        #do not need the next few lines, since a mentor is shown all the queries asked to him
        # with con:
        #     cur = con.cursor()
        #     cur.execute("select group_name from formgroup where Group_owner='"+guser+"'")
        #     rows = cur.fetchall()
        #     for row in rows:
        #         domain_list.append(row[0])
        output = ""

        #only display queries that are related to the particular mentor
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from queries where mentor_mail='"+user.email+"'")
            #cur.execute("select * from queries where mentor_email='"+user.email+"'") #shows query of that mentor only
            rows = cur.fetchall()
            for row in rows:
                qid = row[0]
                company_name = row[2]
                # domain = row[2]
                query = row[3]
                date = row[4]
                email = row[5]
                
                #print(domain+" "+str(domain_list))
                # if domain in domain_list:
                #     output+='<tr><td><font size="" color="black">'+str(qid)+'</td><td><font size="" color="black">'+startup+'</td>'
                #     output+='<td><font size="" color="black">'+domain+'</td><td><font size="" color="black">'+query+'</td>'
                #     output+='<td><font size="" color="black">'+str(date)+'</td>'
                #     output+='<td><a href=\'Suggestions?t1='+str(qid)+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
                output+='<tr><td name="t1">'+str(qid)+'</td>'
                output+='<td>'+company_name+'</td>'
                output+='<td>'+query+'</td>'
                output+='<td>'+date+'</td>'
                output+='<td>'+email+'</td>'
                #output+='<td ><textarea name="t5" name='+str(qid)+' placeholder="Give your suggestion here"  cols="30" rows="5"></textarea></td>'
                output+='<td><a href=\'Suggestions?t1='+str(qid)+'\'><font size=3 color=black>Click Here</font></a></td></tr>'

        context= {'data':output}
        return render(request, 'ViewQueries.html', context)


def getOwnerDetails(owner):
    details = []
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select age,qualification,experience from mentorregister where email = '"+owner+"'")
        rows = cur.fetchall()
        for row in rows:
            details.append(row[0])
            details.append(row[1])
            details.append(row[2])
    return details            

def ViewStartupGroup(request):
    if request.method == 'GET':
        # output = ""
        # con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'scaleup',charset='utf8')
        # with con:
        #     cur = con.cursor()
        #     cur.execute("select * from mentor")
        #     rows = cur.fetchall()
        #     for row in rows:
        #         owner_name = row[0]+' '+row[1]
        #         # details = getOwnerDetails(owner)
        #         exp = row[3]
        #         currect_company = row[4]
        #         linkedin = row[6]
        #         rating = row[7]
        #         output+='<tr><td><font size="" color="black">'+owner_name+'</td>'
        #         output+='<td><font size="" color="black">'+exp+'</td>'
        #         output+='<td><font size="" color="black">'+currect_company+'</td>'
        #         output+='<td><font size="" color="black">'+linkedin+'</td>'
        #         output+='<td><font size="" color="black">'+str(rating)+'</td>'
        #         output+='<td><a href=\'Subscribe?t1=''\'><font size=3 color=black>Click Here</font></a></td></tr>'
        #context= {'data':output}
        return render(request, 'ViewStartupGroup.html')


def ViewMentorRatings(request):
    if request.method == 'GET':
        output=""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select avg(rating) from rating where mentor='"+guser+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] is not None:
                    output+='<tr><td><font size="" color="black">'+guser+'</td><td><font size="" color="black">'+str(row[0])+'</td></tr>'                
        context= {'data':output}
        return render(request, 'ViewMentorRatings.html', context)     

def GroupForm(request):
    if request.method == 'GET':
        output=""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM formgroup")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+row[1]+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+str(row[3])+'</td></tr>'
        context= {'data':output}
        return render(request, 'GroupForm.html', context)        


#understood it correctly, need to change variable names
def Subscribe(request):
    if request.method == 'GET':
        # name = request.GET.get('t1', False)
        mentor_email = request.GET.get('t1',False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            cur = con.cursor()
            #cur.execute("select group_name from subscribe where group_name = '"+name+"' and username='"+guser+"'")
            cur.execute("select mentor_email from subscribe where email='"+user.email+"' and mentor_email='"+mentor_email+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == mentor_email:
                    status = "You already subscribed to this mentor."
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
            db_cursor = db_connection.cursor()
            #student_sql_query = "INSERT INTO subscribe(username,group_name) VALUES('"+guser+"','"+name+"')"
            student_sql_query = "INSERT INTO subscribe(email, mentor_email) VALUES('"+user.email+"','"+mentor_email+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'You have succesfully subscribed!' #change to mentor name
                db_cursor = db_connection.cursor()
                # student_sql_query = "update formgroup set users_count=users_count+1 where group_name='"+name+"'"
                # db_cursor.execute(student_sql_query)
                db_connection.commit()
        context= {'data':status}
        #return render(request, 'StartupScreen.html', context)
        return ViewProfile(request, context)
        
#used to form groups by a mentor(not used in v3)
def FormGroup(request):
    if request.method == 'POST':
        name = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select group_name from formgroup where group_name = '"+guser+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == name:
                    status = "Given group name "+name+" already exists"
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'mentor',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO formgroup(Group_owner,group_name,description,users_count) VALUES('"+guser+"','"+name+"','"+desc+"','0')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Group created successfully'
        context= {'data':status}
        return render(request, 'MentorScreen.html', context)


def MentorRegisterAction(request):
    if request.method == 'POST':
        fname = request.POST.get('t1', False)
        lname = request.POST.get('t2', False)
        exp= request.POST.get('t3', False)
        domain_name= request.POST.get('t4', False)
        current_company = request.POST.get('t5', False)
        email = request.POST.get('t6', False)
        linkedin = request.POST.get('t7', False)
        rating = request.POST.get('t8', False)
        pswd = request.POST.get('t9', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select email from mentor where email = '"+email+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == email:
                    status = 'Given Email id already exists'
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO mentor(fname,lname,exp,domain_name,current_company,email,linkedin,rating,pswd) VALUES('"+fname+"','"+lname+"','"+exp+"','"+domain_name+"','"+current_company+"','"+email+"','"+linkedin+"','"+rating+"','"+pswd+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                #send an email confirmation of registration
                send_mail('Successful Registration','Hello '+fname+' '+lname+',\n You have successly completed the registration to our website. Please login to your account and start exploring our site.','scaleupstartups@zohomail.in',[email],fail_silently=False)
                status = 'Signup Process Completed'
        context= {'data':status}
        return render(request, 'MentorRegister.html', context)


#need to done
def StartupRegisterAction(request):
    if request.method == 'POST':
        # fname = request.POST.get('t1', False)
        # lname = request.POST.get('t2', False)
        # email = request.POST.get('t3', False)
        # contact = request.POST.get('t4', False)
        # address = request.POST.get('t5', False)
        # age = request.POST.get('t10', False)
        # password = request.POST.get('t7', False)
        # qualification = request.POST.get('t8', False)
        # experience = request.POST.get('t9', False)
        company_name = request.POST.get('t1', False)
        age = request.POST.get('t2', False)
        emps = request.POST.get('t3', False)
        domain = request.POST.get('t5', False)
        descp = request.POST.get('t4', False)
        poc = request.POST.get('t6', False)
        poc_email = request.POST.get('t7', False)
        email = request.POST.get('t8', False)
        linkedin = request.POST.get('t9', False)
        website = request.POST.get('t10', False)
        pswd = request.POST.get('t11', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select email from startup where email = '"+email+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == email:
                    status = 'Given Email id already exists'
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
            db_cursor = db_connection.cursor()
            # student_sql_query = "INSERT INTO startupregister(first_name,last_name,email,contact_no,address,age,password,qualification,experience) VALUES('"+fname+"','"+lname+"','"+email+"','"+contact+"','"+address+"','"+age+"','"+password+"','"+qualification+"','"+experience+"')"
            student_sql_query = "INSERT INTO startup(company_name, age, startup_domain, emps, descp, poc, poc_email, email, linkedin, website, pswd) VALUES('"+company_name+"','"+str(age)+"','"+domain+"','"+str(emps)+"','"+descp+"','"+poc+"','"+poc_email+"','"+email+"','"+linkedin+"','"+website+"','"+pswd+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Signup Process Completed'
                #send an email confirmation of registration
                send_mail('Successful Registration','Hello '+company_name+',\n You have successly completed the registration to our website. Please login to your account and start exploring our site.','scaleupstartups@zohomail.in',[email],fail_silently=False)
        context= {'data':status}
        return render(request, 'StartupRegister.html', context)    
      
def checkUser(username, password, table, request):
    flag = False
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM "+table)
        rows = cur.fetchall()
        if (table == "mentor"):
            for row in rows:
                if row[5] == username and row[8] == password:                
                    user = Mentor()
                    request.session['fname'] = user.fname = row[0]
                    request.session['lname'] = user.lname = row[1]
                    request.session['exp'] = user.exp = row[2]
                    request.session['domain_name'] = user.domain_name = row[3]
                    request.session['current_company'] = user.current_company = row[4]
                    request.session['email'] = user.email = row[5]
                    request.session['linkedin'] = user.linkedin = row[6]
                    request.session['rating'] = user.rating = row[7]
                    # user.fname = row[0]
                    # user.lname = row[1]
                    # user.exp = row[2]
                    # user.domain_name = row[3]
                    # user.current_company = row[4]
                    # user.email = row[5]
                    # user.linkedin = row[6]
                    # user.rating = row[7]
                    return user
        else:
            for row in rows:
                if row[7] == username and row[10] == password:                
                    user = Startup()
                    request.session['company_name'] = user.company_name = row[0]
                    request.session['age'] = user.age = row[1]
                    request.session['domain'] = user.domain = row[2]
                    request.session['emps'] = user.emps = row[3]
                    request.session['descp'] = user.descp = row[4]
                    request.session['poc'] = user.poc = row[5]
                    request.session['poc_email'] = user.poc_email = row[6]
                    request.session['email'] = user.email = row[7]
                    request.session['linkedin'] = user.linkedin = row[8]
                    request.session['website'] = user.website = row[9]
                    user.company_name = row[0]
                    user.age = row[1]
                    user.domain = row[2]
                    user.emps = row[3]
                    user.descp = row[4]
                    user.poc = row[5]
                    user.poc_email = row[6]
                    user.email = row[7]
                    user.linkedin = row[8]
                    user.website = row[9]
                    return user        
        
    
#work on this action so that after login home page should be displayed with the user's details
def LoginAction(request):
    if request.method == 'POST':
        global guser
        global user
        guser = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        utype = request.POST.get('t3', False)
        status = 'none'
        output = 'none'
        if utype == "Mentor":
            user = checkUser(guser,password,"mentor",request) 
            if user != None:
                output = "MentorScreen.html"
                status = "Welcome "+user.fname+"!"
            else:
                output = "Login.html"
                status = "Invalid Login"
        else:
            user = checkUser(guser,password,"startup",request) 
            if user != None:
                output = "StartupScreen.html"
                status = "Welcome "+user.company_name
            else:
                output = "Login.html"
                status = "Invalid Login"
        context= {'data': status, 'user': user}
        return render(request, output, context)
        
            
# def StartupScreen(request):
#     if request.method == 'POST':
#        return render(request, 'StartupScreen.html', {})


#filter mentors 
def Filter(request):
    output = ""
    domain=request.GET.get("domain")
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
    with con:            
        cur = con.cursor()
        cur.execute("select * from mentor where domain_name = '"+domain+"'")
        rows = cur.fetchall()
        for row in rows:
            mentor_name = row[0]+' '+row[1]
            # details = getOwnerDetails(owner)
            exp = row[2]
            currect_company = row[4]
            mentor_email = row[5]
            linkedin = row[6]
            rating = row[7]
            output+='<tr><td><font size="" color="black">'+mentor_name+'</td>'
            output+='<td><font size="" color="black">'+str(exp)+'</td>'
            output+='<td><font size="" color="black">'+currect_company+'</td>'
            output+='<td><font size="" color="black">'+linkedin+'</td>'
            output+='<td><font size="" color="black">'+str(rating)+'</td>'
            output+='<td><button><a href=\'Subscribe?t1='+mentor_email+'\'><font size=3 color=black>Click Here</font></a></button></td></tr>'
    context= {'data':output}
    return render(request, 'ViewStartupGroup.html', context)


def ViewProfile(request, *args):
    context1 = args
    print(context1)
    if len(context1) == 0:
        context1 = [{'data': ''}, 'temp']
    if type(user).__name__ == "Mentor":
        context = {'user':user,'data': context1[0]['data']}
        return render(request, 'MentorScreen.html', context)
    else:
        context = {'user':user, 'data': context1[0]['data']}
        return render(request, 'StartupScreen.html', context)       


def ForgotPassword(request):
    return render(request, 'ForgotPassword.html')

def ForgotPasswordSubmit(request):
    if request.method == 'POST':
        email = request.POST.get('t1',False)
        flag = False
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
        with con:            
            cur = con.cursor()
            cur.execute("select email, pswd, fname, lname from mentor")
            rows = cur.fetchall()
            for row in rows:
                if email == row[0]:
                    password = row[1]
                    fname = row[2]
                    lname = row[3]
                    send_mail('Forgot Password request','Hello '+fname+' '+lname+',\nYour current password is: '+password+'\nPlease login to your account and start exploring our site.','scaleupstartups@zohomail.in',[email],fail_silently=False)
                    flag = True
            cur.execute("select email, pswd, company_name from startup")
            rows = cur.fetchall()
            for row in rows:
                if email == row[0]:
                    password = row[1]
                    company_name = row[2]
                    send_mail('Forgot Password request','Hello '+company_name+',\nYour current password is: '+password+'\nPlease login to your account and start exploring our site.','scaleupstartups@zohomail.in',[email],fail_silently=False)
                    flag = True
            if flag:
                #send a success msg, pass sent to mail (mostly js pop up) 
                context = {'data': 'none'}
            else:
                #send a failure msg, js popup
                context = {'data': 'none'}
    return render(request, 'ForgotPassword.html', context)


def RequestMeeting(request):
    output = ''
    mentor_email = request.POST.get('t1')
    mentor_name = ''
    subject = 'Request for meeting from a startup'
    message = ''
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'bhararaarjun03', database = 'scaleup',charset='utf8')
    with con:            
        cur = con.cursor()
        cur.execute("select fname, lname from mentor where email='"+mentor_email+"'")
        rows = cur.fetchall()
        for row in rows:
            mentor_name = row[0]+" "+row[1]
        message = 'Hi '+mentor_name+',\n A startup named '+user.company_name+' which is currently developing itself in the domain of '+user.domain+' having '+str(user.emps)+' employees currently working with it has requested for a personal meeting with you.\nPlease contact the startup at the following email: '+user.email+' or '+user.poc_email+'.\n Detailed Description of Startup: '+user.descp+'\nWebsite : '+user.website+'.' 
        send_mail(subject, message,'scaleupstartups@zohomail.in',[mentor_email],fail_silently=False) #change it to mentor email, also change at other places to send to corresponding mails

    output='Sent a mail for meeting.'
    context={'data':output}
    return render(request, 'StartupScreen.html', context)    

