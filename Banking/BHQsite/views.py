from tkinter import filedialog

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

from .models import Branch_Sheet
from django.urls import reverse
import numpy as np
import plotly.offline as pyo
import sqlalchemy
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots
from django.contrib.auth.decorators import login_required
from .decorator import role_required
from.models import bhq_problems




sns.set_style('darkgrid')

@login_required
@role_required(allowed_roles=["Bank HQ"])
def BHQ(request):


        return render(request,'BHQ.html')


@login_required
@role_required(allowed_roles=["Bank HQ"])
def BHQfeed(request):
    userdata = request.session.get('userdata')
    if request.method == 'POST':
        emp_id = request.POST['emp_id']
        subject = request.POST['subject']
        if subject == 'customers':
            import_file_path = filedialog.askopenfilename()
            data = pd.read_csv(import_file_path)
            print(data)
            df = pd.DataFrame(data,
                              columns=['Year', 'bapunagar_customers',	'bopal_customers',	'chandkheda_customers',	'gandhinagar_customers', 'gota_customers', 'isanpur_customers', 'lal_darwaja_customers', 'maninagar_customers', 'vastral_customers'])
            print(df)
            engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                                   .format(user="root", pw="bhavsardevin1993",
                                           db="bank1"))
            # Insert whole DataFrame into MySQL
            df.to_sql('bmsite_customers', con=engine, if_exists='replace', chunksize=2000, index=False)
            userdata['success'] = 'CSV file successfully submitted'

            return render(request,'BHQfeed.html',userdata)
        elif subject == 'loans':
            import_file_path = filedialog.askopenfilename()
            data = pd.read_csv(import_file_path)
            print(data)
            df = pd.DataFrame(data,
                              columns=['Year', 'bapunagar_loans', 'bopal_loans', 'chandkheda_loans',
                                       'gandhinagar_loans', 'gota_loans', 'isanpur_loans',
                                       'lal_darwaja_loans', 'maninagar_loans', 'vastral_loans'])
            print(df)
            engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                                   .format(user="root", pw="bhavsardevin1993",
                                           db="bank1"))
            # Insert whole DataFrame into MySQL
            df.to_sql('bmsite_loans', con=engine, if_exists='replace', chunksize=1000, index=False ,method='multi')
            userdata['success'] = 'CSV file successfully submitted'
            return render(request, 'BHQfeed.html', userdata)
        elif subject == 'deposits':
            import_file_path = filedialog.askopenfilename()
            data = pd.read_csv(import_file_path)
            print(data)
            df = pd.DataFrame(data,
                              columns=['Year', 'Bapunagar_Deposits', 'Bopal_Deposits', 'Chandkheda_Deposits',
                                       'Gandhinagar_Deposits', 'Gota_Deposits', 'Isanpur_Deposits',
                                       'Lal_Darwaja_Deposits', 'Maninagar_Deposits', 'Vastral_Deposits'])
            print(df)
            engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                                   .format(user="root", pw="bhavsardevin1993",
                                           db="bank1"))
            # Insert whole DataFrame into MySQL
            df.to_sql('bhqsite_deposits', con=engine, if_exists='replace', chunksize=1000, index=True,method='multi')
            userdata['success'] = 'CSV file successfully submitted'
            return render(request, 'BHQfeed.html', userdata)
        else:
            userdata['error3'] = 'You have not select any option'
            return render(request, 'BHQfeed.html',userdata)

    else:

        return render(request,'BHQfeed.html',userdata)


@login_required
@role_required(allowed_roles=["Bank HQ"])
def BHQdash(request):

        context = {
            'message2': 'Bank Headquarter',
            'message1': 'Greetings Bank HQ'
        }
        return render(request,"BHQdash.html",context)

@login_required
@role_required(allowed_roles=["Bank HQ"])
def BalanceSheet(request):

         return render(request,"BalanceData.html")

@login_required
@role_required(allowed_roles=["Bank HQ"])
def Balanceprocess(request):

        conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                       port='3306', auth_plugin='mysql_native_password')
        mycursor = conn.cursor()
        Data = Branch_Sheet.objects.all()
        print(Data)
        Data1 = Branch_Sheet.objects.filter(Acct_branch = 'Bapunagar')
        Data2 = Branch_Sheet.objects.filter(Acct_branch = 'Bopal')
        Data3 = Branch_Sheet.objects.filter(Acct_branch = 'Chandkheda')
        Data4 = Branch_Sheet.objects.filter(Acct_branch = 'Gandhinagar')
        Data5 = Branch_Sheet.objects.filter(Acct_branch = 'Gota')
        Data6 = Branch_Sheet.objects.filter(Acct_branch='Isanpur')
        Data7 = Branch_Sheet.objects.filter(Acct_branch='Lal Darwaja')
        Data8 = Branch_Sheet.objects.filter(Acct_branch='Maninagar')
        Data9 = Branch_Sheet.objects.filter(Acct_branch='vastral')



        records= {
            'data9': Data9,
            'data8': Data8,
            'data7': Data7,
            'data6': Data6,
            'data5': Data5,
            'data4': Data4,
            'data3': Data3,
            'data2': Data2,
            'data1': Data1,
            'data': Data

        }
        mycursor.execute("Select Amount from bhqsite_branch_sheet where Debit_credit='D' ")
        df = mycursor.fetchall()
        print(df)
        df_d = sum(map(sum, df))
        dfd = str(df_d)
        print(dfd)
        mycursor.execute("Select Amount from bhqsite_branch_sheet where Debit_credit='C' ")
        df1 = mycursor.fetchall()
        print(df1)
        df_c = sum(map(sum, df1))
        dfc = str(df_c)
        print(dfc)
        dfans = df_c - df_d
        records['dfans'] = dfans
        conn.close()

        return render(request, 'BalanceData.html', records)

