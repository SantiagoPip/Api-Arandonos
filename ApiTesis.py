from tensorflow import keras
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# Cargar el modelo guardado
model = keras.models.load_model('modelo_precision_acumulado.h5')
model.summary()
@app.route('/',methods=['GET'] )
def test():
    print("Funcionando correctamente")

    return jsonify({'message':'Funcionando Correctamente'},200)
@app.route('/predict', methods=['POST'])
def predict():
    print("Metodo post funcionando correctamente")
    print("iniciando la prediccion de datos...")
#     Verificar si el archivo fue enviado
    if 'file' not in request.files:
         return jsonify({'error': 'No se envió un archivo'}), 400
    file = request.files['file']
    return jsonify({'funcionando': 'funcionando correctamente'}, 400)

# @app.route('/predict', methods=['POST'])
# def predict():
#     print("iniciando la prediccion de datos...")
#     # Verificar si el archivo fue enviado
#     if 'file' not in request.files:
#         return jsonify({'error': 'No se envió un archivo'}), 400

#     file = request.files['file']

   
#     try:
#         # Leer el archivo Excel usando pandas
#         df = pd.read_excel(file)
    
#         # Preprocesar los datos (asegúrate de que solo contengan columnas numéricas)
#         # Reemplaza 'columnas_relevantes' con las columnas que tu modelo necesita
#         columnas_relevantes = ['Variedad_B', ' mm Precipitation', ' m/s Gust Speed', 'IP', ' mm/h Max Precip Rate', 'Semana', 'Variedad_W', 'Variedad_V',' °C Air Temperature', 'PFIG','PFG','Variedad_L']  # Ejemplo de columnas necesarias
        
#         missing_columns = [col for col in columnas_relevantes if col not in df.columns]
#         if missing_columns:
#             return jsonify({'error': f"Faltan las siguientes columnas en el archivo: {missing_columns}"}), 400

    
#         # Seleccionar solo las columnas necesarias
#         input_data = df[columnas_relevantes]
    
#         # Manejar valores faltantes (opcional: rellena con 0 o la media)
#         input_data = input_data.fillna(0)
    
#         # Verifica que todas las columnas sean numéricas
#         input_data = input_data.astype(float)
    
#         # Hacer predicciones con el modelo
#         predictions = model.predict(input_data)
    
#         # Agregar las predicciones como una nueva columna en el DataFrame
#         df['Predicciones'] = predictions.tolist()
    
#         # Crear un archivo Excel en memoria con las predicciones añadidas
#         output = io.BytesIO()
#        # df.to_excel('mi_archivo_con_predicciones3.xlsx', index=False)
#         df.to_excel(output, index=False)
        
#         output.seek(0)  # Volver al principio del archivo en memoria
    
#         # Devolver el archivo Excel con las predicciones al cliente
#         return send_file(output, as_attachment=True, download_name="predicciones_con_resultados.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


    
