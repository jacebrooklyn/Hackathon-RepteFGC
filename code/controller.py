from flask import Flask, render_template, request, redirect, url_for, make_response, render_template_string
import pandas as pd
from datetime import datetime
import ast

app = Flask(__name__, static_folder='icons')

# 0. Llegim DF


# 1. PAGINA INICIAL
@app.route('/')
def index():
    return render_template('web1_inici.html')

# 1.1 INTRODUCCIÓ NIF
@app.route('/check_nif', methods=['POST'])
def check_nif():
    # 1. Obtenim el NIF del usuari
    nif = str(request.form['nif'])
    df_users = pd.read_csv("database/USERS.csv")

    # 2. Comprovem si el NIF existeix a la base de dades
    if nif in df_users['NIF'].values:
        # 3. Si existeix, retornem la pàgina de login
        resp = make_response(render_template('web2_login.html'))
        resp.set_cookie('nif', nif)                     # Guardem el NIF a la cookie (per utilitzar-lo en la resta de pàgines)
        return resp
    else:
        # 4. Si no existeix, retornem la pagina de registre
        resp = make_response(render_template('web3_signin.html'))
        resp.set_cookie('nif', nif)
        return resp
    
# 2 SIGN IN  (name, password)
@app.route('/signin_1', methods=['POST'])
def signin1():
    # 1. Obtenim el password del usuari
    password = str(request.form['password'])
    confirm_password = str(request.form['confirm_password'])

    # 2. Comprovem si el password i el confirm_password coincideixen
    while password != confirm_password:
        # mostrar que contraseña no coincide en la misma pagina html
        error = 'Passwords do not match. Please try again.'
        return render_template('web3_signin.html', error=error)
    
    # 3. Continuem amb el registre
    resp = make_response(render_template('web31_signin.html'))
    resp.set_cookie('password', password)                       # Guardem el password a la cookie (per utilitzar-lo en la resta de pàgines)
    return resp

# 2.1 SIGN IN 2 (name, surname, email)
@app.route('/signin_2', methods=['POST'])
def signin2():
    # 1. Obtenim el nom, cognom i correu del usuari
    name = str(request.form['name'])
    surname = str(request.form['surname'])
    email = str(request.form['email'])

    # 2. Obtenim el NIF i password de la cookie
    nif = str(request.cookies.get('nif'))
    password = str(request.cookies.get('password'))
    # 3. Comprovem si son Clients o Personal Shoppers
    role = request.form.get('role')  # Obtén el valor del radio button

    if role == 'client':
        # 4. Demanem que completi perfil
        resp = make_response(render_template('web32_cl_signin.html'))
        resp.set_cookie('name', name)               # Guardem el nom a la cookie (per utilitzar-lo en la resta de pàgines)
        resp.set_cookie('surname', surname)         # Guardem el cognom a la cookie (per utilitzar-lo en la resta de pàgines)
        resp.set_cookie('email', email)             # Guardem el correu a la cookie (per utilitzar-lo en la resta de pàgines)
        resp.set_cookie('nif', nif)                 # Guardem el NIF a la cookie (per utilitzar-lo en la resta de pàgines)
        resp.set_cookie('password', password)       # Guardem el password a la cookie (per utilitzar-lo en la resta de pàgines)

        return resp
    
    elif role == 'shopper':
        # 5. Desem usuari a USERS_PS i personal shopper a PS
        user = {
            'NIF': [nif,],
            'Nom': [name,],
            'Cognom': [surname,],
            'Data_Alta': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'Correu_electronic': [email,],
            'Contrassenya': [password,]
        }

        df_users = pd.read_csv("database/USERS.csv")
        new_user_df = pd.DataFrame(user)
        df_users = pd.concat([df_users, new_user_df], ignore_index=True)
        df_users.to_csv('database/USERS.csv', index=False)

        df_ps = pd.read_csv("database/PS.csv")
        new_ps = pd.DataFrame({'NIF': [nif,], 'Assigned_clients': ['[]',]})
        df_ps = pd.concat([df_ps, new_ps], ignore_index=True)
        df_ps.to_csv('database/PS.csv', index=False)

        # 6. Retornem la pàgina de login
        return render_template('web2_login.html')
    else:
        # Mostrem error
        return render_template('web31_signin.html', error = 'Please select an option')
    
