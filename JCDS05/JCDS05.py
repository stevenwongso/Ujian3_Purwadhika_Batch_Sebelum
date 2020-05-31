from flask import Flask, render_template, redirect, request, send_from_directory
import requests
import numpy as np
import pandas as pd
import json
import joblib 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('drhome.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == "GET" :
        return redirect('/')
    else :

        dataform = request.form
        digi =str(dataform['digi']).capitalize()
        dfdigimon = pd.read_json('digimon.json')
        dfdigimon['Digimon'] = dfdigimon['Digimon'].apply(lambda x: x.capitalize())
        listdigimon = list(dfdigimon['Digimon'])

        if digi in listdigimon :

            # Data
            dfdigi = dfdigimon[dfdigimon['Digimon']==digi]
            indexdigi = dfdigi.index.values[0]

            # Sistem Rekomendasi
            similardigimon = list(enumerate(SR[indexdigi]))
            similardigimon = sorted(similardigimon, key=lambda x: x[1], reverse=True) 
            j = 0
            dfDR = pd.DataFrame()
            for i in similardigimon:
                if j < 6 and i[0] != indexdigi :
                    dfDR = dfDR.append(dfdigimon[['Digimon','Stage','Type','Attribute','img']].iloc[i[0]], ignore_index=True)
                    j += 1
                elif j >= 6 :
                    break
                else :
                    pass
            return render_template('drresult.html', dfDR=dfDR, dfdigi=dfdigi)        
        else :
            return render_template('drgagal.html')

@app.route('/storage/<path:x>')
def storage(x):
    return send_from_directory('storage', x)

if __name__ == "__main__":
    SR = joblib.load('sistemrekomendasi')
    app.run(debug=True, port=5000)