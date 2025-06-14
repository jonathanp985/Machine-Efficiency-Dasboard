import torch
import os
from flask import Flask
from flask_cors import CORS
from model import MetricsModelV1
from flask import request, jsonify
from train_test_split import X_std, X_mean
from cpu_metrics_collector import collect_metrics


app = Flask(__name__)
CORS(app)

MODEL_PATH = (str(os.getcwd()) + '\\model_files\\cpu_metrics_model.pth')

metrics_model = MetricsModelV1(input_features = 18, output_features = 1, hidden_units = 18)
metrics_model.load_state_dict(torch.load(MODEL_PATH))



@app.route("/get_metrics", methods = ["GET"])
def get_metrics():
    try:
        metrics = collect_metrics()
        metric_list = []
        for metric in metrics.values(): # Convert hashmap (key, value pairs) into array
            metric_list.append(str(metric))

        return jsonify({"message": "collection successful", "metrics": metric_list}), 201
    
    except Exception as e:
        return jsonify({"message": e, "metrics": []}), 404


@app.route("/get_score", methods = ["POST"]) # At localhost:5000
def get_score():
    data = request.get_json()
    metrics_array = data.get("metrics")
    metrics_array.pop(0) # Get rid of timestamp

    # Check for null values
    for metric in range(len(metrics_array)):
        if len(metrics_array[metric]) <= 0:
            return jsonify({"message":"One or more inputs left blank", "score": []}), 404

        metrics_array[metric] = float(metrics_array[metric])
    

    # Convert to tensor
    metrics_array = torch.tensor(metrics_array)

    # Normalize the values given
    metrics_array = (metrics_array - X_mean) / (X_std + 1e-8)

    score = metrics_model(metrics_array)

    # Denormalize after prediction
    score = ((score * X_std) + X_mean).squeeze()

    print(score, score.item(), metrics_array)
    score = score.item()


    return jsonify({"message": "metrics recieved", "score": str(score)}), 201


if __name__ == "__main__":
    app.run(debug = True)