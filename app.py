import pandas as pd
import numpy as np
from flask import Flask, render_template, request,redirect, url_for 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import export_graphviz
#from matplotlib.colors import ListedColormap

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
     #2全データを入力していないと次の画面に進めないようにする    
    
    
       
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
      #df.to_csv("/tmp/blood_data.csv",encoding='utf-8',index=False)
      df.to_csv("blood_data.csv",encoding='utf-8',index=False)         
     
      return redirect(url_for("next")) 
     
    return render_template('next.html',             
    title = "Gait Prodict",
    message = "退院前の歩行予測をするアプリです 続き" ,)

   
#「/back」へアクセスがあった場合に、index.htmlを返す   

@app.route("/back", methods=['GET','POST'])

def back():
  
  if request.method == "POST":
    return render_template("index.html")


#「/sub」へアクセスがあった場合に、sumbmit.htmlを返す 
@app.route("/sub", methods=['GET','POST'])

def sub():
  
  if request.method == "POST": 
         
      df_train = pd.read_csv("medical_data.csv",encoding='utf-8')
      #print(df_train.head())
      
      blood = pd.read_csv("blood_data.csv",encoding='utf-8')
      #blood = pd.read_csv("/tmp/blood_data.csv",encoding='utf-8')
      #print(blood.head())
      
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
  print(y.shape)
  
  #訓練用とテストを分割する
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0) 
  
  print(len(X_train), len(X_test))
  
  model = LogisticRegression(penalty='none', max_iter=200)
  model.fit(X_train, y_train)
  
  #精度の評価 
  y_pred1 = model.predict(X_test)
  cm = confusion_matrix(y_test, y_pred1)
  cl = model.classes_
  disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels= cl)
  disp.plot()
  
  #入力データの予測
  df_test =df_test.drop(["GAIT"] , axis=1)
  df_test =df_test.drop(["pati_id"] , axis=1)
  
  print(X.head())
  print(df_test)
  df_test.to_csv("test_data.csv")
  y_pred = model.predict_proba(df_test)
  print(y_pred)
  
   
  cl = model.classes_
  
  #クラス分類の表示　0を含めると1から7までの段階で8分類
  #例）分類が「4」であれば歩行段階は「5」
  
  print(cl)
  
  
  #グラフを作成
      
  #  return redirect(url_for("sub")) 
  
    
  return render_template("submit.html",
      title = "Gait Prodict 予測結果です",
      message = "y_pred",
      )          

if __name__ == "__main__":

 app.run(debug=True)