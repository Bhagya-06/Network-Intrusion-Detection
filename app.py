from flask import Flask, request, jsonify
import h2o
from h2o.estimators import H2ORandomForestEstimator
from flask_cors import CORS

# Initialize H2O
h2o.init()

# Load the pre-trained model (change this path to where your model is saved)
model = h2o.load_model("DRF_model_python_1734776076049_1")

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse the incoming request data
        data = request.get_json()
        print("Received data:", data)

        # Extract required fields (assuming src_ip and dest_ip are numeric)
        src_port = data['src_port']
        dest_port = data['dest_port']
        src_ip = data['src_ip']  # Numeric value
        dest_ip = data['dest_ip']  # Numeric value
        bytes_out = data['bytes_out']

        # Convert the input data into H2O frame format for prediction
        input_data = {
            'src_port': [src_port],
            'dest_port': [dest_port],
            'src_ip': [src_ip],
            'dest_ip': [dest_ip],
            'bytes_out': [bytes_out]
        }
        
        input_frame = h2o.H2OFrame(input_data)

        # Predict using the trained model
        prediction = model.predict(input_frame)

        print("Raw prediction output:", prediction)

        # Get the predicted class and confidence
        predicted_class = prediction[0, 0]
        confidence = prediction[0, 1] * 100 # confidence for class 1 (Malicious)

        # Return the prediction and confidence
        return jsonify({
            'prediction': 'Malicious' if predicted_class == 1 else 'Benign',
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
