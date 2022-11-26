import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request,redirect, url_for 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def index():
    
    if request.method == 'GET':
    
       return render_template('index.html',
                           
        title = "Gait Prodict",
    
        message = "脳梗塞：退院前の歩行予測をするアプリです",
       )
    else:
       return render_template('index.html',
                           
        title = "Gait Prodict",
    
        message = "脳梗塞：退院前の歩行予測をするアプリです",
       )
     #1データのチェックをした方がいいか？   
    
#「/next」へアクセスがあった場合に、next.htmlを返す
@app.route("/next", methods=['GET','POST'])
           
def next():
    
    if request.method == "POST": 
 
 #血液データを取得       
      pati_id = request.form.get("pati_id")
      SEX = request.form.get("sex")
      AGE = request.form.get("age")
      COUNT = request.form.get("count")
      ALB = request.form.get("ALB")
      AST = request.form.get("AST")
      ALT = request.form.get("ALT")
      GTP = request.form.get("GTP")
      HBA1C = request.form.get("HBA1C")
      HEMO = request.form.get("HEMO")
      CRP = request.form.get("CRP")
      CRE = request.form.get("CRE")
       
  #一時保存するためデータフレームへ        
      df =pd.DataFrame(
        data={'pati_id': [pati_id], 
          'SEX': [SEX],
          'AGE': [AGE],  
          'COUNT': [COUNT],
          'ALB' : [ALB],
          "AST": [AST],
          "ALT": [ALT],
          "GTP" : [GTP],
          "HBA1C": [HBA1C],
          "HEMO" : [HEMO],
          "CRP": [CRP],
          "CRE" : [CRE],
          }
      )
    #CSVファイルに退避　（計算部で使用）
      # ディレクトリがないとエラーになるため作成
      #dir = Path
      #direct = dir.mkdir(parents=True, exist_ok=True)
      
      
      #df.to_csv('/tmp/blood_data.csv', encoding='utf-8',index=False)
      
      df.to_csv("blood_data.csv",encoding='utf-8',index=False)         
     
      return redirect(url_for("next")) 
     
    return render_template('next.html',             
    title = "Gait Prodict",
    message = "続き　退院前の歩行予測をするアプリです" ,)

   
#「/back」へアクセスがあった場合に、index.htmlを返す   

@app.route("/back", methods=['GET','POST'])

def back():
  
  if request.method == "POST":
    return render_template("index.html")


#「/sub」へアクセスがあった場合に、sumbmit.htmlを返す 
@app.route("/sub", methods=['GET','POST'])

def sub():
  
  if request.method == "POST": 
      
      blood = pd.read_csv("blood_data.csv",encoding='utf-8')
      #blood = pd.read_csv('/tmp/blood_data.csv', encoding='utf-8')
      #print(blood.head())
         
      df_train = pd.read_csv("medical_data.csv", encoding='utf-8')
      #print(df_train.head())
      
    #追加・削除が発生する可能性があるため、1項目ずつ代入
      pati_id = blood.loc[:, ["pati_id"]]
      SEX = blood.loc[:, ["SEX"]]
      AGE = blood.loc[:, ["AGE"]]
      COUNT = blood.loc[:, ["COUNT"]]
      ALB = blood.loc[:, ["ALB"]]
      AST = blood.loc[:, ["AST"]]
      ALT = blood.loc[:, ["ALT"]]
      GTP = blood.loc[:, ["GTP"]]
      HBA1C = blood.loc[:, ["HBA1C"]]
      HEMO = blood.loc[:, ["HEMO"]]
      CRE = blood.loc[:, ["CRE"]]
      CRP = blood.loc[:, ["CRP"]]
 
#リハビリ総合実施計画書データを取得 
      
      side = request.form.get("para")
      stage_a = request.form.get("stage-a")
      stage_b = request.form.get("stage-b")
      stage_c = request.form.get("stage-c")
      eat = request.form.get("eat")
      void = request.form.get("void")
      defe = request.form.get("defe")
      gait = request.form.get("gait")
      under = request.form.get("under")
      expre = request.form.get("expre")
      #print("expuress")
      #print(expre)
      
  #入力データを統合する
  df_plan =pd.DataFrame(
        data={"SIDE" : [side],
          "STAGE-A" : [stage_a],
          "STAGE-B" : [stage_b],
          "STAGE-C" : [stage_c],
          "EAT" : [eat],
          "VOID" : [void],
          "DEFE" : [defe],
          "GAIT" : [gait],
          "UNDER" : [under],
          "EXPREE" : [expre]} 
        )
  
  df_plan.to_csv("plan_data.csv",encoding='utf-8',index=False)
  df_test = pd.concat([blood, df_plan], axis=1)
  
  print(df_test.shape)
  print(df_test.head())

  #説明変数
  X = df_train.drop(["GAIT"] , axis=1)
  X = X.drop(["ID"] ,axis=1)
  X = X.dropna()
  
  #目的変数
  df_gait = df_train.loc[:, ["GAIT"]]
  y  = df_gait
  y = y.dropna()
  #print(y.shape)
  
  #訓練用とテストを分割する
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0) 
  
  #print(len(X_train), len(X_test))
  
  model = LogisticRegression(penalty='none', max_iter=200)
  model.fit(X_train, y_train)
  
  #精度の評価 
  y_pred1 = model.predict(X_test)
  cm = confusion_matrix(y_test, y_pred1)
  
  #正解率 
  acc = (accuracy_score(y_test, y_pred1))
  
  #パーセント表示
  acc_w = acc * 100
  
  text1 = "{:.1f}"
  acc_dis_w = text1.format(acc_w)
  
  acc_dis = str(acc_dis_w) + "%"
  
  print("正解率")
  print(acc_w)
  
  
  #入力データの予測
  df_test =df_test.drop(["GAIT"] , axis=1)
  df_test =df_test.drop(["pati_id"] , axis=1)
  
  #print(X.head())
  #print(df_test)
  
  df_test.to_csv("test_data.csv")
  y_pred = model.predict_proba(df_test)
  
  print(y_pred)
  
  #リストに変換
  y_list = np.array(y_pred)
   
  y_list1 =  y_list[0]
  
  print(len(y_list1))
  
  #最大値の確率を取得
  y_list_max =  max(y_list1)
  print(y_list_max)
  
  #最大値のINDEX
  y_list_w = y_list1
  
  max_index = np.argmax(y_list_w)
 
  print(max_index)
  
  #クラス数を取得  
  cl = model.classes_
  
  
  print(cl) 
  print(cl[max_index])
  
  #歩行のグレードを取得
  grade_dis = cl[max_index]
  
  grade_dis = str(grade_dis)
  
  #パーセント表示
  proba = y_list_max * 100
  
  text = "{:.1f}"
  proba_dis_w = text.format(proba)
  
  proba_dis = str(proba_dis_w) + "%"
  
  #楯列から横列へ変換
  print(proba_dis)
   
     #return redirect(url_for("sub"))   
  return render_template("submit.html",
                         
      title = "Gait Prodict",
      message = "あなたの退院前の歩行能力のグレード予測です" ,
      
      data1 = grade_dis, 
      data2 = proba_dis,
      data3 = acc_dis )
      
if __name__ == "__main__":

 app.run(debug=True)