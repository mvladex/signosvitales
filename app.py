from flask import Flask,render_template,request,url_for,redirect
import pyrebase
import json
from Modelo.Usuario import Usuario
from Modelo.UsuarioSistema import UsuarioSistema


#variable de configuracion
config={
    "apiKey": "AIzaSyDuPHt74eCly0aD41C2qx2bgpg55h7uQ14",
    "authDomain": "signos-vitales-a6e59.firebaseapp.com",
    "databaseURL": "https://signos-vitales-a6e59-default-rtdb.firebaseio.com",
    "projectId": "signos-vitales-a6e59",
    "storageBucket": "signos-vitales-a6e59.appspot.com",
    "messagingSenderId": "373066553971",
    "appId": "1:373066553971:web:9c1c3d58b587d622f46806"
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()



app = Flask(__name__)


@app.route('/prueba')
def prueba():
    lista_humedad=db.child("humedad").get().val()
    print("resultado",lista_humedad)
    return render_template("inicio.html",elementos_humedad=lista_humedad.values())


@app.route('/')
def hello_world():  # put application's code here
    lista=db.child("temperatura").get()
    try:
        lista_personas=lista.val()
        lista_indices=lista_personas.keys()
        lista_indice_final=list(lista_indices)
        return render_template("principal.html",lista_personas=lista_personas.values(),lista_indice_final=lista_indice_final)
    except:
        print("asds")
        return render_template("principal.html")


#ruta para mostrar formulario de registro
@app.route('/add')
def add():
    return render_template("alta_personas.html")
#-------------------------------------------------------------------------------
#capturar los datos del formulario y guardarlos en FB
@app.route('/save_data',methods=['POST'])
def save_data():
    nombre=request.form.get('nombre')
    temperatura=request.form.get('temperatura')
    fecha=request.form.get('fecha')

    hora=request.form.get('hora')
    nueva_persona=Usuario(nombre,int(temperatura),fecha,hora)
    objeto_enviar = json.dumps(nueva_persona.__dict__)

    formato = json.loads(objeto_enviar)


    db.child("temperatura").push(formato)

    #db.child("temperatura").push({"nombre": nombre, "valor":int(temperatura),"fecha":fecha,"hora":hora })

    #return render_template("principal.html")
    return redirect(url_for('hello_world'))

#eliminar un registro de la tabla
@app.route('/eliminar_persona',methods=["GET"])
def eliminar_persona():
    id= request.args.get("id")
    db.child("temperatura").child(str(id)).remove()
    return redirect(url_for('hello_world'))



@app.route('/registro')
def formulario_alta():
    return render_template("registro.html")

@app.route('/guardar',methods=['POST'])
def guardar_info():
    if request.method=='POST':
        nombre=request.form.get('nombre')
        edad=request.form.get('edad')
        correo=request.form.get('correo')
        direccion=request.form.get('direccion')
        telefono=request.form.get('telefono')
        try:
            nuevo=Usuario(nombre.replace("",''),int(edad),correo,direccion,telefono)
            objeto_enviar = json.dumps(nuevo.__dict__)
            y=json.loads(objeto_enviar)
            db.child("usuarios").push(y)

        except:
            print("error")

    return render_template("registro.html",mensaje="Registro exitoso")

#-------------------mostrar el formulario de registro-----------------------
@app.route('/actualizar_persona/<id>')
def actualizar_persona(id):
    lista = db.child("temperatura").child(str(id)).get().val()
    return render_template("formulario_actualizar.html",lista=lista,id_persona=id)

#---------------------ruta para obtener los datos del formulario y despues actualizar-------------
@app.route('/update',methods=["POST"])
def update_persona():
    #variables para obtener informacion del formulario
    idpersona=request.form.get('id')
    nombre = request.form.get('nombre')
    temperatura = request.form.get('temperatura')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')

    modificar_persona = Usuario(nombre, int(temperatura), fecha, hora)

    objeto_enviar = json.dumps(modificar_persona.__dict__)
    datos_completo = json.loads(objeto_enviar)
    db.child("temperatura").child(str(idpersona)).update(datos_completo)
    return redirect(url_for('hello_world'))


#------------------formulario de registro de usuarios del sistema--------------------------
@app.route('/altausuarios')
def altausuarios():
    return render_template("alta_usuarios_sistema.html")

#---------------- ruta para obtener los datos del formulario y crear el usuario.--------------
@app.route('/guardarusuariosistema',methods=['POST'])
def guardarusuariosistema():
    if request.method=='POST':
        nombre=request.form.get('nombre')
        correo=request.form.get('correo')
        usuario_sistema=request.form.get('usuario')
        password=request.form.get('password')
        telefono=request.form.get('telefono')
        tipo=request.form.get('tipo')
        try:
            usuario_sistema_nuevo=UsuarioSistema(nombre,correo,usuario_sistema,password,telefono,tipo)
            objeto_enviar = json.dumps(usuario_sistema_nuevo.__dict__)
            y=json.loads(objeto_enviar)
            db.child("usuarios").push(y)

        except:
            print("error")

    return render_template("alta_usuarios_sistema.html")





@app.route('/alta/<nombre>')
def registrar(nombre):
    db.child("personas").push({"nombre":nombre,"edad":"34"})
    return "dato guardado exitosamente"

@app.route('/eliminar')
def eliminar():
    db.child("personas").child("-Mx0vl1y43ZRWKtuJhMy").remove()
    return "usuario eliminado correctamente"

@app.route('/modificar')
def modificar():
    db.child("personas").child("-Mx0vymo0B9Kv4xzs0BK").update({"nombre":"José López Ramirez"})
    return "Datos modificados correctamente"


if __name__ == '__main__':
    app.run(debug=True)
