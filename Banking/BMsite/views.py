from tkinter import filedialog
import pymysql
import tkinter as tk
from django.shortcuts import render
import mysql.connector
import csv, io
import pandas as pd
from django.contrib.auth.decorators import permission_required
from plotly.subplots import make_subplots
import plotly.offline as pyo
import sqlalchemy
import plotly.graph_objects as go
from . import models
from sqlalchemy import create_engine
import cherrypy
from django.contrib.auth.decorators import login_required
from .models import bm_problems
import datetime





# Create your views here.




@login_required
def Bankinfo(request,id):

    userdata= request.session.get('userdata')

    return render(request, "BM.html", userdata)
@login_required
def BMsheet(request):
    userdata = request.session.get('userdata')
    userdata['prompt'] = '(order of the csv should be Acct_branch Branch_Number Transaction_code Transaction_code_desc Post_date Amount Debit_Credit)'
    mydate = datetime.datetime.now()
    month1 = mydate.strftime("%b")
    print(month1)

    return render(request, "sheet.html", userdata)

@login_required
def sheetprocess(request):
    userdata=request.session.get('userdata')
    print(userdata['username'])


    if request.method == 'POST':
        empid=request.POST['emp_id']
        empid1=userdata['username']
        if empid == empid1:
            import_file_path = filedialog.askopenfilename()
            data = pd.read_csv(import_file_path)
            print(data)
            df = pd.DataFrame(data, columns=['Acct_branch', 'Branch_number', 'Transaction_code', 'Transaction_code_desc', 'Post_date','Amount','Debit_Credit'])
            print(df)
            print(userdata['branch'])

            ans1 = df.iloc[0]['Acct_branch']
            print(ans1)
            month = df.iloc[0]['Post_date']
            ans = month[3:6]
            print(ans)
            conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                           port='3306', auth_plugin='mysql_native_password')
            mycursor = conn.cursor()
            mycursor.execute("SELECT Post_date FROM bhqsite_branch_sheet")
            data1 = mycursor.fetchone()
            print(data1)

            def convertTuple(tup):
                str = ''.join(tup)
                return str

            # Driver code

            str = convertTuple(data1)
            print(str)
            ans2 = str[3:6]
            print(ans2)
            mydate = datetime.datetime.now()
            month1 = mydate.strftime("%b")
            print(month1)
            if month1 == ans2:
                if ans == ans2:
                    if userdata['branch'] == ans1:

                        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                                               .format(user="root", pw="bhavsardevin1993",
                                                       db="bank1"))
                        # Insert whole DataFrame into MySQL
                        df.to_sql('bhqsite_branch_sheet', con=engine, if_exists='append', chunksize=1000, index=False)
                        return render(request,'sheetdone.html',userdata)

                else:
                    userdata['prompt'] = '(order of the csv should be Acct_branch Branch_Number Transaction_code Transaction_code_desc Post_date Amount Debit_Credit)'
                    userdata['error'] = 'ERROR(Uploading different document)'
                    return render(request, 'sheet.html', userdata)

            elif month1 != ans2:
                if userdata['branch'] == ans1:

                    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                                           .format(user="root", pw="bhavsardevin1993",
                                                  db="bank1"))
                     #Insert whole DataFrame into MySQL
                    df.to_sql('bhqsite_branch_sheet', con=engine, if_exists='replace', chunksize=1000, index=True)
                    return render(request, 'sheetdone.html', userdata)

            else:
                userdata['prompt'] = '(order of the csv should be Acct_branch Branch_Number Transaction_code Transaction_code_desc Post_date Amount Debit_Credit)'
                userdata['error'] = 'ERROR(Uploading different document)'
                return render(request,'sheet.html',userdata)
        else:
            userdata['prompt'] = '(order of the csv should be Acct_branch Branch_Number Transaction_code Transaction_code_desc Post_date Amount Debit_Credit)'
            userdata['error'] = 'ERROR(Wrong username)'
            return render(request,"sheet.html",userdata)
    else:
        return render(request,'sheet.html',userdata)

@login_required
def sheetdone(request):
   userdata = request.session.get('userdata')

   return render(request,'BM.html',userdata)
@login_required
def requestform(request):
    userdata = request.session.get('userdata')
    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()
    if request.method =="POST":
        empid = request.POST['emp_id']
        email = request.POST['email']
        problem = request.POST['complain']
        empid1 = userdata['username']
        email1 = userdata['email']
        subject = request.POST['subject']
        if empid == empid1 and email == email1:
            branch1 = userdata['branch']
            sql="INSERT into bhqsite_bhq_problems(empid,email,branch,subject,problem) VALUES(%s,%s,%s,%s,%s)"
            data=(empid,email,branch1,subject,problem)
            mycursor.execute(sql,data)
            conn.commit()
            conn.close()

            userdata['message']='Request submitted successfully'
            return render(request,"BMissue.html",userdata)
        else:
            userdata['error2'] = 'ERROR(Empid or Email is incorrect)'
            return render(request,"BMissue.html",userdata)
    else:
        return render(request,"BMissue.html",userdata)


