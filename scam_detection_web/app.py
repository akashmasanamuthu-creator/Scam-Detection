from flask import Flask, render_template_string, request
from model import predict_message

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Scam Detection System</title>
    <style>
        body { font-family: Arial; background: #f4f6f8; }
        .container {
            width: 420px;
            margin: 80px auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 0 10px #ccc;
        }
        textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
        }
        button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            background: #007bff;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Scam Message Detection</h1>

    <form method="POST">
        <textarea name="message" placeholder="Enter message here..." required></textarea>
        <button type="submit">Analyze</button>
    </form>

    {% if result %}
        <div class="result">
            <h2>{{ result }}</h2>
            <p>Scam Probability: {{ probability }}%</p>
        </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    probability = None

    if request.method == "POST":
        message = request.form["message"]
        prediction, probability = predict_message(message)
        result = "⚠️ Scam Message" if prediction == 1 else "✅ Safe Message"

    return render_template_string(
        HTML_PAGE,
        result=result,
        probability=probability
    )

if __name__ == "__main__":
    app.run(debug=True)
