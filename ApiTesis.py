from tensorflow import keras
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import io
from sklearn.preprocessing import StandardScaler
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Asegura que la carpeta de uploads exista
scaler = StandardScaler()
# Cargar el modelo guardado
model = keras.models.load_model('modelo_precision_acumulado.h5', compile=False)
model.compile(optimizer='adam', loss='mse', metrics=['mae'])  # Reemplaza con tu configuración
model.summary()
@app.route('/',methods=['GET'] )
def test():
    print("Funcionando correctamente")

    return jsonify({'message':'Funcionando Correctamente'}),200
# @app.route('/predict', methods=['POST'])
# def predict():
#     print("Metodo post funcionando correctamente")
#     print("iniciando la prediccion de datos...")
# #     Verificar si el archivo fue enviado
#     if 'file' not in request.files:
#          return jsonify({'error': 'No se envió un archivo'}), 400
#     file = request.files['file']
#     return jsonify({'funcionando': 'funcionando correctamente'}, 400)

@app.route('/predict', methods=['POST'])
def predict():
    print("Iniciando la predicción de datos...")

    # Verificar si el archivo fue enviado
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió un archivo'}), 400

    file = request.files['file']

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)  # Guarda el archivo temporalmente
        columnas_ambientales = [' mm Precipitation', ' m/s Gust Speed', ' mm/h Max Precip Rate', ' °C Air Temperature']
        print("Archivo guardado en:", file_path)

        # Leer el archivo Excel usando pandas
        df = pd.read_excel(file_path)
        print("ARCHIVO RECIBIDO Y LEÍDO")

        # Definir las columnas necesarias
        columnas_relevantes = [
            'Variedad_B', ' mm Precipitation', ' m/s Gust Speed', 'IP', 
            ' mm/h Max Precip Rate', 'Semana', 'Variedad_W', 'Variedad_V',
            ' °C Air Temperature', 'PFIG', 'PFG', 'Variedad_L'
        ]
        
        missing_columns = [col for col in columnas_relevantes if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f"Faltan las siguientes columnas en el archivo: {missing_columns}"}), 400

        # Seleccionar solo las columnas necesarias
        input_data = df[columnas_relevantes]

        # Manejar valores faltantes (rellena con 0)
        input_data = input_data.fillna(0)
        #input_data[columnas_ambientales] = scaler.fit_transform(df[columnas_ambientales])

        # Verifica que todas las columnas sean numéricas
        input_data = input_data.astype(float)

        # Verificar si el modelo está disponible
        if 'model' not in globals():
            return jsonify({'error': 'El modelo no está definido'}), 500

        # Hacer predicciones con el modelo
        predictions = model.predict(input_data)

        # Agregar las predicciones como una nueva columna en el DataFrame
        df['Predicciones'] = predictions.tolist()
        df['Predicciones'] = [str(int(pred))[:2] for pred in predictions.flatten()]
# Asegura que sea un array unidimensional
        # Crear un archivo Excel en memoria con las predicciones añadidas
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)  # Volver al principio del archivo en memoria

        # Devolver el archivo Excel con las predicciones al cliente
        return send_file(output, as_attachment=True, download_name="predicciones_con_resultados.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        print("ERROR:", str(e))  # Agrega esta línea
        return jsonify({'error': f"Ocurrió un error al procesar el archivo: {str(e)}"}), 500

    finally:
        # Eliminar el archivo temporal después de usarlo
        if os.path.exists(file_path):
            os.remove(file_path)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)


    
