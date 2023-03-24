from flask import Flask, request,send_file
import barcode
from barcode.writer import ImageWriter
from waitress import serve
import os


app = Flask(__name__)

def delete_barcode() -> bool:
    """
    Elimina todos los archivos con extensión .png en el directorio actual.

    Args:
        NULL
    Returns:
        NULL
    """
    directory = "./"
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".png")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    return

def generate_barcode(value) ->str:
    """
    Genera un código de barras en formato Code128 para el valor dado.

    Args:
        value (str): El valor a codificar en el código de barras.

    Returns:
        str: El nombre del archivo de imagen del código de barras generado, si se generó correctamente.
             Si no se pudo generar el código de barras, devuelve 0.
    """
    EAN_FORMAT ="Code128"
    EAN = barcode.get_barcode_class(EAN_FORMAT)
    my_ean = EAN(value, writer=ImageWriter())
    file_name = str(value)+"_"+EAN_FORMAT+"_barcode"
    barcode_generated = my_ean.save(file_name)
    if barcode_generated: 
        print("Codigo de barras creado: ",file_name+".png")
        return file_name+".png"
    else: return 0


@app.route('/search', methods=['GET'])
def search()->str:
    """
    Genera y envía un archivo de imagen PNG de un código de barras en formato Code128
    para el valor proporcionado en los argumentos de la solicitud GET.

    Args:
        None.

    Returns:
        str: El archivo de imagen del código de barras generado, con el tipo de contenido "image/png".
    """
    args = request.args
    value = args.get('value')
    print("Valor de codigo de barras: ", value)
    delete_barcode()
    file_name = generate_barcode(value)
    return send_file(file_name,mimetype="image/png")


if __name__ == '__main__':
    print("RWT: app,host='0.0.0.0', port=80")
    serve(app,host='0.0.0.0', port=80)
