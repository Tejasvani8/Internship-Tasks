

import pickle 
from flask import Flask 
from flask import request 
from flask import jsonify 

dv_file = 'dv.bin'
model_file = 'model1.bin'

with open(model_file, 'rb') as f:
    model = pickle.load(f)

with open(dv_file, 'rb') as f:
    dv = pickle.load(f)
    
app = Flask('churn')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()
    X = dv.transform(customer)
    prediction = model.predict_proba(X)[0,1]
    churn = prediction >= 0.5
    
    result = {
        "churn_probability": float(prediction),
        "churn": bool(churn)
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
