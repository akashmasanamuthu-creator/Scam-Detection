from flask import Flask, render_template_string, request
from model import predict_message

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scam Detection System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 500px;
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header {
            text-align: center;
            margin-bottom: 35px;
        }
        
        .header-icon {
            font-size: 48px;
            margin-bottom: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        h1 {
            font-size: 28px;
            color: #2d3748;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .subtitle {
            color: #718096;
            font-size: 14px;
            font-weight: 500;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            color: #2d3748;
            font-weight: 600;
            font-size: 14px;
        }
        
        textarea {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            transition: all 0.3s ease;
            color: #2d3748;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea::placeholder {
            color: #a0aec0;
        }
        
        button {
            width: 100%;
            padding: 14px;
            margin-top: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 12px;
            animation: slideIn 0.5s ease-out;
        }
        
        .result.safe {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
            border-left: 4px solid #22c55e;
        }
        
        .result.scam {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
            border-left: 4px solid #ef4444;
        }
        
        .result-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }
        
        .result-icon {
            font-size: 32px;
        }
        
        .result h2 {
            font-size: 22px;
            margin: 0;
        }
        
        .result.safe h2 {
            color: #22c55e;
        }
        
        .result.scam h2 {
            color: #ef4444;
        }
        
        .probability-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 15px;
        }
        
        .probability-fill {
            height: 100%;
            background: linear-gradient(90deg, #ef4444 0%, #f97316 50%, #eab308 100%);
            border-radius: 10px;
            transition: width 0.6s ease-out;
        }
        
        .probability-text {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-size: 13px;
            color: #718096;
        }
        
        .probability-value {
            font-weight: 700;
            color: #2d3748;
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 25px;
            }
            
            h1 {
                font-size: 24px;
            }
            
            .header-icon {
                font-size: 40px;
            }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="header-icon">
            <i class="fas fa-shield-alt"></i>
        </div>
        <h1>Scam Detection</h1>
        <p class="subtitle">Analyze messages to detect potential scams</p>
    </div>

    <form method="POST">
        <div class="form-group">
            <label for="message">
                <i class="fas fa-envelope"></i> Enter Message
            </label>
            <textarea id="message" name="message" placeholder="Paste the message you want to analyze..." required></textarea>
        </div>
        <button type="submit">
            <i class="fas fa-search"></i> Analyze Message
        </button>
    </form>

    {% if result %}
        <div class="result {% if 'Safe' in result %}safe{% else %}scam{% endif %}">
            <div class="result-header">
                <div class="result-icon">
                    {% if 'Safe' in result %}
                        <i class="fas fa-check-circle"></i>
                    {% else %}
                        <i class="fas fa-exclamation-circle"></i>
                    {% endif %}
                </div>
                <h2>{{ result }}</h2>
            </div>
            
            <div class="probability-bar">
                <div class="probability-fill" style="width: {{ probability }}%"></div>
            </div>
            
            <div class="probability-text">
                <span>Scam Probability</span>
                <span class="probability-value">{{ probability }}%</span>
            </div>
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
