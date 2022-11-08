from datetime import datetime, date
from email import message


from flask import Flask, render_template, request, redirect, url_for # url_forを追加する
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def index():
    
    return render_template('index.html',
                           
       title = "Gait Prodict",
       message = "退院前の歩行予測をするアプリです",
     
     #データのチェックをした方がいいか？  
     #全データを入力していないと警告文とか                
     
       id = request.form.get('id'),
       data1= request.form.get('data1'),
       data2= request.form.get('data2'),

       )
      
      # 一時保存
      #new_post = Post(id=id, data1=data1, data2=data2)
      #db.session.add(new_post)
      #db.session.commit()
      #return redirect('/')
      
#「/next」へアクセスがあった場合に、next_index.htmlを返す
@app.route("/next", methods=['GET','POST'])
           
def next():
    return render_template("next.html",
      title = "Gait Prodict",
      message = "退院前の歩行予測をするアプリです",
      
      data3= request.form.get('data3'),
      data4= request.form.get('data4'),)
     
#「/back」へアクセスがあった場合に、index.htmlを返す   

@app.route("/back", methods=['GET','post'])

def back():
    return render_template("/")


#「/submit」へアクセスがあった場合に、sumbmit.htmlを返す 
@app.route("/sub", methods=['GET','post'])

def sub():
    return render_template("submit.html",
      title = "Gait Prodict",
      message = "予測結果です"
      )

if __name__ == "__main__":
    app.run(debug=True)