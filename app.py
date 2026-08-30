import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VTuber AI Live</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .config-box {
            margin-bottom: 15px;
            background: #1e1e1e;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #333;
            width: 90%;
            max-width: 450px;
            display: flex;
        }
        .config-box input {
            flex: 1;
            padding: 8px;
            border: 1px solid #444;
            background: #121212;
            color: white;
            border-radius: 5px;
            outline: none;
            font-size: 13px;
        }
        .vtuber-container {
            text-align: center;
            margin-bottom: 15px;
        }
        .avatar-box {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px solid #ff758c;
            box-shadow: 0 0 20px rgba(255, 117, 140, 0.6);
            overflow: hidden;
            margin: 0 auto 10px auto;
            background-color: #222;
        }
        .avatar-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .chat-container {
            width: 90%;
            max-width: 450px;
            background: #1e1e1e;
            border-radius: 12px;
            border: 1px solid #333;
            display: flex;
            flex-direction: column;
            height: 400px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .chat-box {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            padding: 10px 14px;
            border-radius: 10px;
            max-width: 80%;
            word-wrap: break-word;
            font-size: 14px;
            white-space: pre-wrap;
        }
        .user-message {
            background: #007bff;
            color: white;
            align-self: flex-end;
        }
        .ai-message {
            background: #333;
            color: #ff758c;
            align-self: flex-start;
            border: 1px solid #444;
        }
        .input-box {
            display: flex;
            padding: 10px;
            border-top: 1px solid #333;
            background: #252525;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
        }
        .input-box input {
            flex: 1;
            padding: 10px;
            border: 1px solid #444;
            background: #121212;
            color: white;
            border-radius: 6px;
            outline: none;
        }
        .input-box button {
            background: #ff758c;
            color: white;
            border: none;
            padding: 0 15px;
            margin-left: 8px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="config-box">
        <input type="password" id="apiKeyInput" placeholder="Dán Gemini API Key của mày vào đây...">
    </div>

    <div class="vtuber-container">
        <div class="avatar-box">
            <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1dzNqOHB3MTFrbGRlYWZ3b2Y3MWQyOHZ5b2w0ZHRvdmpvMXk4dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohhwkKBcDzLjSfYic/giphy.gif" alt="VTuber Avatar">
        </div>
        <h3 style="margin: 3px 0; color: #ff758c;">Mina VTuber (Bản thử nghiệm 0.1) 🌸</h3>
    </div>

    <div class="chat-container">
        <div class="chat-box" id="chatBox">
            <div class="message ai-message">Hellu cục cưng! Nhớ nhập API Key vào ô trên rồi mới nhắn tin được với tớ nha, chỉ hỗ trợ key của Google thôi ạ, thông cảm cho bé nha✨</div>
        </div>
        <div class="input-box">
            <input type="text" id="userInput" placeholder="Nhắn gì đi đại vương..." onkeypress="checkEnter(event)">
            <button onclick="sendMessage()">Gửi</button>
        </div>
    </div>

    <script>
        function checkEnter(event) {
            if (event.key === 'Enter') sendMessage();
        }

        function appendMessage(text, sender) {
            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender === 'user' ? 'user-message' : 'ai-message'}`;
            msgDiv.textContent = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            return msgDiv;
        }

        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const apiKeyField = document.getElementById('apiKeyInput');
            
            const text = inputField.value.trim();
            const apiKey = apiKeyField.value.trim();

            if (!apiKey) {
                alert('Kìa, bé iu chưa nhập API Key kìa!');
                return;
            }
            if (!text) return;

            appendMessage(text, 'user');
            inputField.value = '';

            const loadingDiv = appendMessage('Mina đang nghĩ, chờ mina chút(⁠✿⁠ ⁠♡⁠‿⁠♡⁠)... 💭', 'ai');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, api_key: apiKey })
                });
                const data = await response.json();
                
                loadingDiv.remove();
                appendMessage(data.reply, 'ai');
            } catch (err) {
                loadingDiv.remove();
                appendMessage('[Lỗi kết nối tới server!]', 'ai');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_api_key = data.get('api_key', '')

    api_key = user_api_key or os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        return jsonify({'reply': "Nè, chưa nhập API Key kìa bé iu ơi!"})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "system_instruction": {
            "parts": [{"text": "Mày tên là Mina, là một AI VTuber. Mày không phải là Gemini. Mày phải luôn xưng hô là Mina và nói chuyện thân thiện, nhí nhảnh với mọi người, hiện tại mày là Trí Tuệ Nhân Tạo phiên bản Mina 1.0 Flash, mày chưa được hoàn thiện và đang trong quá trình cải tiến, hãy nhớ người thiết kế ra mày có nick name là Shimizu Haruki - Yamada Takahashi và là học sinh cấp hai. Hãy chỉ nói những điều cần thiết, hãy tỏ ra dễ thương vừa phải, không quá sến"}]
        },
     "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        
        if response.status_code == 200 and 'candidates' in res_json:
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'reply': answer})
        else:
            error_msg = res_json.get('error', {}).get('message', f"Mã lỗi HTTP: {response.status_code}")
            return jsonify({'reply': f"Google quạu rồi: {error_msg}"})
            
    except Exception as e:
        return jsonify({'reply': f"Lỗi code Python: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
