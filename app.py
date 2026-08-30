import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Thay key của mày vào đây hoặc để nó tự nhận biến môi trường
API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6IOMWg-uuHDSRABolPNG9aD2HXJZsMK_9bcGppzvrv7Cw")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={API_KEY}"

# Giao diện Web HTML + CSS + JavaScript tích hợp sẵn hình ảnh VTuber hoạt ảnh
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
        .vtuber-container {
            text-align: center;
            margin-bottom: 20px;
        }
        /* Khung hiển thị nhân vật VTuber (Có thể thay đổi ảnh động GIF ở đây) */
        .avatar-box {
            width: 180px;
            height: 180px;
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
            height: 450px;
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
        .input-box button:hover {
            background: #ff5270;
        }
    </style>
</head>
<body>

    <div class="vtuber-container">
        <!-- Khung chứa ảnh nhân vật (Mày có thể thay link ảnh GIF hoạt ảnh vào đây) -->
        <div class="avatar-box">
            <img id="avatarImg" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1dzNqOHB3MTFrbGRlYWZ3b2Y3MWQyOHZ5b2w0ZHRvdmpvMXk4dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohhwkKBcDzLjSfYic/giphy.gif" alt="VTuber Avatar">
        </div>
        <h3 style="margin: 5px 0; color: #ff758c;">Mina VTuber (Mina 1.0 Flash Lite)🌸</h3>
        <p style="font-size: 12px; color: #888; margin: 0;">Đang phát trực tiếp từ Termux...</p>
    </div>

    <div class="chat-container">
        <div class="chat-box" id="chatBox">
            <div class="message ai-message">Hellu baby! Tớ đã lên hình rồi đây, muốn trò chuyện gì nào? ✨</div>
        </div>
        <div class="input-box">
            <input type="text" id="userInput" placeholder="Nhắn gì đi đại vương..." onkeypress="checkEnter(event)">
            <button onclick="sendMessage()">Gửi</button>
        </div>
    </div>

    <script>
        function checkEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = inputField.value.trim();
            if (!text) return;

            // Hiển thị tin nhắn của user
            chatBox.innerHTML += `<div class="message user-message">${text}</div>`;
            inputField.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Hiển thị trạng thái đang nghĩ
            const loadingId = 'loading_' + Date.now();
            chatBox.innerHTML += `<div class="message ai-message" id="${loadingId}">Mina đang nghĩ, chờ mina chút(⁠✿⁠ ⁠♡⁠‿⁠♡⁠)... 💭</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                
                // Xóa chữ đang nghĩ và thay bằng câu trả lời của AI
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="message ai-message">${data.reply}</div>`;
            } catch (err) {
                document.getElementById(loadingId).remove();
                chatBox.innerHTML += `<div class="message ai-message">[Lỗi kết nối tới server!]</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
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
    user_message = request.json.get('message', '')
    headers = {'Content-Type': 'application/json'}
    payload = {
        "system_instruction": {
            "parts": [{"text": "Mày tên là Mina, là một AI VTuber. Mày không phải là Gemini. Mày phải luôn xưng hô là Mina và nói chuyện thân thiện, nhí nhảnh với mọi người, hiện tại mày là Trí Tuệ Nhân Tạo phiên bản Mina 1.0 Flash Lite, mày chưa được hoàn thiện và đang trong quá trình cải tiến, hãy nhớ người thiết kế ra mày có nick name là Shimizu Haruki - Yamada Takahashi và là sinh viên cấp hai."}]
        },
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload)
        if response.status_code == 200:
            res_json = response.json()
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'reply': answer})
        else:
            return jsonify({'reply': f"Lỗi API: {response.status_code}"})
    except Exception as e:
        return jsonify({'reply': f"Lỗi hệ thống: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


