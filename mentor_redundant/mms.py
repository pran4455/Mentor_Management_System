from validation import *
from mentee import Mentee
from mentor import Mentor
import json
import pickle
from meeting import *
from flask import Flask, render_template, request,session,redirect,url_for
from templates import *
from validation import * 
from quickstart import *
from allocation import *
from catmark import *
import json
'''
In each dashboard have a logout button
'''

app = Flask(__name__)
app.secret_key = 'pompom'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def render_login_page():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        print(user_id,password)
        session['username'] = user_id
        # Validate user ID using regex
        user_strategy = RegexusernameValidation()
        password_strategy = RegexPasswordValidation()

        password_context = ValidationContext(password_strategy, password)
        user_context = ValidationContext(user_strategy,user_id)
        print(password_context.validate(),user_context.validate())
        if not (password_context.validate() and user_context.validate()):
              error = "Invalid Username Or Password"
        else:
          with open('users.json','r') as f1:
                userdata =json.load(f1)
                for user in userdata:
                    if user == user_id and userdata[user][1]==password:
                        if userdata[user][0]=='admin':
                            return render_template('admin.html')
                        elif userdata[user][0]=='mentee':
                            return redirect(url_for('mentee'))
                        elif userdata[user][0]=='mentor':
                            return render_template('mentor.html')
                    else:
                         error="Invalid Credentials"
        return render_template('login2.html',error=error)
               
    
    return render_template('login2.html')

@app.route('/addmentor',methods=['GET','POST'])
def addMentor():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        names=request.form['names']
        contactno=request.form['contactno']
        department=request.form['department']
        user_strategy = RegexusernameValidation()
        password_strategy = RegexPasswordValidation()

        password_context = ValidationContext(password_strategy, password)
        user_context = ValidationContext(user_strategy,username)

        if not password_context.validate():
              error1 = "Invalid Password"
              return render_template('addmentor.html',error1=error1)
        if not (user_context.validate()):
            error = "Invalid Username"
            return render_template('addmentor.html',error=error)
        if (password_context.validate() and user_context.validate()):
                # Check if the username and password already exist in users.json
            with open('users.json', 'r') as f2:
                userdata = json.load(f2)
                if username in userdata and userdata[username] == password:
                    # Username and password already exist, render template with an error
                    error_username = "Credentials already exists.Use different credentials"
                    return render_template('addmentor.html', error_username=error_username)

            # Username and password do not exist, proceed with mentor registration
            mentor = Mentor(username, password, names, contactno, department)
            with open("mentor.pkl", "rb") as f1:
                data=pickle.load(f1)
                data.append(mentor)
            with open("mentor.pkl", "wb") as f2:
                pickle.dump(data,f2)

            # Also update users.json
            with open('users.json', 'r') as f2:
                userdata = json.load(f2)
            userdata[username] = ('mentor',password)
            with open('users.json', 'w') as f2:
                json.dump(userdata, f2)
            send_message(service,username,'Mentor in MentorU', 
            f'You have been successfully added as a mentor to MentorU.\n Username:{username}\nPassword:{password}')
            return render_template('completedadmin.html')


    return render_template('addmentor.html')

@app.route('/addmentee',methods=['GET','POST'])
def addMentee():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        names=request.form['names']
        contactno=request.form['contactno']
        year=request.form['year']
        department=request.form['department']
        user_strategy = RegexusernameValidation()
        password_strategy = RegexPasswordValidation()

        password_context = ValidationContext(password_strategy, password)
        user_context = ValidationContext(user_strategy,username)

        if not password_context.validate():
              error1 = "Invalid Password"
              return render_template('addmentee.html',error1=error1)
        
        if not (user_context.validate()):
            error = "Invalid Username"
            return render_template('addmentee.html',error=error)
        
        if (password_context.validate() and user_context.validate()):

                # Check if the username and password already exist in users.json
            with open('users.json', 'r') as f2:
                userdata = json.load(f2)
                if username in userdata and userdata[username] == password:
                    # Username and password already exist, render template with an error
                    error_username = "Credentials already exists.Use different credentials"
                    return render_template('addmentee.html', error_username=error_username)

            # Username and password do not exist, proceed with mentee registration
            mentee = Mentee(username, password, names, contactno,year, department)
            with open("mentee.pkl", "rb") as f1:
                data=pickle.load(f1)
                data.append(mentee)

            with open("mentee.pkl", "wb") as f2:
                pickle.dump(data,f2)

            # Also update users.json
            with open('users.json', 'r') as f2:
                userdata = json.load(f2)

            userdata[username] = ('mentee',password)
            with open('users.json', 'w') as f2:
                json.dump(userdata, f2)

            send_message(service,username,'Mentee in MentorU', 
            f'You have been successfully added as a mentee in MentorU.\n Username:{username}\nPassword:{password}')
            
            with open('markentry.json','r')  as f9:
                    data=json.load(f9)
            data[username]=[0,0,0,0,0,0,0,0]
            with open('markentry.json','w')  as f8:
                    json.dump(data,f8)
            return render_template('completedadmin.html')
    

    return render_template('addmentee.html')