def bm_notification(request):
    userdata = request.session.get('userdata')
    branch1 = userdata['branch']

    if branch1 == 'Maninagar':
        data = bm_problems.objects.filter(branch='Maninagar')
        userdata['data_m'] = data
        return render(request,'BM_notification.html',userdata)
    elif branch1 == 'Bapunagar':
        data = bm_problems.objects.filter(branch='Bapunagar')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Bopal':
        data = bm_problems.objects.filter(branch='Bopal')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Chandkheda':
        data = bm_problems.objects.filter(branch='Chandkheda')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Gandhinagar':
        data = bm_problems.objects.filter(branch='Gandhinagar')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Gota':
        data = bm_problems.objects.filter(branch='Gota')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Isanpur':
        data = bm_problems.objects.filter(branch='Isanpur')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Lal Darwaja':
        data = bm_problems.objects.filter(branch='Lal Darwaja')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    elif branch1 == 'Vastral':
        data = bm_problems.objects.filter(branch='Vastral')
        userdata['data_m'] = data
        return render(request, 'BM_notification.html', userdata)
    else:
        return render(request,'BM_notification.html',userdata)

def BMdash(request):
    userdata = request.session.get('userdata')
    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()
    branch1 = userdata['branch']
    if branch1 == "Bapunagar":
        mycursor.execute("Select bapunagar_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select bapunagar_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data,columns=['Bapu_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bapu_loans'])
        print(df2)


        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bapu_customer, name="Customers"),
            secondary_y=False,
        )


        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bapu_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        ############################################################################################

        mycursor.execute("Select bapunagar_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Bapunagar_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1= make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request,'BMDash.html',userdata)

    elif branch1 == "Bopal":
        mycursor.execute("Select bopal_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select bopal_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        ######################################################
        mycursor.execute("Select bopal_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Bopal_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Chandkheda":
        mycursor.execute("Select chandkheda_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select chandkheda_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        #########################################################################
        mycursor.execute("Select chandkheda_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Chandkheda_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Gandhinagar":
        mycursor.execute("Select gandhinagar_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select gandhinagar_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        ###########################################################
        mycursor.execute("Select gandhinagar_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Gandhinagar_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Gota":
        mycursor.execute("Select gota_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select gota_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        ###############################################################
        mycursor.execute("Select gota_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Gota_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Maninagar":
        mycursor.execute("Select maninagar_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select maninagar_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        ########################################################
        mycursor.execute("Select maninagar_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Maninagar_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Isanpur":
        mycursor.execute("Select isanpur_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select isanpur_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        #########################################################
        mycursor.execute("Select isanpur_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Isanpur_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Lal Darwaja":
        mycursor.execute("Select lal_darwaja_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select lal_darwaja_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        #########################################################
        mycursor.execute("Select lal_darwaja_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Lal_Darwaja_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    elif branch1 == "Vastral":
        mycursor.execute("Select vastral_customers from bmsite_customers")
        data = mycursor.fetchall()
        print(data)
        mycursor.execute("Select Year from bmsite_customers")
        data1 = mycursor.fetchall()
        print(data1)
        mycursor.execute("Select vastral_loans from bmsite_loans")
        data2 = mycursor.fetchall()
        print(data2)

        df = pd.DataFrame(data, columns=['Bop_customer'])
        print(df)
        df1 = pd.DataFrame(data1, columns=['Year'])
        print(df1)
        df2 = pd.DataFrame(data2, columns=['Bop_loans'])
        print(df2)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df1.Year, y=df.Bop_customer, name="Customers"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=df1.Year, y=df2.Bop_loans, name="Loans"),
            secondary_y=True,
        )

        fig.update_xaxes(title_text="<b>Year</b>")

        fig.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig.update_yaxes(title_text="<b>Loans</b>", secondary_y=True, type="linear")

        plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        userdata['BMdash'] = plot_div
        ###############################################################
        mycursor.execute("Select vastral_customers from bmsite_customers")
        datac = mycursor.fetchall()
        print(datac)
        mycursor.execute("Select Year from bmsite_customers")
        data1c = mycursor.fetchall()
        print(data1c)
        mycursor.execute("Select Vastral_Deposits from bhqsite_deposits")
        data2c = mycursor.fetchall()
        print(data2c)

        dfc = pd.DataFrame(datac, columns=['Bapu_customer'])
        print(dfc)
        df1c = pd.DataFrame(data1c, columns=['Year'])
        print(df1c)
        df2c = pd.DataFrame(data2c, columns=['Bapu_Deposits'])
        print(df2c)

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=dfc.Bapu_customer, name="Customers"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x=df1c.Year, y=df2c.Bapu_Deposits, name="Deposits"),
            secondary_y=True,
        )

        fig1.update_xaxes(title_text="<b>Year</b>")

        fig1.update_yaxes(title_text="<b>Customers</b>", secondary_y=False, type="linear")
        fig1.update_yaxes(title_text="<b>Deposits</b>", secondary_y=True, type="linear")
        fig1.update_layout(
            width=1000,
            height=500,
        )

        plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

        userdata['BMdash1'] = plot_div1
        return render(request, 'BMDash.html', userdata)
    else:
        return render(request,'BMDash.html',userdata)


def bm_profile(request):
    userdata = request.session.get('userdata')

    return render(request,'BM_profile.html',userdata)







