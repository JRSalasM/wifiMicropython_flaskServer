from flask import Flask, render_template, request
import os

app = Flask(__name__)

class Loggeado:
    def __init__(self):
        self.loggeado = False
        self.password = ''


def consultar_contrasenia():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'g.txt')

    with open(my_file, 'r', encoding='utf8') as f:
        password = f.read()

    return password


@app.route('/<usuario>/<estado>')
def cambiar_estado(usuario, estado):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    password = consultar_contrasenia()

    if status.loggeado is True and password == 'i\n':
        my_file = os.path.join(THIS_FOLDER, 'data.csv')

        if estado == 'on':
            with open(my_file, 'w', encoding='utf8') as f:
                f.write('1\n1\nipsum')
        elif estado == 'off':
            with open(my_file, 'w', encoding='utf8') as f:
                f.write('0\n0\nlorem')

        return render_template('control.html', usuario=usuario)
    else:
        return "Debes iniciar sesión para acceder al controlador"


@app.route('/<usuario>/texto', methods=['POST', 'GET'])
def enviar_texto(usuario):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    password = consultar_contrasenia()

    if status.loggeado is True and password == 'i\n':
        my_file = os.path.join(THIS_FOLDER, 'data.csv')

        if request.method == 'POST':
            with open(my_file, 'r', encoding='utf8') as f:
                estado_leds = f.read()
            estado_leds = '\n'.join(estado_leds.split('\n')[:-1])
            texto16char = request.form['texto16char']
            with open(my_file, 'w', encoding='utf8') as f:
                f.write(estado_leds + "\n" + texto16char)
            return render_template('control.html', usuario=usuario)
        else:
            return render_template('control.html')
    else:
        return "Debes iniciar sesión para acceder al controlador"


@app.route('/', methods=['POST', 'GET'])#  http://127.0.0.1:5000/on
def index():
    status.loggeado = False
    if request.method == 'POST':
        usuario = request.form['usuario']
        password_ingresada = request.form['contrasenia']
        status.password = consultar_contrasenia()
        #print(status.password)
        if usuario == 'e' and (password_ingresada+'\n') == status.password:
            status.loggeado = True
            return render_template('control.html', usuario=usuario)
        else:
            return "Usuario o contraseña incorrectos"
    else:
        return render_template('logging.html')

# @app.route('/on')
# def encendido():
#     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#     my_file = os.path.join(THIS_FOLDER, 'data.csv')
#
#     with open(my_file, 'w', encoding='utf8') as f:
#         f.write('1\n1')
#     return render_template('on.html')
#
# @app.route('/off')
# def apagado():
#     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#     my_file = os.path.join(THIS_FOLDER, 'data.csv')
#
#     with open(my_file, 'w', encoding='utf8') as f:
#         f.write('0\n0')
#     return render_template('off.html')


@app.route('/getjson', methods=['GET'])
def metodoget():
    data = ''
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'data.csv')

    with open(my_file, 'r', encoding='utf8') as f:
        data = f.read()
    data = data.split('\n')
    return '{' + f'"pin16":{data[0]}, "pinX":{data[1]}, "msg":{data[2]}' + '}'


status = Loggeado()

if __name__ == '__main__':
    app.run(debug=True)
