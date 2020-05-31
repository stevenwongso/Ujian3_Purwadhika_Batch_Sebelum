from flask import Flask, render_template, redirect, request, send_from_directory
import requests
import numpy as np
import pandas as pd
import json
import joblib 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pbhome.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == "GET" :
        return redirect('/')
    else :
        dataform = request.form
        poke1 =str(dataform['poke1']).capitalize()
        poke2 =str(dataform['poke2']).capitalize()
        url1 = 'https://pokeapi.co/api/v2/pokemon/' + str(poke1).lower()
        url2 = 'https://pokeapi.co/api/v2/pokemon/' + str(poke2).lower()
        datapoke1 = requests.get(url1)
        datapoke2 = requests.get(url2)
        if datapoke1.status_code == 200 and datapoke2.status_code == 200 :
                
            # data
            dfPokemon = pd.read_csv('pokemon.csv')
            dfpoke1 = dfPokemon[dfPokemon['Name'] == poke1]
            dfpoke2 = dfPokemon[dfPokemon['Name'] == poke2]

            # Model Machine Learning

            feature = []
            feature.append([
                int(dfpoke1['HP']),int(dfpoke1['Attack']),int(dfpoke1['Defense']),
                int(dfpoke1['Sp. Atk']),int(dfpoke1['Sp. Def']),int(dfpoke1['Speed']),
                int(dfpoke2['HP']),int(dfpoke2['Attack']),int(dfpoke2['Defense']),
                int(dfpoke2['Sp. Atk']),int(dfpoke2['Sp. Def']),int(dfpoke2['Speed'])
            ])

            pred =int(modelcombat.predict(feature))
            if pred == 1:
                winner = poke1.capitalize()
            else :
                winner = poke2.capitalize()
            
            # probability
            probability = modelcombat.predict_proba(feature).max()
            probability = int(probability * 100)
            
            # Data Visualitation

            import plotly
            import chart_studio.plotly as py 
            import plotly.graph_objects as go


            nama = [poke1.capitalize(),poke2.capitalize()]

            plothp = go.Bar(
                x= nama, 
                y=[int(dfpoke1['HP']),int(dfpoke2['HP'])],
                marker ={'color' : ['blue','green']},
                text = [int(dfpoke1['HP']),int(dfpoke2['HP'])], 
                textposition = 'auto',
                )
            plotatk = go.Bar(
                x= nama, 
                y=[int(dfpoke1['Attack']),int(dfpoke2['Attack'])],
                marker ={'color' : ['blue','green']},
                text = [int(dfpoke1['Attack']),int(dfpoke2['Attack'])] , 
                textposition = 'auto',
                )
            plotdef = go.Bar(
                x= nama, 
                y=[int(dfpoke1['Defense']),int(dfpoke2['Defense'])],
                marker ={'color' : ['blue','green']},
                text = [int(dfpoke1['Defense']),int(dfpoke2['Defense'])], 
                textposition = 'auto'
                )
            plotspa = go.Bar(
                x= nama, 
                y=[int(dfpoke1['Sp. Atk']),int(dfpoke2['Sp. Atk'])],
                marker ={'color' : ['blue','green']},
                text = [int(dfpoke1['Sp. Atk']),int(dfpoke2['Sp. Atk'])], 
                textposition = 'auto'
                )
            plotspd = go.Bar(
                x= nama, 
                y=[int(dfpoke1['Sp. Def']),int(dfpoke2['Sp. Def'])],
                marker ={'color' : ['blue','green']},
                text = [int(dfpoke1['Sp. Def']),int(dfpoke2['Sp. Def'])], 
                textposition = 'auto'
                )
            plotspeed = go.Bar(
                x= nama, 
                y=[int(dfpoke1['Speed']),int(dfpoke2['Speed'])],
                marker ={'color' : ['blue','green']},
                text =[int(dfpoke1['Speed']),int(dfpoke2['Speed'])], 
                textposition = 'auto'
                )

            plotJSONhp = json.dumps([plothp], cls=plotly.utils.PlotlyJSONEncoder)
            plotJSONatk = json.dumps([plotatk], cls=plotly.utils.PlotlyJSONEncoder)
            plotJSONdef = json.dumps([plotdef], cls=plotly.utils.PlotlyJSONEncoder)
            plotJSONspa = json.dumps([plotspa], cls=plotly.utils.PlotlyJSONEncoder)
            plotJSONspd = json.dumps([plotspd], cls=plotly.utils.PlotlyJSONEncoder)
            plotJSONspeed = json.dumps([plotspeed], cls=plotly.utils.PlotlyJSONEncoder)

            hasilpoke1 = datapoke1.json()
            hasilpoke2 = datapoke2.json()
            return render_template(
                'pbresult.html',
                poke1=poke1,
                poke2=poke2, 
                hasilpoke1=hasilpoke1, 
                hasilpoke2=hasilpoke2, 
                winner=winner, 
                proba=probability,
                plotJSONhp=plotJSONhp,
                plotJSONatk=plotJSONatk,
                plotJSONdef=plotJSONdef,
                plotJSONspa=plotJSONspa,
                plotJSONspd=plotJSONspd,
                plotJSONspeed=plotJSONspeed
                )
        else :
            return render_template('pbgagal.html')

@app.route('/storage/<path:x>')
def storage(x):
    return send_from_directory('storage', x)

if __name__ == "__main__":
    modelcombat = joblib.load('modelcombat')
    app.run(debug=True, port=5000)