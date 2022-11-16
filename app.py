from datetime import datetime, date
import pandas as pd
from flask import Flask, render_template, request,redirect, url_for 
#from flask_sqlalchemy import SQLAlchemy 未使用

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
    
    
       
#「/next」へアクセスがあった場合に、next.htmlを返す
@app.route("/next", methods=['GET','POST'])
           
def next():
    
    if request.method == "POST": 
 
 #血液データを取得       
      pati_id = request.form.get("pati_id")
      sex = request.form.get("sex")
      age = request.form.get("age")
      count = request.form.get("count")
      ALB = request.form.get("ALB")
      AST = request.form.get("AST")
      GTP = request.form.get("GTP")
      LDL = request.form.get("L-LDL")
      HBA1c = request.form.get("HBA1c")
      HEMO = request.form.get("HEMO")
      CRP = request.form.get("CRP")
      CRE = request.form.get("CRE")
       
  #一時保存するためデータフレームへ        
      df =pd.DataFrame(
        data={'pati_id': [pati_id], 
          'sex': [sex],
          'age': [age],  
          'count': [count],
          'ALB' : [ALB],
          "AST": [AST],
          "GTP" : [GTP],
          "L-LDL": [LDL],
          "HBA1c": [HBA1c],
          "HEMO" : [HEMO],
          "CRP": [CRP],
          "CRE" : [CRE],
          }
      )
    #CSVファイルに退避　（計算部で使用）
      df.to_csv('blood_data.csv',encoding='utf-8',index=False)
               
     
      return redirect(url_for("next")) 
     
    return render_template('next.html',             
    title = "Gait Prodict",
    message = "退院前の歩行予測をするアプリです 続き" ,)

   
#「/back」へアクセスがあった場合に、index.htmlを返す   

@app.route("/back", methods=['GET','POST'])

def back():
    return render_template("/")


#「/submit」へアクセスがあった場合に、sumbmit.htmlを返す 
@app.route("/sub", methods=['GET','POST'])

def sub():
  
  if request.method == "POST": 
         
      gait = pd.read_csv("medical_data.csv",encoding='utf-8')
      print(pd.__version__)
      print(gait.head())
      
      blood = pd.read_csv("blood_data.csv",encoding='utf-8')
      print(blood.head())
      
#リハビリ総合実施計画書データを取得       
      para = request.form.get("para")
      stage = request.form.get("stage")
      eat = request.form.get("eat")
      count = request.form.get("gait")
      void = request.form.get("void")
      defe = request.form.get("defe")
      under = request.form.get("under")
      expre = request.form.get("expre")
      print("expuress")
      print(expre)
      
      
  #入力データを統合する。
  #訓練用とテストを分割する
  #予測モデル作成

  #精度の評価#confugion matrix 
  #グラフを作成
  
      
       
  #  return redirect(url_for("sub")) 
  
    
  return render_template("submit.html",
      title = "Gait Prodict",
      message = "予測結果です",
      )          

#精度を表示
#confugion matrix 

if __name__ == "__main__":

 app.run(debug=True)