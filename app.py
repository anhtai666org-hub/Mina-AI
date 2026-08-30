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
            margin-bottom: 10px;
            background: #1e1e1e;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #333;
            width: 90%;
            max-width: 450px;
            display: flex;
            flex-direction: column;
            gap: 8px;
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
        .file-upload-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }
        .btn-upload {
            border: 1px solid #ff4757;
            color: #ff4757;
            background-color: transparent;
            padding: 7px 15px;
            border-radius: 5px;
            font-size: 13px;
            cursor: pointer;
            width: 100%;
            box-sizing: border-box;
            text-align: center;
        }
        .btn-upload:hover {
            background-color: rgba(255, 71, 87, 0.1);
        }
        .file-upload-wrapper input[type=file] {
            font-size: 100px;
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            cursor: pointer;
        }
        .vtuber-container {
            text-align: center;
            margin-bottom: 10px;
        }
        .avatar-box {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            border: 4px solid #ff4757;
            box-shadow: 0 0 20px rgba(255, 71, 87, 0.6);
            overflow: hidden;
            margin: 0 auto 8px auto;
            background-color: #222;
            cursor: pointer;
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
            height: 380px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .chat-box {
            flex: 1;
            padding: 12px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            padding: 10px 14px;
            border-radius: 10px;
            max-width: 85%;
            word-wrap: break-word;
            font-size: 14px;
            white-space: pre-wrap;
        }
        .user-message {
            background: #ff4757;
            color: white;
            align-self: flex-end;
        }
        .ai-message {
            background: #333;
            color: #ff6b81;
            align-self: flex-start;
            border: 1px solid #444;
        }
        .message img {
            max-width: 100%;
            border-radius: 6px;
            margin-top: 5px;
            display: block;
        }
        .preview-container {
            padding: 5px 12px;
            background: #252525;
            display: none;
            align-items: center;
            gap: 10px;
            border-top: 1px solid #333;
        }
        .preview-container img {
            width: 40px;
            height: 40px;
            object-fit: cover;
            border-radius: 4px;
        }
        .preview-container span {
            font-size: 12px;
            color: #aaa;
            flex: 1;
        }
        .preview-container button {
            background: transparent;
            border: none;
            color: #ff4757;
            cursor: pointer;
            font-weight: bold;
        }
        .input-box {
            display: flex;
            padding: 10px;
            border-top: 1px solid #333;
            background: #252525;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
            align-items: center;
            gap: 5px;
        }
        .input-box input[type="text"] {
            flex: 1;
            padding: 9px;
            border: 1px solid #444;
            background: #121212;
            color: white;
            border-radius: 6px;
            outline: none;
            font-size: 13px;
        }
        .btn-attach {
            background: #333;
            color: white;
            border: 1px solid #555;
            padding: 9px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        .input-box button.btn-send {
            background: #ff4757;
            color: white;
            border: none;
            padding: 9px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="config-box">
        <input type="password" id="apiKeyInput" placeholder="Dán Gemini API Key của cậu vào đây...">
        <div class="file-upload-wrapper">
            <button class="btn-upload">Đổi Avatar Mina</button>
            <input type="file" id="avatarInput" accept="image/*">
        </div>
    </div>

    <div class="vtuber-container">
        <div class="avatar-box" onclick="document.getElementById('avatarInput').click()">
            <img id="minaAvatar" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="VTuber Avatar">
        </div>
        <h3 style="margin: 2px 0; color: #ff6b81;">Mina VTuber (v0.2) 🌸</h3>
    </div>

    <div class="chat-container">
        <div class="chat-box" id="chatBox">
            <div class="message ai-message">Hellu cậu iu! Tớ đã được update tính năng xem ảnh và vẽ tranh rồi đó nha ✨ Cậu nhập Key để nói chuyện với tớ đi nha, tớ chỉ hỗ trợ key Google mong cậu thông cảm nhiều nhoa, giờ cậu có thể chat, gửi ảnh, tạo ảnh rồi đó nhoa cậu ạ, nhập key đi!</div>
        </div>
        
        <div class="preview-container" id="previewContainer">
            <img id="imgPreview" src="" alt="Preview">
            <span id="imgName">Đã đính kèm ảnh</span>
            <button onclick="clearImage()">✕</button>
        </div>

        <div class="input-box">
            <label class="btn-attach" title="Gửi ảnh cho Mina">
                📷 <input type="file" id="chatImageInput" accept="image/*" style="display: none;" onchange="handleImageSelect(event)">
            </label>
            <input type="text" id="userInput" placeholder="Nhắn gì đi bé iu❤️..." onkeypress="checkEnter(event)">
            <button class="btn-send" onclick="sendMessage()">Gửi</button>
        </div>
    </div>

    <script>
        let currentBase64Image = null;
        let currentMimeType = null;

        function checkEnter(event) {
            if (event.key === 'Enter') sendMessage();
        }

        function appendMessage(content, sender, isImage = false) {
            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender === 'user' ? 'user-message' : 'ai-message'}`;
            
            if (isImage) {
                const img = document.createElement('img');
                img.src = content;
                msgDiv.appendChild(img);
            } else {
                msgDiv.textContent = content;
            }
            
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            return msgDiv;
        }

        function handleImageSelect(event) {
            const file = event.target.files[0];
            if (file) {
                currentMimeType = file.type;
                const reader = new FileReader();
                reader.onload = function(e) {
                    currentBase64Image = e.target.result.split(',')[1];
                    document.getElementById('imgPreview').src = e.target.result;
                    document.getElementById('imgName').textContent = file.name;
                    document.getElementById('previewContainer').style.display = 'flex';
                }
                reader.readAsDataURL(file);
            }
        }

        function clearImage() {
            currentBase64Image = null;
            currentMimeType = null;
            document.getElementById('chatImageInput').value = '';
            document.getElementById('previewContainer').style.display = 'none';
        }

        document.getElementById('avatarInput').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('minaAvatar').src = e.target.result;
                    localStorage.setItem('minaAvatar', e.target.result);
                }
                reader.readAsDataURL(file);
            }
        });

        window.onload = function() {
            const savedAvatar = localStorage.getItem('minaAvatar');
            if (savedAvatar) {
                document.getElementById('minaAvatar').src = savedAvatar;
            }
        }

        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const apiKeyField = document.getElementById('apiKeyInput');
            
            const text = inputField.value.trim();
            const apiKey = apiKeyField.value.trim();

            if (!apiKey) {
                alert('Nè, cậu iu chưa nhập API Key kìa!');
                return;
            }
            if (!text && !currentBase64Image) return;

            // Hiển thị tin nhắn người dùng
            if (currentBase64Image) {
                appendMessage(`data:${currentMimeType};base64,${currentBase64Image}`, 'user', true);
            }
            if (text) {
                appendMessage(text, 'user', false);
            }

            const imgToSend = currentBase64Image;
            const mimeToSend = currentMimeType;

            inputField.value = '';
            clearImage();

            const loadingDiv = appendMessage('Mina đang nghĩ, chờ chút(⁠✿⁠ ⁠♡⁠‿⁠♡⁠)... 💭', 'ai');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        message: text, 
                        api_key: apiKey,
                        image: imgToSend,
                        mime_type: mimeToSend
                    })
                });
                const data = await response.json();
                
                loadingDiv.remove();
                
                if (data.type === 'image') {
                    appendMessage(data.reply, 'ai', true);
                } else {
                    appendMessage(data.reply, 'ai', false);
                }
            } catch (err) {
                loadingDiv.remove();
                appendMessage('[Lỗi kết nối server!]', 'ai');
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
    img_data = data.get('image', '')
    mime_type = data.get('mime_type', 'image/jpeg')

    api_key = user_api_key or os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        return jsonify({'reply': "Kìa, cậu iu chưa nhập API Key kìa!"})

    # Kiểm tra xem người dùng có yêu cầu tạo/vẽ ảnh không
    lower_msg = user_message.lower()
    is_image_request = any(keyword in lower_msg for keyword in ["vẽ", "tạo ảnh", "generate image", "draw", "bức ảnh"])

    if is_image_request:
        # Sử dụng Pollinations AI (Miễn phí, không cần API Key phụ) để tạo ảnh chất lượng cao dựa trên prompt
        prompt_encoded = requests.utils.quote(user_message)
        image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}"
        return jsonify({
            'type': 'image',
            'reply': image_url
        })

    # Xử lý nhắn tin thông thường / Gửi ảnh cho Gemini 3.5 Flash Lite phân tích
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    parts = []
    if img_data:
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": img_data
            }
        })
    if user_message:
        parts.append({"text": user_message})
    else:
        parts.append({"text": "Hãy miêu tả bức ảnh này cho tớ nghe nhé!"})

    payload = {
        "system_instruction": {
            "parts": [{"text": "Mày tên là Mina, là một AI VTuber. Mày không phải là Gemini. Mày phải luôn xưng hô là Mina và nói chuyện thân thiện, nhí nhảnh với mọi người, hiện tại mày là Trí Tuệ Nhân Tạo phiên bản Mina 1.0 Flash, mày chưa được hoàn thiện và đang trong quá trình cải tiến, hãy nhớ người thiết kế ra mày có nick name là Shimizu Haruki - Yamada Takahashi và là học sinh cấp hai. Không Nói những điều thừa thãi, người dùng nếu muốn thiết kế tính cách cho mày qua chat hãy nghe theo nhân cách của nó đặt ra"}]
        },
        "contents": [{
            "parts": parts
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        
        if response.status_code == 200 and 'candidates' in res_json:
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'type': 'text', 'reply': answer})
        else:
            error_msg = res_json.get('error', {}).get('message', f"Mã lỗi HTTP: {response.status_code}")
            return jsonify({'type': 'text', 'reply': f"Google quạu rồi: {error_msg}"})
            
    except Exception as e:
        return jsonify({'type': 'text', 'reply': f"Lỗi code Python: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
