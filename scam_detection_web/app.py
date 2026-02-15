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
            border-radius: 18px;
            overflow: hidden;
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
            border-radius: 28px;
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
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .tab-button {
            padding: 12px 24px;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            color: #718096;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 15px;
            width: auto;
            margin: 0;
            margin-top: -2px;
        }
        
        .tab-button:hover {
            color: #667eea;
            transform: none;
            box-shadow: none;
        }
        
        .tab-button.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
            animation: slideIn 0.3s ease-out;
        }
        
        input[type="url"], input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-family: inherit;
            font-size: 14px;
            transition: all 0.3s ease;
            color: #2d3748;
        }
        
        input[type="url"]:focus, input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        input[type="url"]::placeholder, input[type="text"]::placeholder {
            color: #a0aec0;
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
        
        /* Custom select with Font Awesome brand icons */
        .custom-select {
            position: relative;
            width: 100%;
            animation: slideInLeft 0.5s ease-out;
        }

        .custom-select-button {
            width: 100%;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            font-weight: 600;
            color: #2d3748;
            text-align: left;
        }

        .custom-select-button:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .custom-select-icon i { font-size: 16px; }

        .custom-select-caret i { margin-left: auto; color: #718096; }

        .custom-select-list {
            position: absolute;
            left: 0;
            right: 0;
            top: calc(100% + 8px);
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            max-height: 220px;
            overflow: auto;
            z-index: 50;
            display: none;
            padding: 8px 0;
        }

        .custom-select-list.show { display: block; }

        .custom-select-item {
            padding: 10px 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #2d3748;
        }

        .custom-select-item:hover {
            background: linear-gradient(135deg, #f7fafc 0%, #f1f5f9 100%);
        }

        .custom-select-item.selected {
            background: linear-gradient(135deg, #eef2ff 0%, #e9d5ff 100%);
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
            overflow: hidden;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
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
            border-radius: 30px;
            overflow: hidden;
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
        <p class="subtitle">Analyze messages and url to detect potential scams</p>
    </div>

    <form method="POST" id="analysisForm" onsubmit="showModal(event)">
        <div class="tabs">
            <button type="button" class="tab-button active" onclick="switchTab('message')">
                <i class="fas fa-envelope"></i> Message
            </button>
            <button type="button" class="tab-button" onclick="switchTab('url')">
                <i class="fas fa-link"></i> URL
            </button>
        </div>
        
        <!-- Message Tab -->
        <div id="message-tab" class="tab-content active">
            <div class="form-group">
                <label for="message">
                    <i class="fas fa-envelope"></i> Enter Message
                </label>
                <textarea id="message" name="message" placeholder="Paste the message you want to analyze..."></textarea>
            </div>
            <div class="form-group">
                <label for="message_source">
                    <i class="fas fa-comment-dots"></i> Message Source
                </label>
                <div class="custom-select" id="message_source_custom">
                    <button type="button" class="custom-select-button" id="message_source_button" aria-haspopup="listbox" aria-expanded="false">
                        <span class="custom-select-icon"><i class="fas fa-envelope"></i></span>
                        <span class="custom-select-label">Email</span>
                        <span class="custom-select-caret"><i class="fas fa-chevron-down"></i></span>
                    </button>
                    <ul class="custom-select-list" id="message_source_list" role="listbox" aria-labelledby="message_source_button">
                        <li class="custom-select-item selected" data-value="Email"><i class="fas fa-envelope"></i> Email</li>
                        <li class="custom-select-item" data-value="SMS"><i class="fas fa-sms"></i> SMS</li>
                        <li class="custom-select-item" data-value="WhatsApp"><i class="fab fa-whatsapp"></i> WhatsApp</li>
                        <li class="custom-select-item" data-value="Telegram"><i class="fab fa-telegram"></i> Telegram</li>
                        <li class="custom-select-item" data-value="Instagram"><i class="fab fa-instagram"></i> Instagram</li>
                        <li class="custom-select-item" data-value="Facebook"><i class="fab fa-facebook-f"></i> Facebook</li>
                        <li class="custom-select-item" data-value="Twitter"><i class="fab fa-twitter"></i> Twitter</li>
                        <li class="custom-select-item" data-value="Discord"><i class="fab fa-discord"></i> Discord</li>
                        <li class="custom-select-item" data-value="LinkedIn"><i class="fab fa-linkedin"></i> LinkedIn</li>
                    </ul>
                    <input type="hidden" id="message_source_input" name="message_source" value="Email">
                </div>
            </div>
            <button type="submit" id="analyzeMessageBtn">
                <i class="fas fa-search"></i> Analyze Message
            </button>
        </div>
        
        <!-- URL Tab -->
        <div id="url-tab" class="tab-content">
            <div class="form-group">
                <label for="url">
                    <i class="fas fa-link"></i> Enter URL
                </label>
                <input type="url" id="url" name="url" placeholder="Enter the URL you want to analyze (e.g., https://example.com)">
            </div>
            <button type="button" id="analyzeUrlBtn" onclick="analyzeURL()">
                <i class="fas fa-search"></i> Analyze URL
            </button>
        </div>
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
    function switchTab(tabName) {
        // Hide all tab contents
        document.getElementById('message-tab').classList.remove('active');
        document.getElementById('url-tab').classList.remove('active');
        
        // Deactivate all buttons
        const buttons = document.querySelectorAll('.tab-button');
        buttons.forEach(btn => btn.classList.remove('active'));
        
        // Show selected tab
        document.getElementById(tabName + '-tab').classList.add('active');
        
        // Activate clicked button
        event.target.closest('.tab-button').classList.add('active');
    }
    
    function showModal(event) {
        event.preventDefault();
        const message = document.getElementById('message').value.trim();
        
        if (!message) {
            alert('Please enter a message to analyze');
            return;
        }
        
        const modal = document.getElementById('analyzeModal');
        modal.classList.add('show');
        
        // Submit form
        document.getElementById('analysisForm').submit();
    }
    
    function analyzeURL() {
        const url = document.getElementById('url').value.trim();
        
        if (!url) {
            alert('Please enter a URL to analyze');
            return;
        }
        
        const modal = document.getElementById('analyzeModal');
        const modalText = modal.querySelector('.modal-text');
        modalText.textContent = 'Analyzing URL...';
        modal.classList.add('show');
        
        fetch('/predict-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            modal.classList.remove('show');
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            // Show result modal
            showURLResult(data.result, data.probability, url);
        })
        .catch(error => {
            modal.classList.remove('show');
            alert('Error analyzing URL: ' + error);
        });
    }
    
    function showURLResult(result, probability, url) {
        const resultHTML = `
        <div class="result-modal show" id="resultModal">
            <div class="result-modal-content ${result.includes('Safe') ? 'safe' : 'scam'}">
                <div class="result-icon ${result.includes('Safe') ? 'safe' : 'scam'}">
                    ${result.includes('Safe') ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-exclamation-circle"></i>'}
                </div>
                <h2>${result}</h2>
                <div class="source-info">
                    <i class="fas fa-info-circle"></i> URL: <strong>${url}</strong>
                </div>
                
                <div class="probability-bar">
                    <div class="probability-fill" style="width: ${probability}%"></div>
                </div>
                
                <div class="probability-text">
                    <span>Scam Probability</span>
                    <span class="probability-value">${probability}%</span>
                </div>
                
                <button class="reset-button" onclick="resetForm()">
                    <i class="fas fa-redo"></i> Check Another URL
                </button>
            </div>
        </div>
        `;
        
        const container = document.querySelector('.container');
        const oldResult = document.getElementById('resultModal');
        if (oldResult) {
            oldResult.remove();
        }
        container.insertAdjacentHTML('afterend', resultHTML);
    }
    
    function resetForm() {
        document.getElementById('analysisForm').reset();
        document.getElementById('message').value = '';
        document.getElementById('url').value = '';
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
    
    // Handle form submission for message analysis
    document.getElementById('analysisForm').addEventListener('submit', function(e) {
        if (document.getElementById('message-tab').classList.contains('active')) {
            showModal(e);
        }
    });
    
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
    
    // Custom select (message source) behavior using Font Awesome icons
    (function() {
        const customSelect = document.getElementById('message_source_custom');
        if (!customSelect) return;

        const button = document.getElementById('message_source_button');
        const list = document.getElementById('message_source_list');
        const hiddenInput = document.getElementById('message_source_input');
        const labelSpan = button.querySelector('.custom-select-label');
        const iconElem = button.querySelector('.custom-select-icon i');

        function closeList() {
            list.classList.remove('show');
            button.setAttribute('aria-expanded', 'false');
        }

        button.addEventListener('click', function(e) {
            const isOpen = list.classList.contains('show');
            if (isOpen) closeList(); else {
                list.classList.add('show');
                button.setAttribute('aria-expanded', 'true');
            }
        });

        list.addEventListener('click', function(e) {
            const item = e.target.closest('.custom-select-item');
            if (!item) return;

            // update selection
            const value = item.getAttribute('data-value');
            const icon = item.querySelector('i');
            hiddenInput.value = value;
            labelSpan.textContent = item.textContent.trim();
            iconElem.className = icon.className;

            // mark selected
            const prev = list.querySelector('.custom-select-item.selected');
            if (prev) prev.classList.remove('selected');
            item.classList.add('selected');

            // subtle animation
            button.style.transform = 'scale(0.98)';
            setTimeout(() => { button.style.transform = 'scale(1)'; }, 100);

            closeList();
        });

        // close when clicking outside
        document.addEventListener('click', function(e) {
            if (!customSelect.contains(e.target)) closeList();
        });

        // keyboard support (toggle)
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                button.click();
            }
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const first = list.querySelector('.custom-select-item');
                if (first) first.focus();
            }
        });
    })();
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

@app.route("/predict-url", methods=["POST"])
def url_prediction():
    try:
        data = request.get_json()
        url = data.get("url", "").strip()
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        prediction, probability = predict_url(url)
        result = "⚠️ Scam URL" if prediction == 1 else "✅ Safe URL"
        
        return jsonify({
            "result": result,
            "probability": round(probability, 2),
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
