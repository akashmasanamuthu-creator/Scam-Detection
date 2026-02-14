from flask import Flask, render_template_string, request, jsonify
from model import predict_message, predict_url

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
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.7; }
        }
        
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
            50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.6); }
        }
        
        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInRight {
            from { transform: translateX(100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(240, 147, 251, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            animation: float 6s infinite ease-in-out;
        }
        
        .particle:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
        .particle:nth-child(2) { left: 80%; top: 80%; animation-delay: 1s; }
        .particle:nth-child(3) { left: 50%; top: 10%; animation-delay: 2s; }
        .particle:nth-child(4) { left: 90%; top: 30%; animation-delay: 3s; }
        .particle:nth-child(5) { left: 20%; top: 70%; animation-delay: 4s; }
        
        .container {
            position: relative;
            z-index: 10;
        }
        
        .container {
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 500px;
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.5s ease-out;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
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
        
        @keyframes slideInPopup {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes spinnerSpin {
            to {
                transform: rotate(360deg);
            }
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .modal-content {
            background: white;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
            animation: slideInPopup 0.4s ease-out;
            min-width: 300px;
            max-width: 400px;
        }
        
        .spinner {
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spinnerSpin 1s linear infinite;
            margin: 20px auto;
        }
        
        .modal-text {
            font-size: 18px;
            color: #2d3748;
            font-weight: 600;
            margin-top: 15px;
        }
        
        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
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
            position: relative;
            overflow: hidden;
        }
        
        button:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        button:hover:before {
            left: 100%;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .social-media-options {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        
        .message-source-select {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-family: inherit;
            font-size: 14px;
            font-weight: 600;
            color: #2d3748;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 12px center;
            background-size: 20px;
            padding-right: 40px;
            animation: slideInLeft 0.5s ease-out;
        }
        
        .message-source-select:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            background-color: #f7fafc;
        }
        
        .message-source-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background-color: white;
        }
        
        .message-source-select option {
            padding: 10px;
            background: white;
            color: #2d3748;
        }
        
        .message-source-select option:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 12px;
            animation: slideInResult 0.6s ease-out;
        }
        
        @keyframes slideInResult {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .result.safe {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
            border-left: 4px solid #22c55e;
        }
        
        .result.scam {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
            border-left: 4px solid #ef4444;
        }
        
        .result-modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            padding: 20px;
            overflow-y: auto;
        }
        
        .result-modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease-out;
        }
        
        .result-modal-content {
            background: white;
            padding: 60px 40px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.3);
            animation: bounceIn 0.6s ease-out;
            max-width: 600px;
            width: 100%;
            min-height: auto;
        }
        
        .result-modal-content.safe {
            border-top: 6px solid #22c55e;
            border-top-left-radius: 25px;
            border-top-right-radius: 25px;
        }
        
        .result-modal-content.scam {
            border-top: 6px solid #ef4444;
            border-top-left-radius: 25px;
            border-top-right-radius: 25px;
        }
        
        .result-modal .result-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounceIn 0.8s ease-out;
        }
        
        .result-modal .result-icon.safe {
            color: #22c55e;
        }
        
        .result-modal .result-icon.scam {
            color: #ef4444;
        }
        
        .result-modal h2 {
            font-size: 42px;
            margin: 20px 0;
            animation: slideInRight 0.6s ease-out;
        }
        
        .result-modal .probability-bar {
            width: 100%;
            height: 12px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin: 30px 0;
            animation: slideInLeft 0.8s ease-out;
        }
        
        .result-modal .probability-fill {
            height: 100%;
            background: linear-gradient(90deg, #ef4444 0%, #f97316 50%, #eab308 100%);
            border-radius: 10px;
            transition: width 1s ease-out;
        }
        
        .result-modal .probability-text {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 16px;
            color: #718096;
            animation: slideInRight 0.8s ease-out;
        }
        
        .result-modal .probability-value {
            font-weight: 700;
            font-size: 20px;
            color: #2d3748;
        }
        
        .result-modal .source-info {
            margin: 25px 0;
            padding: 15px;
            background: #f7fafc;
            border-radius: 10px;
            font-size: 16px;
            color: #2d3748;
            animation: slideInLeft 1s ease-out;
        }
        
        .reset-button {
            width: 100%;
            padding: 16px;
            margin-top: 30px;
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
            animation: slideInRight 1s ease-out;
        }
        
        .reset-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .reset-button:active {
            transform: translateY(0);
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
        .footer {
            position: fixed;
            right: 18px;
            bottom: 16px;
            background: rgba(255,255,255,0.92);
            padding: 10px 14px;
            border-radius: 10px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            font-size: 13px;
            color: #2d3748;
            text-align: right;
            line-height: 1.2;
            opacity: 0.95;
            z-index: 5;
        }
        .footer .names {
            margin-top: 4px;
            font-weight: 600;
        }
    </style>
</head>
<body>
<div class="floating-particles">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
</div>

<div id="analyzeModal" class="modal">
    <div class="modal-content">
        <div class="spinner"></div>
        <div class="modal-text">Analyzing Message...</div>
    </div>
</div>
<div class="container">
    <div class="header">
        <div class="header-icon">
            <i class="fas fa-shield-alt"></i>
        </div>
        <h1>Scam Detection</h1>
        <p class="subtitle">Analyze messages to detect potential scams</p>
    </div>

    <form method="POST" id="analysisForm" onsubmit="showModal(event)">
        <div class="form-group">
            <label for="message">
                <i class="fas fa-envelope"></i> Enter Message
            </label>
            <textarea id="message" name="message" placeholder="Paste the message you want to analyze..." required></textarea>
        </div>
        <div class="form-group">
            <label for="message_source">
                <i class="fas fa-comment-dots"></i> Message Source
            </label>
            <select id="message_source" name="message_source" class="message-source-select" required>
                <option value="Email" selected>📧 Email</option>
                <option value="SMS">📱 SMS</option>
                <option value="WhatsApp">💚 WhatsApp</option>
                <option value="Telegram">💙 Telegram</option>
                <option value="Instagram">📷 Instagram</option>
                <option value="Facebook">👥 Facebook</option>
                <option value="Twitter">🐦 Twitter</option>
                <option value="Discord">🎮 Discord</option>
                <option value="LinkedIn">💼 LinkedIn</option>
            </select>
        </div>
        <button type="submit">
            <i class="fas fa-search"></i> Analyze Message
        </button>
    </form>

    {% if result %}
        <div class="result-modal show" id="resultModal">
            <div class="result-modal-content {% if 'Safe' in result %}safe{% else %}scam{% endif %}">
                <div class="result-icon {% if 'Safe' in result %}safe{% else %}scam{% endif %}">
                    {% if 'Safe' in result %}
                        <i class="fas fa-check-circle"></i>
                    {% else %}
                        <i class="fas fa-exclamation-circle"></i>
                    {% endif %}
                </div>
                <h2>{{ result }}</h2>
                {% if message_source %}
                    <div class="source-info">
                        <i class="fas fa-info-circle"></i> Message source: <strong>{{ message_source }}</strong>
                    </div>
                {% endif %}
                
                <div class="probability-bar">
                    <div class="probability-fill" style="width: {{ probability }}%"></div>
                </div>
                
                <div class="probability-text">
                    <span>Scam Probability</span>
                    <span class="probability-value">{{ probability }}%</span>
                </div>
                
                <button class="reset-button" onclick="resetForm()">
                    <i class="fas fa-redo"></i> Check Another Message
                </button>
            </div>
        </div>
    {% endif %}
</div>
<div class="footer">Made by -<br>Akash M<br>Ganesh B<br>Mohith MS<br>Harish G<br>Gopi B</div>

<script>
    function showModal(event) {
        const modal = document.getElementById('analyzeModal');
        modal.classList.add('show');
        // Form will still submit and page will reload
    }
    
    function resetForm() {
        document.getElementById('analysisForm').reset();
        const resultModal = document.getElementById('resultModal');
        if (resultModal) {
            resultModal.classList.remove('show');
        }
        const analyzeModal = document.getElementById('analyzeModal');
        if (analyzeModal) {
            analyzeModal.classList.remove('show');
        }
        window.location.href = '/';
    }
    
    // Hide loading modal when page loads (after form submission)
    window.addEventListener('load', function() {
        const modal = document.getElementById('analyzeModal');
        if (modal) {
            modal.classList.remove('show');
        }
        // Trigger the animation for the result modal
        const resultModal = document.getElementById('resultModal');
        if (resultModal) {
            resultModal.classList.add('show');
        }
    });
    
    // Add smooth transitions for dropdown
    const messageSourceSelect = document.getElementById('message_source');
    if (messageSourceSelect) {
        messageSourceSelect.addEventListener('change', function() {
            // Add a subtle animation effect on selection
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
        
        messageSourceSelect.addEventListener('focus', function() {
            this.style.borderColor = '#667eea';
        });
        
        messageSourceSelect.addEventListener('blur', function() {
            this.style.borderColor = '#e2e8f0';
        });
    }
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    probability = None
    message_source = None

    if request.method == "POST":
        message = request.form["message"]
        message_source = request.form.get("message_source", "Email")
        prediction, probability = predict_message(message)
        result = "⚠️ Scam Message" if prediction == 1 else "✅ Safe Message"

    return render_template_string(
        HTML_PAGE,
        result=result,
        probability=probability,
        message_source=message_source
    )

if __name__ == "__main__":
    app.run(debug=True)
