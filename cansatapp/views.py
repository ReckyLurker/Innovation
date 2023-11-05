from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
import matplotlib.pyplot as plt
import io
import base64

# Create your views here.
def home(request):
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="NoNa#1401", database="innovation")
    mycursor=mydb.cursor()
    mycursor.execute("select * from innovation")
    myrecord=mycursor.fetchall()
    myrecord=myrecord[-5:]
    mycursor.reset()
    if myrecord is not None:
        dat=myrecord[-1][1]
        i1=dat.find("MQ7")
        i2=dat.find("PM25")
        nox=float(dat[6:i1-1])
        co=float(dat[i1+4:i2-1])
        pm=float(dat[i2+5:])
    else :
        co="-"
        nox="-"
        pm="-"
    
    time_l,co_l,nox_l,pm_l=[],[],[],[]
    for i in myrecord:
        time_l.append(i[0])
        i1=i[1].find("MQ7")
        i2=i[1].find("PM25")
        co_l.append(float(i[1][i1+4:i2-1]))
        nox_l.append(float(i[1][6:i1-1]))
        pm_l.append(float(i[1][i2+5:]))

    avg_co,avg_nox,avg_pm=0,0,0
    for i in myrecord[-2:]:
        i1=i[1].find("MQ7")
        i2=i[1].find("PM25")
        avg_co+=float(i[1][i1+4:i2-1])
        avg_nox+=float(i[1][6:i1-1])
        avg_pm+=float(i[1][i2+5:])
    avg_co/=2
    avg_nox/=2
    avg_pm/=2

    tco,tnox,tpm=5,5,5
    t_co,t_nox,t_pm=[],[],[]
    for i in range(5):
        t_co.append(tco)
        t_nox.append(tnox)
        t_pm.append(tpm)

    plt.plot(time_l,co_l,label="Concentration")
    plt.plot(time_l,t_co,label="Threshold Value")
    plt.xlabel('Time')
    plt.ylabel('CO Concentration')
    plt.legend()

    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    plt.close()

    plt.plot(time_l,nox_l,label="Concentration")
    plt.plot(time_l,t_nox,label="Threshold Value")
    plt.xlabel('Time')
    plt.ylabel('NOx Concentration')
    plt.legend()

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    plt.close()

    plt.plot(time_l,pm_l,label="Concentration")
    plt.plot(time_l,t_pm,label="Threshold Value")
    plt.xlabel('Time')
    plt.ylabel('Particulate Matter Concentration')
    plt.legend()

    buffer3 = io.BytesIO()
    plt.savefig(buffer3, format='png')
    plt.close()

    plot_co = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    plot_nox = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    plot_pm = base64.b64encode(buffer3.getvalue()).decode('utf-8')

    context={
        "co":co,
        "nox":nox,
        "pm":pm,
        'plot_co': plot_co,
        'plot_nox': plot_nox,
        'plot_pm': plot_pm,
        "tco":tco,
        "tpm":tpm,
        "tnox":tnox,
        "avgco":round(avg_co,2),
        "avgnox":round(avg_nox,2),
        "avgpm":round(avg_pm,2),
    }
    return render(request,"cansatapp/index.html",context)