# 2.2 SIGN IN 3 (client)
@app.route('/signin_3_cl', methods=['POST'])
def signin3_cl():
    phone = str(request.form['phone'])
    address = str(request.form['address'])
    gender = str(request.form['gender'])
    age = int(request.form['age'])
    height = int(request.form['height'])
    weight = float(request.form['weight'])
    hair_color = str(request.form['hair_color'])
    eye_color = str(request.form['eye_color'])
    skin_tone = str(request.form['skin_tone'])
    shirt_size = str(request.form['shirt_size'])
    pants_size = str(request.form['pant_size'])
    shoe_size = str(request.form['shoe_size'])
    description = str(request.form['description'])

    
    user = {
        'NIF': [request.cookies.get('nif'),],
        'Nom': [request.cookies.get('name'),],
        'Cognom': [request.cookies.get('surname'),],
        'Data_Alta': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'Correu_electronic': [request.cookies.get('email'),],
        'Contrassenya': [request.cookies.get('password'),]
    }
    
    df_users = pd.read_csv("database/USERS.csv")
    new_user_df = pd.DataFrame(user)
    df_users = pd.concat([df_users, new_user_df], ignore_index=True)
    df_users.to_csv('database/USERS.csv', index=False)

    df_clients = pd.read_csv("database/CLIENTS.csv")
    new_client = pd.DataFrame({'NIF': [request.cookies.get('nif'),], 'Phone': [phone,], 'Address': [address,], 'Gender': [gender,], 'Age': [age,], 'Height': [height,], 'Weight': [weight,], 'Hair_color': [hair_color,], 'Eye_color': [eye_color,], 'Skin_tone': [skin_tone,], 'Shirt_size': [shirt_size,], 'Pants_size': [pants_size,], 'Shoe_size': [shoe_size,], 'Description': [description,]})
    df_clients = pd.concat([df_clients, new_client], ignore_index=True)
    df_clients.to_csv('database/CLIENTS.csv', index=False)

    return render_template('web2_login.html')

# 3 LOGIN
@app.route('/login', methods=['POST'])
def login():
    # 1. Obtenim el NIF i password del usuari
    nif = str(request.form['nif'])
    password = str(request.form['password'])

    # 2. Comprovem si el NIF i password coincideixen
    df_users = pd.read_csv("database/USERS.csv")
    if nif in df_users['NIF'].values and password == df_users[df_users['NIF'] == nif]['Contrassenya'].values[0]:
        # 3. Si coincideixen, retornem la pàgina de login
        # mirem si es client o shopper
        df_ps = pd.read_csv("database/PS.csv")
        if nif in df_ps['NIF'].values:
            # 4. Si es shopper, retornem la pàgina de shopper
            resp = make_response(render_template('web4_menu_ps.html'))
            resp.set_cookie('nif', nif)                     # Guardem el NIF a la cookie (per utilitzar-lo en la resta de pàgines)
            return resp
        else:
            # 5. Si es client, retornem la pàgina de client
            resp = make_response(render_template('web4_menu_cl.html'))
            resp.set_cookie('nif', nif)                     # Guardem el NIF a la cookie (per utilitzar-lo en la resta de pàgines)
            return resp
    else:
        # 4. Si no coincideixen, retornem la pagina de registre
        error = 'Incorrect NIF or password. Please try again.'
        return render_template('web2_login.html', error=error)

# 4.1 CLIENT MENU
@app.route('/client_menu')
def client_menu():
    return render_template('web4_menu_cl.html')

# 4.2 PERSONAL SHOPPER MENU
@app.route('/ps_menu')
def shopper_menu():
    return render_template('web4_menu_ps.html')

# 5.1 PS PROFILE
@app.route('/ps_profile')
def ps_profile():
    # 1. Obtenim el NIF del usuari
    nif = str(request.cookies.get('nif'))

    # 2. Obtenim la informació del usuari
    df_users = pd.read_csv("database/USERS.csv")
    df_ps = pd.read_csv("database/PS.csv")
    name = df_users[df_users['NIF'] == nif]['Nom'].values[0]
    surname = df_users[df_users['NIF'] == nif]['Cognom'].values[0]
    email = df_users[df_users['NIF'] == nif]['Correu_electronic'].values[0]
    data_alta = df_users[df_users['NIF'] == nif]['Data_Alta'].values[0]

    # 3. Retornem la pàgina de perfil
    return render_template('web5_ps_profile.html', name=name, surname=surname, email=email, data_alta=data_alta)

