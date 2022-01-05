from django.shortcuts import render
from tkinter import filedialog

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from django.urls import reverse
import numpy as np
import plotly.offline as pyo
import sqlalchemy
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse


def feed(request):
    userdata = request.session.get('userdata')
    print(userdata)
    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()
    mycursor.execute("Select Year from bmsite_customers")
    year = mycursor.fetchall()
    print(year)
    mycursor.execute("Select bapunagar_customers from bmsite_customers where Year='2019'")
    data =mycursor.fetchone()
    print(data)
    mycursor.execute("Select bopal_customers from bmsite_customers where Year='2019'")
    data1 = mycursor.fetchone()
    print(data1)
    mycursor.execute("Select chandkheda_customers from bmsite_customers where Year='2019'")
    data2 = mycursor.fetchone()
    print(data2)
    mycursor.execute("Select gandhinagar_customers from bmsite_customers where Year='2019'")
    data3 = mycursor.fetchone()
    print(data3)
    mycursor.execute("Select gota_customers from bmsite_customers where Year='2019'")
    data4 = mycursor.fetchone()
    print(data4)
    mycursor.execute("Select isanpur_customers from bmsite_customers where Year='2019'")
    data5 = mycursor.fetchone()
    print(data5)
    mycursor.execute("Select lal_darwaja_customers from bmsite_customers where Year='2019'")
    data6 = mycursor.fetchone()
    print(data6)
    mycursor.execute("Select maninagar_customers from bmsite_customers where Year='2019'")
    data7 = mycursor.fetchone()
    print(data7)
    mycursor.execute("Select vastral_customers from bmsite_customers where Year='2019'")
    data8 = mycursor.fetchone()
    print(data8)

    records=(data,data1,data2,data3,data4,data5,data6,data7,data8)
    df = pd.DataFrame(records,columns=['Customers'])
    print(df)
    fig1 = go.Figure([go.Bar(x=['Bapunagar','Bopal','Chandkheda','Gandhinagar','Gota','Isanpur','Lal Darwaja','Maninagar,','Vastral'], y=df.Customers)])
    fig1.update_layout(

        xaxis_tickfont_size=14,
        xaxis=dict(
            title='Branches',

        ),
        yaxis=dict(
            type='linear',
            title='Customers',
            titlefont_size=16,
            tickfont_size=14,
        ),

    )
    plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)

    mycursor.execute("Select bapunagar_loans from bmsite_loans where Year='2019'")
    wdata = mycursor.fetchone()
    print(wdata)
    mycursor.execute("Select bopal_loans from bmsite_loans where Year='2019'")
    wdata1 = mycursor.fetchone()
    print(wdata1)
    mycursor.execute("Select chandkheda_loans from bmsite_loans where Year='2019'")
    wdata2 = mycursor.fetchone()
    print(wdata2)
    mycursor.execute("Select gandhinagar_loans from bmsite_loans where Year='2019'")
    wdata3 = mycursor.fetchone()
    print(wdata3)
    mycursor.execute("Select gota_loans from bmsite_loans where Year='2019'")
    wdata4 = mycursor.fetchone()
    print(wdata4)
    mycursor.execute("Select isanpur_loans from bmsite_loans where Year='2019'")
    wdata5 = mycursor.fetchone()
    print(wdata5)
    mycursor.execute("Select lal_darwaja_loans from bmsite_loans where Year='2019'")
    wdata6 = mycursor.fetchone()
    print(wdata6)
    mycursor.execute("Select maninagar_loans from bmsite_loans where Year='2019'")
    wdata7 = mycursor.fetchone()
    print(wdata7)
    mycursor.execute("Select vastral_loans from bmsite_loans where Year='2019'")
    wdata8 = mycursor.fetchone()
    print(wdata8)

    records = (wdata, wdata1, wdata2, wdata3, wdata4, wdata5, wdata6, wdata7, wdata8)
    df1 = pd.DataFrame(records, columns=['loans'])
    print(df1)
    fig2 = go.Figure([go.Bar(
        x=['Bapunagar', 'Bopal', 'Chandkheda', 'Gandhinagar', 'Gota', 'Isanpur', 'Lal Darwaja', 'Maninagar,',
           'Vastral'], y=df1.loans)])
    fig2.update_layout(

        xaxis_tickfont_size=14,
        xaxis=dict(
            title='Branches',

        ),
        yaxis=dict(
            type='linear',
            title='loans',
            titlefont_size=16,
            tickfont_size=14,
        ),

    )
    plot_div2 = pyo.plot(fig2, output_type='div', include_plotlyjs=True)
    context={
        'customer':plot_div1,
        'loans':plot_div2
    }
    return render(request, 'feed.html',context)




# Create your views here.