@login_required
@role_required(allowed_roles=["Bank HQ"])
def Deposits(request):
    userdata = request.session.get('userdata')
    print(userdata['username'])
    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()
    mycursor.execute("Select Year from bhqsite_deposits")
    year = mycursor.fetchall()
    print(year)
    mycursor.execute("Select bapunagar_deposits from bhqsite_deposits")
    data = mycursor.fetchall()
    print(data)
    mycursor.execute("Select bopal_deposits from bhqsite_deposits")
    data1 = mycursor.fetchall()
    print(data1)
    mycursor.execute("Select chandkheda_deposits from bhqsite_deposits")
    data2 = mycursor.fetchall()
    print(data2)
    mycursor.execute("Select gandhinagar_deposits from bhqsite_deposits")
    data3 = mycursor.fetchall()
    print(data3)
    mycursor.execute("Select gota_deposits from bhqsite_deposits")
    data4 = mycursor.fetchall()
    print(data4)
    mycursor.execute("Select isanpur_deposits from bhqsite_deposits")
    data5 = mycursor.fetchall()
    print(data5)
    mycursor.execute("Select lal_darwaja_deposits from bhqsite_deposits")
    data6 = mycursor.fetchall()
    print(data6)
    mycursor.execute("Select maninagar_deposits from bhqsite_deposits")
    data7 = mycursor.fetchall()
    print(data7)
    mycursor.execute("Select vastral_deposits from bhqsite_deposits")
    data8 = mycursor.fetchall()
    print(data8)

    records = {
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6,
        'data7': data7,
        'data8': data8,

    }

    df = pd.DataFrame(data, columns=['bapunagar_deposits'])
    print(df)
    df1 = pd.DataFrame(data1,
                      columns=[ 'bopa_deposits'])
    print(df1)
    df2 = pd.DataFrame(data2,
                      columns=[ 'chandkheda_deposits'])
    print(df2)
    df3 = pd.DataFrame(data3,
                      columns=[ 'gandhinagar_deposits'])
    print(df3)
    df4 = pd.DataFrame(data4,
                      columns=['gota_deposits'])
    print(df4)
    df5 = pd.DataFrame(data5,
                      columns=[ 'isanpur_deposits'])
    print(df5)
    df6 = pd.DataFrame(data6,
                      columns=['lal_darwaja_deposits'])
    print(df6)
    df7 = pd.DataFrame(data7,
                      columns=[ 'maninagar_deposits'])
    print(df7)
    df8 = pd.DataFrame(data8,
                      columns=['vastral_deposits'])
    print(df8)

    df9 = pd.DataFrame(year,columns=['year'])
    print(df9)
    fig = go.Figure()

    fig['layout']['yaxis']['title'] = 'Deposits in Rs'
    fig.update_yaxes(type="linear")
    fig.update_xaxes(type="-")

    fig.add_trace(go.Scatter(x=df9.year, y=df.bapunagar_deposits,
                             mode='lines+markers',
                             name='Bapunagar(Deposits)',

                             ))
    fig.add_trace(go.Scatter(x=df9.year, y=df1.bopa_deposits,
                             mode='lines+markers',
                             name='Bopal(Deposits)',
                             ))
    fig.add_trace(go.Scatter(x=df9.year, y=df2.chandkheda_deposits,
                             mode='lines+markers', name='Chandkheda(Deposits)'))
    fig.add_trace(go.Scatter(x=df9.year, y=df3.gandhinagar_deposits,
                             mode='lines+markers', name='Gandhinagar(Deposits)'))
    fig.add_trace(go.Scatter(x=df9.year, y=df4.gota_deposits,
                             mode='lines+markers', name='Gota(Deposits)'))
    fig.add_trace(go.Scatter(x=df9.year, y=df5.isanpur_deposits,
                             mode='lines+markers', name='Isanpur(Deposits)'))
    fig.add_trace(go.Scatter(x=df9.year, y=df6.lal_darwaja_deposits,
                             mode='lines+markers', name='Lal Darwaja(Deposits)'))
    fig.add_trace(go.Scatter(x=df9.year, y=df7.maninagar_deposits,
                             mode='lines+markers', name='Maninagar(Deposits)'))
    fig.add_trace(go.Scatter(x=df9.year, y=df8.vastral_deposits,
                             mode='lines+markers', name='Vastral(Deposits)'))



    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=list(
                [dict(label='All',
                      method='update',
                      args=[{'visible': [True, True, True, True, True, True, True, True, True]},
                            {
                             'showlegend': True}]),
                 dict(label='Bapunagar',
                      method='update',
                      args=[{'visible': [True, False, False, False, False, False, False, False, False]},
                            # the index of True aligns with the indices of plot traces
                            {
                             'showlegend': True}]),
                 dict(label='Bopal',
                      method='update',
                      args=[{'visible': [False, True, False, False, False, False, False, False, False]},
                            {
                             'showlegend': True}]),
                 dict(label='Chandkheda',
                      method='update',
                      args=[{'visible': [False, False, True, False, False, False, False, False, False]},
                            {
                             'showlegend': True}]),
                 dict(label='Gandhinagar',
                      method='update',
                      args=[{'visible': [False, False, False, True, False, False, False, False, False]},
                            {
                             'showlegend': True}]),
                 dict(label='Gota',
                      method='update',
                      args=[{'visible': [False, False, False, False, True, False, False, False, False]},
                            {
                             'showlegend': True}]),
                 dict(label='Isanpur',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, True, False, False, False]},
                            {
                             'showlegend': True}]),
                 dict(label='Lal Darwaja',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, True, False, False]},
                            {
                             'showlegend': True}]),
                 dict(label='Maninagar',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, True, False]},
                            {
                             'showlegend': True}]),

                 dict(label='Vastral',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, False, True]},
                            {
                             'showlegend': True}]),

                 ])

        )
        ],height=500,
        showlegend=True,

    )

    plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=True)
    userdata['gdpgrowth'] = plot_div
    return render(request,'BHQ_deposits.html',userdata)