# 5.2 PS GESTIO
@app.route('/ps_gestio')
def ps_gestio():
    # Obtener el NIF del Personal Shopper
    nif_ps = str(request.cookies.get('nif'))

    # Leer el archivo PS.csv y obtener los clientes asignados al PS
    df_ps = pd.read_csv("database/PS.csv")

    # Filtrar el PS por su NIF y obtener los NIF de los clientes asignados
    assigned_clients = df_ps[df_ps['NIF'] == nif_ps]['Assigned_clients'].values
    assigned_clients = assigned_clients[0] if len(assigned_clients) > 0 else ''  # Seleccionar el valor de la lista

    # Convertir la cadena de NIF en una lista
    client_list = assigned_clients.split('-') if assigned_clients else []

    # dictionary for every client
    df_clients = pd.read_csv("database/CLIENTS.csv")
    df_users = pd.read_csv("database/USERS.csv")
    client_dict = {}
    for client in client_list:
        name = df_users[df_users['NIF'] == client]['Nom'].values[0]
        surname = df_users[df_users['NIF'] == client]['Cognom'].values[0]

        cl_details = df_clients[df_clients['NIF'] == client].to_dict('records')[0]

        client_dict[client] = {'name': name, 'surname': surname, 'details': cl_details}
    
    return render_template('web5_ps_gestio.html', client_dict=client_dict)


# 5.3 PS CATALOG
@app.route('/ps_catalog')
def ps_catalog():
    return render_template('web5_ps_catalog.html')

# 5.4 PS INFORMES
@app.route('/ps_chats')
def ps_chats():
    # Obtener el NIF del Personal Shopper
    nif_ps = str(request.cookies.get('nif'))

    # Leer el archivo PS.csv y obtener los clientes asignados al PS
    df_ps = pd.read_csv("database/PS.csv")

    # Filtrar el PS por su NIF y obtener los NIF de los clientes asignados
    assigned_clients = df_ps[df_ps['NIF'] == nif_ps]['Assigned_clients'].values
    assigned_clients = assigned_clients[0] if len(assigned_clients) > 0 else ''  # Seleccionar el valor de la lista

    # Convertir la cadena de NIF en una lista
    client_list = assigned_clients.split('-') if assigned_clients else []

    # get the name and surname of each client
    df_users = pd.read_csv("database/USERS.csv")
    client_dict = {}
    for client in client_list:
        name = df_users[df_users['NIF'] == client]['Nom'].values[0]
        surname = df_users[df_users['NIF'] == client]['Cognom'].values[0]

        client_dict[client] = {'name': name, 'surname': surname}

    return render_template('web5_ps_chats.html', client_dict=client_dict)

# 6.1 CL PROFILE
@app.route('/cl_profile')
def cl_profile():
    # 1. Obtenim el NIF del usuari
    nif = str(request.cookies.get('nif'))

    # 2. Obtenim la informació del usuari
    df_users = pd.read_csv("database/USERS.csv")
    df_clients = pd.read_csv("database/CLIENTS.csv")
    name = df_users[df_users['NIF'] == nif]['Nom'].values[0]
    surname = df_users[df_users['NIF'] == nif]['Cognom'].values[0]
    email = df_users[df_users['NIF'] == nif]['Correu_electronic'].values[0]
    data_alta = df_users[df_users['NIF'] == nif]['Data_Alta'].values[0]
    phone = df_clients[df_clients['NIF'] == nif]['Phone'].values[0]

    # mostrem perfil user
    user_detauls = df_clients[df_clients['NIF'] == nif].to_dict('records')[0]

    return render_template('web6_cl_profile.html', name=name, surname=surname, email=email, data_alta=data_alta, phone=phone, user_detauls=user_detauls)

# 6.2 CL COMANDA
@app.route('/cl_comanda')
def cl_comanda():
    return render_template('web6_cl_comanda.html')

# 6.3 CL COMANDES PENDENTS
@app.route('/comandes_pendents')
def cl_comandes_pendents():
    return render_template('web6_comandes_pendents.html')

# 6.4 CHAT
@app.route('/chat')
def cl_chat():
    return render_template('web6_chat.html')

if __name__ == '__main__':
    app.run(debug=True)

    

