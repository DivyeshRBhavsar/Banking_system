import mysql.connector
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from.models import signup

from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required





def home(request):

    return render(request,'home.html')

def show_home(request):

    return render(request,'home.html')




def show_signup(request):

    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_pass']:
            try:

                user = User.objects.get(username=request.POST['emp_id'])
                print("username already exist")
                return render(request, 'sign up.html', {'message:"username is already exist'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['emp_id'], password=request.POST['password'],
                                                email=request.POST['email'],
                                                first_name=request.POST['fname'],last_name=request.POST['lname'])
                IR = request.POST['IR']
                branch = request.POST['branch']
                sign = signup(IR=IR,branch=branch , user=user)
                sign.save()
                context = {'message': 'successful signed up'}
                return render(request, 'home.html', context)

        else:

            return render(request, 'sign up.html', {'error': "password doesn't match"})

    else:

        return render(request, 'sign up.html')






def loginprocess(request):

        if request.method == "POST":

                uname = request.POST['emp_id']
                passwd = request.POST['password']
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    login(request,user)
                    print("logged in")
                    print(request.user.id)
                    cstid = request.user.id
                    cstobj = signup.objects.get(user_id=cstid)
                    print(cstobj.IR)
                    userdata = {'id': cstid,
                                'username': request.user.username,
                                'email': request.user.email,
                                'IR':cstobj.IR,
                                'branch':cstobj.branch,
                                'first_name':request.user.first_name,
                                'last_name':request.user.last_name
                                }
                    request.session['userdata'] = userdata
                    print(userdata)
                    return HttpResponseRedirect('profileuser')

                else:
                 print("incorect password")
                 context = {'message': 'Invalid Username & Password'}
                 return render(request, 'home.html', context)
        else:
            print("login page without post")
            return render(request, 'home.html')


@login_required
def profileuser(request):
    userdata=request.session.get('userdata')
    print(userdata)
    print(userdata['username'])
    if userdata['IR'] == 'Bank HQ':
        return render(request,'BHQ.html',userdata)
    elif userdata['IR'] == 'Branch Manager':
        return render(request, 'BM.html', userdata)
@login_required
def logoutprocess(request):

        request.session.flush()
        logout(request)
        print("logged out")
        return HttpResponseRedirect('show_home')