@login_required
@role_required(allowed_roles=["Bank HQ"])
def surplus(request):
    userdata = request.session.get('userdata')

    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()

    #Extract Debit of every branches

    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Bapunagar' and Debit_credit='D'")
    Bapu_d = mycursor.fetchall()
    print(Bapu_d)
    bapu_d = sum(map(sum, Bapu_d))
    Ba = str(bapu_d)
    print(Ba)

    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Bopal' and Debit_credit='D'")
    Bop_d = mycursor.fetchall()
    print(Bop_d)
    bop_d = sum(map(sum, Bop_d))
    Bo = str(bop_d)
    print(Bo)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Chandkheda' and Debit_credit='D'")
    Ch_d = mycursor.fetchall()
    print(Ch_d)
    ch_d= sum(map(sum, Ch_d))
    Ch = str(ch_d)
    print(Ch)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Gandhinagar' and Debit_credit='D'")
    Ga_d = mycursor.fetchall()
    print(Ga_d)
    ga_d = sum(map(sum, Ga_d))
    Ga = str(ga_d)
    print(Ga)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Gota' and Debit_credit='D'")
    Go_d = mycursor.fetchall()
    print(Go_d)
    go_d = sum(map(sum, Go_d))
    Go = str(go_d)
    print(Go)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Isanpur' and Debit_credit='D'")
    Is_d = mycursor.fetchall()
    print(Is_d)
    is_d = sum(map(sum, Is_d))
    Is = str(is_d)
    print(Is)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Lal Darwaja' and Debit_credit='D'")
    Ld_d = mycursor.fetchall()
    print(Ld_d)
    ld_d = sum(map(sum, Ld_d))
    Ld = str(ld_d)
    print(Ld)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Maninagar' and Debit_credit='D'")
    Mn_d = mycursor.fetchall()
    print(Mn_d)
    mn_d = sum(map(sum, Mn_d))
    Mn = str(mn_d)
    print(Mn)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='vastral' and Debit_credit='D'")
    Vs_d = mycursor.fetchall()
    print(Vs_d)
    vs_d = sum(map(sum, Vs_d))
    Vs = str(vs_d)
    print(Vs)
    data=[Ba,Bo,Ch,Ga,Go,Is,Ld,Mn,Vs]
    print(data)

    ###Extract of credit of every branches..
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Bapunagar' and Debit_credit='C'")
    Bapu_c = mycursor.fetchall()
    print(Bapu_c)
    bapu_c = sum(map(sum, Bapu_c))
    Bac = str(bapu_c)
    print(Bac)

    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Bopal' and Debit_credit='C'")
    Bop_c = mycursor.fetchall()
    print(Bop_c)
    bop_c = sum(map(sum, Bop_c))
    Boc = str(bop_c)
    print(Boc)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Chandkheda' and Debit_credit='C'")
    Ch_c = mycursor.fetchall()
    print(Ch_c)
    ch_c = sum(map(sum, Ch_c))
    Chc = str(ch_c)
    print(Chc)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Gandhinagar' and Debit_credit='C'")
    Ga_c = mycursor.fetchall()
    print(Ga_c)
    ga_c = sum(map(sum, Ga_c))
    Gac = str(ga_c)
    print(Gac)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Gota' and Debit_credit='C'")
    Go_c = mycursor.fetchall()
    print(Go_c)
    go_c = sum(map(sum, Go_c))
    Goc = str(go_c)
    print(Goc)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Isanpur' and Debit_credit='C'")
    Is_c = mycursor.fetchall()
    print(Is_c)
    is_c = sum(map(sum, Is_c))
    Isc = str(is_c)
    print(Isc)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Lal Darwaja' and Debit_credit='C'")
    Ld_c = mycursor.fetchall()
    print(Ld_c)
    ld_c = sum(map(sum, Ld_c))
    Ldc = str(ld_c)
    print(Ldc)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='Maninagar' and Debit_credit='C'")
    Mn_c = mycursor.fetchall()
    print(Mn_c)
    mn_c = sum(map(sum, Mn_c))
    Mnc = str(mn_c)
    print(Mnc)
    mycursor.execute("Select Amount from bhqsite_branch_sheet where Acct_branch='vastral' and Debit_credit='C'")
    Vs_c = mycursor.fetchall()
    print(Vs_c)
    vs_c = sum(map(sum, Vs_c))
    Vsc = str(vs_c)
    print(Vsc)
    data1 = [Bac, Boc, Chc, Gac, Goc, Isc, Ldc, Mnc, Vsc]
    print(data1)
    dat = {
        'debit': data,
        'credit': data1,
    }

    df = pd.DataFrame(dat,columns=['debit','credit'])
    print(df)
    df.head()
    ba_total = bapu_c - bapu_d
    bo_total = bop_c - bop_d
    ch_total = ch_c - ch_d
    ga_total = ga_c - ga_d
    go_total = go_c - go_d
    is_total = is_c - is_d
    ld_total = ld_c - ld_d
    mn_total = mn_c - mn_d
    vs_total = vs_c - vs_d


    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Bapunagar','Bopal','Chandkheda','Gandhinagar','Gota','Isanpur','Lal Darwaja','Maninagar','Vastral'],
                         y=df.debit,
                         name='Debit',
                         marker=dict(line=dict(width=0.5)),
                         marker_color='rgb(55, 83, 109)'
                         ))
    fig.add_trace(go.Bar(x=['Bapunagar','Bopal','Chandkheda','Gandhinagar','Gota','Isanpur','Lal Darwaja','Maninagar','Vastral'],
                         y=df.credit,
                         name='Credit',
                         marker=dict(line=dict(width=0.5)),
                         marker_color='rgb(26, 118, 255)'
                         ))

    bapu_annotations = [dict(x="Bapunagar",
                             y=bapu_c,
                             xref="x", yref="y",
                             text="Bapunagar:<br> %.2f" % ba_total,
                             ax=0, ay=-40,
                             xanchor='left',
                             yanchor='top'),
                       ]
    Bop_annotations = [dict(x="Bopal",
                             y=bop_c,
                             xref="x", yref="y",
                             text="Bopal:<br> %.2f" % bo_total,
                             ax=0, ay=-40,
                             xanchor='left',
                             yanchor='top'),
                        ]
    ch_annotations = [dict(x="Chandkheda",
                            y=ch_c,
                            xref="x", yref="y",
                            text="Chandkheda:<br> %.2f" % ch_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]
    ga_annotations = [dict(x="Gandhinagar",
                            y=ga_c,
                            xref="x", yref="y",
                            text="Gandhinagar:<br> %.2f" % ga_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]
    go_annotations = [dict(x="Gota",
                            y=go_c,
                            xref="x", yref="y",
                            text="Gota:<br> %.2f" % go_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]
    is_annotations = [dict(x="Isanpur",
                            y=is_c,
                            xref="x", yref="y",
                            text="Isanpur:<br> %.2f" % is_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]
    ld_annotations = [dict(x="Lal Darwaja",
                            y=ld_c,
                            xref="x", yref="y",
                            text="lal Darwaja:<br> %.2f" % ld_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]
    mn_annotations = [dict(x="Maninagar",
                            y=mn_c,
                            xref="x", yref="y",
                            text="Maninagar:<br> %.2f" % mn_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]
    vs_annotations = [dict(x="Vastral",
                            y=vs_c,
                            xref="x", yref="y",
                            text="Vastral:<br> %.2f" % vs_total,
                            ax=0, ay=-40,
                            xanchor='left',
                            yanchor='top'),
                       ]

    fig.update_layout(
        title='Daily ratio of D/C',
        xaxis_tickfont_size=14,
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Select",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Select",
                                "annotations": []}]),
                    dict(label="Bapunagar",
                         method="update",
                         args=[{"visible": [True, True,True]},
                               {"title": "Bapunagar(surplus)",
                                "annotations": bapu_annotations}]),
                    dict(label="Bopal",
                         method="update",
                         args=[{"visible": [True, True,True]},
                               {"title": "Bopal(surplus)",
                                "annotations": Bop_annotations}]),
                    dict(label="Chandkheda",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Chandkheda(surplus)",
                                "annotations": ch_annotations}]),
                    dict(label="Gandhinagar",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Gandhinagar(surplus)",
                                "annotations": ga_annotations}]),
                    dict(label="Gota",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Gota(surplus)",
                                "annotations": go_annotations}]),
                    dict(label="Isanpur",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Isanpur(surplus)",
                                "annotations": is_annotations}]),
                    dict(label="Lal Darwaja",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "lal darwaja(surplus)",
                                "annotations": ld_annotations}]),
                    dict(label="Maninagar",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Maninagar(surplus)",
                                "annotations": mn_annotations}]),
                    dict(label="Vastral",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Vastral(surplus)",
                                "annotations": vs_annotations}]),

                ]),
            )
        ],

        xaxis=dict(
          title='Branch'
        ),
        yaxis=dict(
            type='linear',
            title='Rupees',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        autosize=False,
        width=1000,
        height=500,
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    plot_div1 = pyo.plot(fig, output_type='div', include_plotlyjs=True)
    userdata['surplus'] = plot_div1

    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Bapunagar' and Debit_credit='D'")
    data1 = mycursor.fetchall()
    print(data1)
    mycursor.execute( "Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Bapunagar' and Debit_credit='C'")
    data2 = mycursor.fetchall()
    print(data2)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Bopal' and Debit_credit='D'")
    data3 = mycursor.fetchall()
    print(data3)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Bopal' and Debit_credit='C'")
    data4 = mycursor.fetchall()
    print(data4)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Chandkheda' and Debit_credit='D'")
    data5 = mycursor.fetchall()
    print(data5)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Chandkheda' and Debit_credit='C'")
    data6 = mycursor.fetchall()
    print(data6)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Gandhinagar' and Debit_credit='D'")
    data7 = mycursor.fetchall()
    print(data7)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Gandhinagar' and Debit_credit='C'")
    data8 = mycursor.fetchall()
    print(data8)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Gota' and Debit_credit='D'")
    data9 = mycursor.fetchall()
    print(data9)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Gota' and Debit_credit='C'")
    data10 = mycursor.fetchall()
    print(data10)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Isanpur' and Debit_credit='D'")
    data11 = mycursor.fetchall()
    print(data11)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Isanpur' and Debit_credit='C'")
    data12 = mycursor.fetchall()
    print(data12)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Lal Darwaja' and Debit_credit='D'")
    data13 = mycursor.fetchall()
    print(data13)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Lal Darwaja' and Debit_credit='C'")
    data14 = mycursor.fetchall()
    print(data14)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Maninagar' and Debit_credit='D'")
    data15 = mycursor.fetchall()
    print(data15)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Maninagar' and Debit_credit='C'")
    data16 = mycursor.fetchall()
    print(data16)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Vastral' and Debit_credit='D'")
    data17 = mycursor.fetchall()
    print(data17)
    mycursor.execute("Select Amount,Post_date from bhqsite_branch_sheet where Acct_Branch='Vastral' and Debit_credit='C'")
    data18 = mycursor.fetchall()
    print(data18)


    df1=pd.DataFrame(data1, columns=['Amount','Post_date'])
    print(df1)
    df2=pd.DataFrame(data2,columns=['Amount','Post_date'])
    print(df2)
    df3 = pd.DataFrame(data3, columns=['Amount', 'Post_date'])
    print(df3)
    df4 = pd.DataFrame(data4, columns=['Amount', 'Post_date'])
    print(df4)
    df5 = pd.DataFrame(data5, columns=['Amount', 'Post_date'])
    print(df5)
    df6 = pd.DataFrame(data6, columns=['Amount', 'Post_date'])
    print(df6)
    df7 = pd.DataFrame(data7, columns=['Amount', 'Post_date'])
    print(df7)
    df8 = pd.DataFrame(data8, columns=['Amount', 'Post_date'])
    print(df8)
    df9 = pd.DataFrame(data9, columns=['Amount', 'Post_date'])
    print(df9)
    df10 = pd.DataFrame(data10, columns=['Amount', 'Post_date'])
    print(df10)
    df11 = pd.DataFrame(data11, columns=['Amount', 'Post_date'])
    print(df11)
    df12 = pd.DataFrame(data12, columns=['Amount', 'Post_date'])
    print(df12)
    df13 = pd.DataFrame(data13, columns=['Amount', 'Post_date'])
    print(df13)
    df14 = pd.DataFrame(data14, columns=['Amount', 'Post_date'])
    print(df14)
    df15 = pd.DataFrame(data15, columns=['Amount', 'Post_date'])
    print(df15)
    df16 = pd.DataFrame(data16, columns=['Amount', 'Post_date'])
    print(df16)
    df17 = pd.DataFrame(data17, columns=['Amount', 'Post_date'])
    print(df17)
    df18 = pd.DataFrame(data18, columns=['Amount', 'Post_date'])
    print(df18)

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df1.Post_date,
        y=df1.Amount,
        name='Debit',
        marker=dict( line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df2.Post_date,
        y=df2.Amount,
        name='Credit',
        marker=dict( line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df3.Post_date,
        y=df3.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df4.Post_date,
        y=df4.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df5.Post_date,
        y=df5.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df6.Post_date,
        y=df6.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df7.Post_date,
        y=df7.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df8.Post_date,
        y=df8.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df9.Post_date,
        y=df9.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df10.Post_date,
        y=df10.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df11.Post_date,
        y=df11.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df12.Post_date,
        y=df12.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df13.Post_date,
        y=df13.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df14.Post_date,
        y=df14.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df15.Post_date,
        y=df15.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df16.Post_date,
        y=df16.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))
    fig1.add_trace(go.Bar(
        x=df17.Post_date,
        y=df17.Amount,
        name='Debit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(55, 83, 109)'
    ))
    fig1.add_trace(go.Bar(
        x=df18.Post_date,
        y=df18.Amount,
        name='Credit',
        marker=dict(line=dict(width=0.5)),

        marker_color='rgb(26, 118, 255)'
    ))

    fig1.update_layout(
        title='Daily ratio of D/C',
        xaxis_tickfont_size=14,
        xaxis=dict(
            title='Date',

        ),
        yaxis=dict(
            type='linear',
            title='Rupees',
            titlefont_size=16,
            tickfont_size=14,
        ),
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=list(
                [dict(label='All',
                      method='update',
                      args=[{'visible': [True, True, True, True, True, True, True, True, True,True, True, True, True, True, True, True, True, True]},
                            {
                             'showlegend': False}]),

                 dict(label='Bapunagar',
                      method='update',
                      args=[{'visible': [True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]},
                            # the index of True aligns with the indices of plot traces
                            {
                                'showlegend': True}]),
                 dict(label='Bopal',
                      method='update',
                      args=[{'visible': [False,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False]},
                            {
                                'showlegend': True}]),
                 dict(label='Chandkheda',
                      method='update',
                      args=[{'visible': [False, False,False,False, True, True, False, False, False, False, False, False,False,False,False,False,False,False]},
                            {
                                'showlegend': True}]),
                 dict(label='Gandhinagar',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, True,True, False, False,False,False,False,False,False,False,False,False]},
                            {
                                'showlegend': True}]),
                 dict(label='Gota',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, False,True,True,False,False,False,False,False,False,False,False]},
                            {
                                'showlegend': True}]),
                 dict(label='Isanpur',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, False,False,False,True,True,False,False,False,False,False,False]},
                            {
                                'showlegend': True}]),
                 dict(label='Lal Darwaja',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, False,False,False,False,False,True,True,False,False,False,False]},
                            {
                                'showlegend': True}]),
                 dict(label='Maninagar',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, False,False,False,False,False,False,False,True,True,False,False]},
                            {
                                'showlegend': True}]),

                 dict(label='Vastral',
                      method='update',
                      args=[{'visible': [False, False, False, False, False, False, False, False,False,False,False,False,False,False,False,False,True,True]},
                            {
                                'showlegend': True}]),

                 ])

        )
        ],
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        autosize=False,
        width=1000,
        height=500,
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    plot_div1 = pyo.plot(fig1, output_type='div', include_plotlyjs=True)
    userdata['datewise'] = plot_div1
    context={}

    if request.method == "POST":

        OR = request.POST['OR']
        print(OR)
        conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                       port='3306', auth_plugin='mysql_native_password')
        mycursor = conn.cursor()
        if OR == 'Bapunagar':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Bapunagar' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Bopal':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Bopal' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Chandkheda':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Chandkheda' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Gandhinagar':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Gandhinagar' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Gota':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Gota' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Isanpur':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Isanpur' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Lal Darwaja':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Lal Darwaja' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Maninagar':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='Maninagar' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)
        elif OR =='Vastral':
            mycursor.execute(
                "Select Amount, Post_date from bhqsite_branch_sheet where Acct_branch='vastral' and Debit_credit='D'")
            data = mycursor.fetchall()
            print(data)
            df = pd.DataFrame(data, columns=['Amount', 'Post_date'])
            print(df)
            aggregation_functions = {'Amount': 'sum', 'Post_date': 'first'}
            df_new = df.groupby('Post_date').aggregate(aggregation_functions)
            print(df_new)

            Ans = df_new.loc[df_new['Amount'].idxmax()]
            print(Ans.Post_date)

            userdata['Ans_bop'] = Ans.Post_date
            userdata['OR'] = OR

            return render(request,'surplus.html',userdata)

    return render(request, 'surplus.html',userdata)

