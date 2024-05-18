from flask import Flask, render_template, request, redirect, url_for, make_response, render_template_string
import pandas as pd
from datetime import datetime
import ast

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
    

@app.route('/tornar_inici', methods=['POST'])
def tornar_inici():
    resp = make_response(render_template('web1_inici.html'))                 # Guardem el password a la cookie (per utilitzar-lo en la resta de pàgines)
    return resp


# @app.route('/tornar_inici', methods=['POST'])
# def mostrar_info():

#     resp = make_response(render_template('web1_inici.html'))                 # Guardem el password a la cookie (per utilitzar-lo en la resta de pàgines)
#     return resp
















if __name__ == '__main__':
    app.run(debug=True)



