from flask import Flask, render_template, request, redirect, url_for, make_response, render_template_string
import pandas as pd
from datetime import datetime
import ast
import time

app = Flask(__name__, static_folder='icons')


@app.route('/')
def index():
    return render_template('web1_inici.html')


@app.route('/check_estacio', methods=['POST'])
def check_estacio():
    estacio = str(request.form['estacio'])
    df_estacio = pd.read_csv("database/noms_estacions.csv")

    if estacio in df_estacio['NOM ESTACIÓ'].values:
        resp = make_response(render_template('web2.html'))
        resp.set_cookie('estacio', estacio)                  
        return resp
    else:
        resp = make_response(render_template('web1_error.html'))
        return resp
    

@app.route('/web2', methods=['POST'])
def web2():
    if 'acceptar' in request.form:     
        return render_template('web3.html')
    elif 'cancelar' in request.form:
        return render_template('web1_inici.html')


@app.route('/tornar_inici', methods=['POST'])
def tornar_inici():
    return render_template('web1_inici.html')



@app.route('/mostrar_info', methods=['POST'])
def mostrar_info():
    resp = make_response(render_template('web3.html'))                
    return resp


@app.route('/web4', methods=['POST'])
def web4():
    time.sleep(3)
    resp = make_response(render_template('web4.html'))                
    return resp


@app.route('/web4_web1_inicial', methods=['POST'])
def web4_web1_inicial():
    time.sleep(3)
    resp = make_response(render_template('web1_inicial.html'))                
    return resp


# def get_next_train_time():
#     current_time = "14:00:00"
#     #current_time = datetime.now().strftime('%H:%M:%S')
#     df_viajes = pd.read_csv("database/viajes-de-hoy.csv")
#     df_viajes['arrival_time'] = pd.to_datetime(df_viajes['arrival_time'], format='%H:%M:%S').dt.time

#     next_train_time = None
#     next_train_line = None

#     for idx, time in enumerate(df_viajes['arrival_time']):
#         if time > datetime.strptime(current_time, '%H:%M:%S').time():
#             next_train_time = (datetime.combine(datetime.today(), time) + timedelta(minutes=8)).strftime('%H:%M')
#             next_train_line = df_viajes['Short Name'].iloc[idx]
#             break

#     if next_train_time is None:
#         next_train_time = (datetime.combine(datetime.today(), df_viajes['arrival_time'].iloc[0]) + timedelta(minutes=8)).strftime('%H:%M')
#         next_train_line = df_viajes['Short Name'].iloc[0]

#     return next_train_time, next_train_line




if __name__ == '__main__':
    app.run(debug=True)