@app.route('/assign')
def assign():

    with open('mentor.pkl','rb') as f2:
            mentor_data=pickle.load(f2)
            print(mentor_data)
    for i in mentor_data:
        i.mentees=[]
    with open('mentee.pkl','rb') as f1:
                allocate=[]
            
                mentees=pickle.load(f1)
                updatedmentees=[]
                for userdata in mentees:
                    print(type(userdata.year))
                    if userdata.year=='1':
                        print(1)
                        a=AnyMentorAllocationStrategy()
                    else:
                        print(2)
                        a=DepartmentMentorAllocationStrategy()
                    
                    a2=allocationContext(a,userdata,mentor_data)
                    a1=a2.allocate_mentor()

                    if a1!=None:
                            index=mentor_data.index(a1)
                            a1.mentees.append(userdata)
                            mentor_data[index]=a1

                    if userdata.currentmentor!=None and userdata.currentmentor not in userdata.pastmentor:
                            userdata.pastmentor.append(userdata.currentmentor)
                            userdata.currentmentor=a1
                            print(userdata.names,a1.names,userdata.currentmentor,userdata.pastmentor,a1.mentees)
                    else:
                        userdata.currentmentor=a1
                        print(userdata.names,a1.names,userdata.currentmentor,userdata.pastmentor,a1.mentees)
                    allocate.append((userdata,a1))
                    body=f'Dear Mentee,\nYou have been assigned to Mentor {a1.names}\nEmail:{a1.username}\nThank You'
                    send_message(service,userdata.username,'Mentor Allocation',body)
                    updatedmentees.append(userdata)
                    print(updatedmentees)

                with open('mentee.pkl','wb') as f6:
                        pickle.dump(updatedmentees,f6)

                with open('mentor.pkl','wb') as f4:
                        pickle.dump(mentor_data,f4)
                
                with open('allocation.pkl','wb') as f5:
                       pickle.dump(allocate,f5)
               
    return render_template('completedadmin.html')


@app.route('/schedulemeeting',methods=['GET','POST'])
def schedulemeeting():
    with open('mentor.pkl','rb') as f:
        data=pickle.load(f)
        r=Meeting()
        m=[]
        for i in data:
            #mentor 
            if i.username==session.get('username'):
                    name=i.names#mentor name
                    for user in i.mentees:#mentees
                        m.append(user.username)#mentee username appending
                        r.addMentee(user)

    if request.method=='POST':
        mentee=request.form['mentee_list']
        link=request.form['meeting_link']
        date=request.form['meeting_date']
            
        if mentee=='ALL':
                body=f'Dear Mentee,The below Meeting is scheduled to take place on {date}'+f'\nMeeting Link:{link}'+f'\nThanks in Advance\nWith regards\n{name}'
                r.alert_mentees('Meeting request',body)

        else: 
                body=f'Dear Mentee,The below Meeting is scheduled to take place on {date}'+f'\nMeeting Link:{link}'+f'\nThanks in Advance\nWith regards\n{name}'
                send_message(service,mentee,'Meeting request',body) 
        render_template('completedmentor.html')  
    return render_template('schedulemeeting.html',mentees=m)

#viewmentees have back to home
@app.route('/viewmentees')
def viewmentees():
    with open('mentor.pkl','rb') as f:
        data=pickle.load(f)
        for i in data:
            if i.username==session.get('username'):
                    mentees=i.mentees

    return render_template('viewmentees.html',mentees=mentees)

@app.route('/requestmark')
def requestmark():
    return render_template('catmark.html')

@app.route('/sendemail',methods=['GET','POST'])
def sendemail():
        print('in')
        with open('mentor.pkl','rb') as f:
            data=pickle.load(f)
            for i in data:
                if i.username==session.get('username'):
                   mentees=i.mentees
                   mentor=i
                   print(mentor,mentees)
                   break
        print(mentor)
        print(mentor.names)
        index=data.index(mentor)
        newmentor=None
        if request.method=='POST':
            msg=request.form['message']
            print(mentor.names)
            mentor.control=mentor.control.send_email(mentees,msg)
            newmentor=mentor
        print(mentor.control.enable_command.mentee_button.is_enabled())
        data[index]=newmentor
        print(newmentor.control.enable_command.mentee_button.is_enabled())
        for i in data:
             print(i.username,i.control.enable_command.mentee_button.is_enabled())
        with open('mentor.pkl','wb') as f8:
            pickle.dump(data,f8)
            
        return render_template('completedmentor.html')

#correct it while doing mark entry
@app.route('/disable')
def disable():
        print('in')
        with open('mentor.pkl','rb') as f:
            data=pickle.load(f)
            for i in data:
                if i.username==session.get('username'):
                   mentees=i.mentees
                   mentor=i
                   print(mentor,mentees)
                   break
        print(mentor.names)
        index=data.index(mentor)
        print(mentor.names)
        mentor.control=mentor.control.disable_button()
        newmentor=mentor
        print('enabled:',mentor.control.enable_command.mentee_button.is_enabled())
        print('disabled:',mentor.control.disable_command.mentee_button.is_enabled())
        data[index]=newmentor
        print(newmentor.control.disable_command.mentee_button.is_enabled())
        for i in data:
             print(i.username,i.control.disable_command.mentee_button.is_enabled())
        with open('mentor.pkl','wb') as f8:
            pickle.dump(data,f8)
            
        return render_template('completedmentor.html')

