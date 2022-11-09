from datetime import datetime, date
import pandas as pd
import codecs


from flask import Flask, render_template, request, session,redirect, url_for ,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def index():
  
    if request.method == 'GET':
    
       return render_template('index.html',
                           
       title = "Gait Prodict",
       message = "退院前の歩行予測をするアプリです",
    ) 
     #1データのチェックをした方がいいか？  
     #2全データを入力していないと次の画面に進めないようにする  
                  
    if request.method == 'post': 
                                         
       pati_id = request.form.get('id')
        
       sex= request.form.get('gender')
           
       count= request.form.get('count')
       
       # データフレームを作成
       df = pd.DataFrame( [pati_id, sex, count],
       columns=['id', 'sex', 'count'])
 
      # CSV ファイル (employee.csv) として出力
       print("df")
       print(df)
       df.to_csv("pati_data.csv", encoding='utf-8')
      
    return render_template('index.html')
      
    
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
    
#訓練データを読み込む
#テストデータ作成中

gait = pd.read_csv("blood_data2.csv",encoding='utf-8') 
print(gait.head())

print("test")   

#訓練用をテストを分割する
#予測モデル作成

#精度の評価

#入力データから予測を実施

#グラフを作成

#精度を表示



if __name__ == "__main__":
    app.run(debug=True)