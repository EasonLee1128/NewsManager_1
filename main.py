from flask import Flask, render_template, request,url_for,redirect
from datetime import datetime
#import time
import sqlite3
import pandas as pd
from pandas import DataFrame


app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('./news20210819.db')
    cursor = conn.cursor() 
    cursor = conn.execute("SELECT * from NEWSTABLE")
    readData = cursor.fetchall()
    readDataDf = DataFrame(readData)
    
    #readDataDf['Datetime'] = pd.to_datetime(readDataDf[3])
    
    #readDataDf['Date'] =(readDataDf.Date)
    #readDataDf.sort_values(by=[3]) # This now sorts in date order
    
    readDataDf =readDataDf.sort_values(by=[3])
   
    #readDataDf.pop(0)
    readData = readDataDf.values.tolist()
    length = len(readData)
    #title = readData[0][0]    
    readData = readData[::-1]
    #reversed_readData = readData.iloc[::-1]
    
    return render_template("index.html", **locals())




@app.route('/addcreatnews',methods = ['POST'])
def addcreatnews():
    
    
    
    
    conn = sqlite3.connect('./news20210819.db')
    query = '''INSERT INTO NEWSTABLE (title,author, news_datetime,content)
          VALUES ( :title, :author, :news_datetime, :content);'''

#query = ('INSERT INTO STUDENT (title,author, news_datetime,content)'
 #         'VALUES ( :title, :author, :news_datetime, :content);')
    title = request.values['title']
    author = request.values['author']
    content = request.values['content']
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    news_datetime = now
     
    params = {    
        'title': title,
        'author': author,
        'news_datetime': news_datetime,
        'content': content
       }
    conn.execute(query, params)
    conn.commit()
    #conn.close()
    
    
    #conn = sqlite3.connect('./news20210819.db')
    """
    cursor = conn.cursor() 
    cursor = conn.execute("SELECT * from NEWSTABLE")
    readData = cursor.fetchall()
    length = len(readData)
    title = readData[0][1]
    
    readData = readData[::-1]
    """

    return redirect(url_for('index'))
    #return render_template("index.html",**locals())

@app.route('/creatnews')
def creatnews():
    
    #title = request.args.get('title')
    #author = request.args.get('author')
    #content = request.args.get('content')
    
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    
    return render_template("content_01.html",**locals())



@app.route('/form',methods = ["GET"])
def edit():
    newsid = request.args.get('newsid')
    content = request.args.get('content')
    
    #id = request.get(id)
    #content ='this is content'
    
    return render_template("content_update.html",**locals() )


@app.route('/readingNews',methods = ["GET"])
def readingNews():
    newsid = request.args.get('newsid')
    
    #content = request.args.get('content')
    title = request.args.get('title')
    author = request.args.get('author')
    
    conn = sqlite3.connect('./news20210819.db')
    cursor = conn.cursor() 
    cursor = conn.execute(f'SELECT news_datetime ,content from NEWSTABLE where id = "{newsid}" ')
    load = cursor.fetchall()
    news_datetime = load[0][0]
    '''news_datetime = DataFrame(news_datetime)
    news_datetime = news_datetime.values.tolist()
    news_datetime = news_datetime[0][0] '''
    content = load[0][1]
    
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    return render_template("content_update.html",**locals())


@app.route('/updateNews',methods = ["GET"])
def updateNews():
    
    newsid = request.args.get('newsid')
    
    print(newsid)
    print("print(newsid)")
    id = str(newsid)
    
    #id = '19'
    

    
    content = request.args.get('content')
    print("print(content)")
    print(content)
    content = str(content)
    
    conn = sqlite3.connect('./news20210819.db')
    
    now = datetime.now()
    
    
    news_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    editor ="--內部管理者於"+str(news_datetime)+"重新編輯"
    #str = f'{stock} price: {close}'
    
    #string = f'UPDATE NEWSTABLE set content = "fsafsaf4234214"  where id = 18'
    
    #string = f'UPDATE NEWSTABLE set content = "fsafsaf4234214"  where id = 18' #OKOK
    string = f'UPDATE NEWSTABLE set content = "{content}{editor}" ,news_datetime = "{news_datetime}" where id = "{id}"' #OKOK
    print(string)
    
    
    #string = "UPDATE NEWSTABLE set content = '%sfdsfs'   where id = "+id+" "
    conn.execute(string) 
    conn.commit()
    '''
    conn = sqlite3.connect('./news20210819.db')
    cursor = conn.cursor() 
    cursor = conn.execute("SELECT * from NEWSTABLE")
    readData = cursor.fetchall()
    readDataDf = DataFrame(readData)
    
    
    readDataDf =readDataDf.sort_values(by=[3])
   
    #readDataDf.pop(0)
    readData = readDataDf.values.tolist()
    length = len(readData)
    #title = readData[0][0]    
    readData = readData[::-1]
    conn.close()
    #cursor = conn.execute("SELECT * from NEWSTABLE")
    #conn.close()
    '''
    
    return redirect(url_for('index'))
    
    #now = now.strftime("%Y-%m-%d %H:%M:%S")
    #return render_template("index.html",**locals())

@app.route('/deleteNews',methods = ["GET"])
def deleteNews():
    
    
    newsid = request.args.get('newsid')
    
    
    conn = sqlite3.connect('./news20210819.db')

    conn.execute(f'DELETE from NEWSTABLE where ID = "{newsid}";')
    conn.commit()
    
    return redirect(url_for('index'))
    return render_template("content_01.html",**locals())




if __name__ == '__main__':
    app.debug = True
    app.run()