@app.route('/requestmeeting',methods=['GET','POST'])
def requestmeeting():
    if request.method=='POST':
        msg=request.form['message']
        with open('mentee.pkl','rb') as f:
            data=pickle.load(f)
            for i in data:
                if i.username==session.get('username'):
                   mentee=i
                   break
        print(mentee.names)
        send_message(service,mentee.currentmentor.username,f'Request for meeting from mentee {mentee.names}',msg+f'\nmentee username:+' '+{mentee.username}')
        return render_template('completed.html')
    
    return render_template('requestmeeting.html')

@app.route('/goback')
def goback():
    with open('mentee.pkl','rb') as f:
            data=pickle.load(f)
            for i in data:
                if i.username==session.get('username'):
                   mentee=i
                   mentor=i.currentmentor
                   break
    with open('mentor.pkl','rb') as f8:
         data=pickle.load(f8)
         for j in data:
              if j.username==mentor.username:
                   actualmentorobj=j
    print(actualmentorobj.control.enable_command.mentee_button.is_enabled())
    return render_template('mentee.html', is_mentee_button_enabled=actualmentorobj.control.enable_command.mentee_button.is_enabled())



@app.route('/mentee',methods=['GET','POST'])
def mentee():
    print('in')
    with open('mentee.pkl','rb') as f:
            data=pickle.load(f)
            for i in data:
                if i.username==session.get('username'):
                   mentee=i
                   mentor=i.currentmentor
                   break
    with open('mentor.pkl','rb') as f8:
         data=pickle.load(f8)
         for j in data:
              if j.username==mentor.username:
                   actualmentorobj=j
    print(actualmentorobj.control.enable_command.mentee_button.is_enabled())
    return render_template('mentee.html', is_mentee_button_enabled=actualmentorobj.control.enable_command.mentee_button.is_enabled())

@app.route('/markentry',methods=['GET','POST'])
def markentry():
    if request.method=='POST':
        print('inside markentry if statement')
        username=session.get('username')
        mark=request.form['mark']
        with open('markentry.json','r') as f1:
            data=json.load(f1)
        index=data[username].index(0)
        print(index)
        data[username][index]=int(mark)
        print(data[username][index])
        with open('markentry.json','w') as f2:
            data=json.dump(data,f2)
        return render_template('completed.html')
    return render_template('markentry.html')

@app.route('/viewmarks',methods=['GET'])
def viewmarks():
    username=session.get('username')
    with open('mentor.pkl','rb') as g:
        data=pickle.load(g)
        for i in data:
              if i.username==username:#mentor username
                   mentees=i.mentees
                   break
    mentee_dets=[]
    #names,username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8
    with open('markentry.json','r')   as g1:
        userdata=json.load(g1)
    for mentee in mentees:
        mentee_dets.append([mentee.names,mentee.username]+userdata[mentee.username])

    return render_template('viewmarks.html',mentees=mentee_dets)

@app.route('/gobackmentee')
def gobackmentee():
     return render_template('mentee.html')             

@app.route('/gobackmentor')
def gobackmentor():
     return render_template('mentor.html')

@app.route('/gobackadmin')
def gobackadmin():
     return render_template('admin.html')

@app.route('/assignedmentees')
def assignedmentees():
    with open('mentor.pkl','rb') as g:
        data=pickle.load(g)
    allocate={}
    for mentor in data:
        mentees=[]
        for mentee in mentor.mentees:
            mentees.append(mentee.names)
        allocate[mentor.names]=mentees
    print(allocate)
    return render_template('viewmentormentee.html',mentor_mentee_dict=allocate)

@app.route('/report')
def report():
    with open('markentry.json','r') as f:
        userdata=json.load(f)
    
    with open('mentor.pkl','rb') as g:
        mentordata=pickle.load(g) 
    list_marks=[]
    mentors=[]
    
    for i in mentordata:
        mentors.append(i.username)
        add=0
        ct=0
        for j in i.mentees:#mentees
            mark=userdata[j.username]#mark of each mentee
            print(j.username,mark)
            add+=sum(mark)
            ct+=1
            print(j.username,ct)
        if ct==0:
             list_marks.append(ct)
        else:
            list_marks.append(add/(ct*8))
    return render_template('graph.html',mentors=mentors,marks=list_marks)

def rough():
    with open('mentee.pkl','rb') as f1:
        data=pickle.load(f1)
    markentry={}
    for i in data:
        markentry[i.username]=[0,0,0,0,0,0,0,0]
    
    with open('markentry.json','w')  as f2:
        json.dump(markentry,f2)
@app.route('/logout')
def logout():
     return render_template('login2.html')
def fileinst():
    with open('mentee.pkl','wb') as f1:
        pickle.dump([],f1)
    with open('mentor.pkl','wb') as f2:
        pickle.dump([],f2)
if __name__=='__main__':
    app.run(debug=True)