@login_required
@role_required(allowed_roles=["Bank HQ"])
def request1(request):
    userdata = request.session.get('userdata')
    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()
    if request.method =="POST":
        empid = request.POST['empid']
        problem = request.POST['request']
        empid1 = userdata['username']
        subject = request.POST['subject']
        branch = request.POST['branch']
        if empid == empid1:

            sql="INSERT into bmsite_bm_problems(empid,branch,subject,request) VALUES(%s,%s,%s,%s)"
            data=(empid,branch,subject,problem)
            mycursor.execute(sql,data)
            conn.commit()
            conn.close()

            userdata['message']='Request submitted successfully'
            return render(request,"BHQrequest.html",userdata)
        else:
            userdata['error2'] = 'ERROR(Emp id is incorrect)'
            return render(request,"BHQrequest.html",userdata)
    else:
        return render(request,"BHQrequest.html",userdata)



@login_required
@role_required(allowed_roles=["Bank HQ"])
def notification(request):
    userdata = request.session.get('userdata')

    data = bhq_problems.objects.filter()
    print(data)
    userdata['data'] = data
    return render(request,'BHQ_notification.html',userdata)

def delete(request):
    userdata = request.session.get('userdata')
    data1 = bhq_problems.objects.filter()
    if request.method == "POST":
        pi = bhq_problems.objects.get(pk=id)
        bhq_problems.objects.filter(id=id).update(status="1")
        #pi.delete()
    return render(request,'BHQ_notification.html',userdata)

@login_required
@role_required(allowed_roles=["Bank HQ"])
def branch_efficiency(request):
    userdata = request.session.get('userdata')
    conn = mysql.connector.connect(database="bank1", user='root', password='bhavsardevin1993', host='127.0.0.1',
                                   port='3306', auth_plugin='mysql_native_password')
    mycursor = conn.cursor()


    mycursor.execute("SELECT * FROM (SELECT * FROM bmsite_loans ORDER BY id DESC LIMIT 2) sub ORDER BY id ASC")
    dt = mycursor.fetchall()
    print(dt)
    df= pd.DataFrame(dt,columns=['id','year','bapu_l','bop_l','cha_l','gan_l','got_l','isa_l','dar_l','man_l','vas_l'])
    print(df)
    Bapu_l = df.iloc[1]['bapu_l']
    Bop_l = df.iloc[1]['bop_l']
    Cha_l = df.iloc[1]['cha_l']
    Gan_l = df.iloc[1]['gan_l']
    Got_l = df.iloc[1]['got_l']
    Isa_l = df.iloc[1]['isa_l']
    Dar_l = df.iloc[1]['dar_l']
    Man_l = df.iloc[1]['man_l']
    Vas_l = df.iloc[1]['vas_l']
    loan =[Bapu_l,Bop_l,Cha_l,Gan_l,Got_l,Isa_l,Dar_l,Man_l,Vas_l]
    Branch =['Bapunagar','Bopal','Chandkheda','Gandhinagar','Gota','Isanpur','Lal_Darwaja','Maninagar','Vastral']
    records={
        'branch': Branch,
        'loan':loan,

    }
    df1 = pd.DataFrame(records,columns=['branch','loan'])
    print(df1)
    df1.sort_values(by=['loan'], inplace=True, ascending=False)
    print(df1)
    print(df1.to_dict("list"))

    data_first = df1.iloc[0]['loan']
    print(data_first)
    userdata['loan_first'] = data_first
    data_second = df1.iloc[1]['loan']
    print(data_second)
    userdata['loan_second'] = data_second
    data_third = df1.iloc[2]['loan']
    print(data_third)
    userdata['loan_third'] = data_third
    data_fourth = df1.iloc[3]['loan']
    print(data_fourth)
    userdata['loan_fourth'] = data_fourth
    data_fifth = df1.iloc[4]['loan']
    print(data_fifth)
    userdata['loan_fifth'] = data_fifth
    data_sixth = df1.iloc[5]['loan']
    print(data_sixth)
    userdata['loan_sixth'] = data_sixth
    data_seventh = df1.iloc[6]['loan']
    print(data_seventh)
    userdata['loan_seventh'] = data_seventh
    data_eighth = df1.iloc[7]['loan']
    print(data_eighth)
    userdata['loan_eighth'] = data_eighth
    data_ninth = df1.iloc[8]['loan']
    print(data_ninth)
    userdata['loan_ninth'] = data_ninth

    userdata['branch_first'] = df1.iloc[0]['branch']
    userdata['branch_second'] = df1.iloc[1]['branch']
    userdata['branch_third'] = df1.iloc[2]['branch']
    userdata['branch_fourth'] = df1.iloc[3]['branch']
    userdata['branch_fifth'] = df1.iloc[4]['branch']
    userdata['branch_sixth'] = df1.iloc[5]['branch']
    userdata['branch_seventh'] = df1.iloc[6]['branch']
    userdata['branch_eighth'] = df1.iloc[7]['branch']
    userdata['branch_ninth'] = df1.iloc[8]['branch']

    Bapu_l = df.iloc[0]['bapu_l']
    Bop_l = df.iloc[0]['bop_l']
    Cha_l = df.iloc[0]['cha_l']
    Gan_l = df.iloc[0]['gan_l']
    Got_l = df.iloc[0]['got_l']
    Isa_l = df.iloc[0]['isa_l']
    Dar_l = df.iloc[0]['dar_l']
    Man_l = df.iloc[0]['man_l']
    Vas_l = df.iloc[0]['vas_l']
    loan = [Bapu_l, Bop_l, Cha_l, Gan_l, Got_l, Isa_l, Dar_l, Man_l, Vas_l]
    Branch = ['Bapunagar', 'Bopal', 'Chandkheda', 'Gandhinagar', 'Gota', 'Isanpur', 'Lal_Darwaja', 'Maninagar',
              'Vastral']
    records = {
        'branch': Branch,
        'loan': loan,

    }
    df2 = pd.DataFrame(records, columns=['branch', 'loan'])
    print(df2)
    df2.sort_values(by=['loan'], inplace=True, ascending=False)
    print(df2)

    print(df2.to_dict("list"))

    ##########################################################################################

    mycursor.execute("SELECT * FROM (SELECT * FROM bmsite_customers ORDER BY id DESC LIMIT 2) sub ORDER BY id ASC")
    dt = mycursor.fetchall()
    print(dt)
    df3 = pd.DataFrame(dt,
                      columns=['id', 'year', 'bapu_c', 'bop_c', 'cha_c', 'gan_c', 'got_c', 'isa_c', 'dar_c', 'man_c',
                               'vas_c'])
    print(df3)
    Bapu_c = df3.iloc[1]['bapu_c']
    Bop_c = df3.iloc[1]['bop_c']
    Cha_c = df3.iloc[1]['cha_c']
    Gan_c = df3.iloc[1]['gan_c']
    Got_c = df3.iloc[1]['got_c']
    Isa_c = df3.iloc[1]['isa_c']
    Dar_c = df3.iloc[1]['dar_c']
    Man_c = df3.iloc[1]['man_c']
    Vas_c = df3.iloc[1]['vas_c']
    customers = [Bapu_c, Bop_c, Cha_c, Gan_c, Got_c, Isa_c, Dar_c, Man_c, Vas_c]
    Branch = ['Bapunagar', 'Bopal', 'Chandkheda', 'Gandhinagar', 'Gota', 'Isanpur', 'Lal_Darwaja', 'Maninagar',
              'Vastral']
    records = {
        'branch': Branch,
        'customers': customers,

    }
    df4 = pd.DataFrame(records, columns=['branch', 'customers'])
    print(df4)
    df4.sort_values(by=['customers'], inplace=True, ascending=False)
    print(df4)
    print(df4.to_dict("list"))

    data_first1 = df4.iloc[0]['customers']
    print(data_first1)
    userdata['customers_first'] = data_first1
    data_second2 = df4.iloc[1]['customers']
    print(data_second2)
    userdata['customers_second'] = data_second2
    data_third3 = df4.iloc[2]['customers']
    print(data_third3)
    userdata['customers_third'] = data_third3
    data_fourth4 = df4.iloc[3]['customers']
    print(data_fourth4)
    userdata['customers_fourth'] = data_fourth4
    data_fifth5 = df4.iloc[4]['customers']
    print(data_fifth5)
    userdata['customers_fifth'] = data_fifth5
    data_sixth6 = df4.iloc[5]['customers']
    print(data_sixth6)
    userdata['customers_sixth'] = data_sixth6
    data_seventh7 = df4.iloc[6]['customers']
    print(data_seventh7)
    userdata['customers_seventh'] = data_seventh7
    data_eighth8 = df4.iloc[7]['customers']
    print(data_eighth8)
    userdata['customers_eighth'] = data_eighth8
    data_ninth9 = df4.iloc[8]['customers']
    print(data_ninth9)
    userdata['customers_ninth'] = data_ninth9

    userdata['branch_first1'] = df4.iloc[0]['branch']
    userdata['branch_second2'] = df4.iloc[1]['branch']
    userdata['branch_third3'] = df4.iloc[2]['branch']
    userdata['branch_fourth4'] = df4.iloc[3]['branch']
    userdata['branch_fifth5'] = df4.iloc[4]['branch']
    userdata['branch_sixth6'] = df4.iloc[5]['branch']
    userdata['branch_seventh7'] = df4.iloc[6]['branch']
    userdata['branch_eighth8'] = df4.iloc[7]['branch']
    userdata['branch_ninth9'] = df4.iloc[8]['branch']

    Bapu_l = df.iloc[0]['bapu_l']
    Bop_l = df.iloc[0]['bop_l']
    Cha_l = df.iloc[0]['cha_l']
    Gan_l = df.iloc[0]['gan_l']
    Got_l = df.iloc[0]['got_l']
    Isa_l = df.iloc[0]['isa_l']
    Dar_l = df.iloc[0]['dar_l']
    Man_l = df.iloc[0]['man_l']
    Vas_l = df.iloc[0]['vas_l']
    loan = [Bapu_l, Bop_l, Cha_l, Gan_l, Got_l, Isa_l, Dar_l, Man_l, Vas_l]
    Branch = ['Bapunagar', 'Bopal', 'Chandkheda', 'Gandhinagar', 'Gota', 'Isanpur', 'Lal_Darwaja', 'Maninagar',
              'Vastral']
    records = {
        'branch': Branch,
        'loan': loan,

    }
    df2 = pd.DataFrame(records, columns=['branch', 'loan'])
    print(df2)
    df2.sort_values(by=['loan'], inplace=True, ascending=False)
    print(df2)

    print(df2.to_dict("list"))

    ##################################################################################

    mycursor.execute("Select Maninagar_Deposits from bhqsite_deposits where Year='2019'")
    man_d = mycursor.fetchone()
    print(man_d)
    return render(request,'branch_efficiency.html',userdata)

@login_required
@role_required(allowed_roles=["Bank HQ"])
def BHQ_profile(request):
    userdata = request.session.get('userdata')
    print(userdata)

    return render(request,'BHQ_profile.html',userdata)
















