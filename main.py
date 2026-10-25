from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

queue = []
TARGET_SID = "motovationai"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Build Logic HTTP Typewriter</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e24; color: #fff; text-align: center; padding: 50px; }
        .card { background-color: #2a2a35; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0 8px 16px rgba(0,0,0,0.3); max-width: 400px; width: 100%; }
        input[type="text"] { width: 90%; padding: 10px; margin: 10px 0; border: none; border-radius: 6px; background-color: #3b3b4f; color: #fff; font-size: 16px; }
        button { background-color: #00a2ff; color: white; border: none; padding: 12px 20px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; transition: 0.2s; width: 95%; margin-top: 15px; }
        button:hover { background-color: #007cc7; }
        .spam-btn { background-color: #ef4444; }
        .spam-btn:hover { background-color: #dc2626; }
        .spam-btn.active { background-color: #22c55e; animation: pulse 1s infinite; }
        .status { margin-top: 15px; color: #a3e635; font-weight: bold; }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 Build Logic Typewriter</h2>
        <p>Locked Session: <strong>motovationai</strong></p>
        
        <form action="/send" method="POST" id="msgForm">
            <label for="msg">Message to Send:</label>
            <input type="text" id="msg" name="msg" placeholder="HELLO WORLD" required autocomplete="off">
            
            <button type="submit">Transmit to Queue</button>
            <button type="button" id="spamBtn" class="spam-btn">Spam Message (1s)</button>
        </form>
        <div id="statusBox" class="status"></div>
    </div>

    <script>
        let spamInterval = null;
        const spamBtn = document.getElementById('spamBtn');
        const msgInput = document.getElementById('msg');
        const statusBox = document.getElementById('statusBox');

        spamBtn.addEventListener('click', () => {
            if (spamInterval) {
                clearInterval(spamInterval);
                spamInterval = null;
                spamBtn.textContent = 'Spam Message (1s)';
                spamBtn.classList.remove('active');
                statusBox.textContent = 'Spam stopped.';
            } else {
                const message = msgInput.value.trim();
                if (!message) {
                    alert('Please enter a message first!');
                    return;
                }
                
                spamBtn.textContent = 'Spamming... (Click to Stop)';
                spamBtn.classList.add('active');
                
                // Function to send the request via background fetch
                const sendRequest = () => {
                    const formData = new FormData();
                    formData.append('msg', msgInput.value);

                    fetch('/send', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => {
                        statusBox.textContent = '✓ Spammed message at ' + new Date().toLocaleTimeString();
                    })
                    .catch(err => {
                        statusBox.textContent = 'Error sending spam packet.';
                    });
                };

                sendRequest(); // Run immediately first
                spamInterval = setInterval(sendRequest, 1000); // Repeat every 1000ms (1 second)
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/send', methods=['POST'])
def send_text():
    global queue
    msg = request.form.get('msg', '').upper()
    if not msg:
        return "Error: Message is required.", 400
    queue = [ord(char) for char in msg]
    return "Success"

@app.route('/get_char', methods=['GET'])
def get_character():
    global queue
    client_sid = request.headers.get('sid') or request.args.get('sid')
    
    if client_sid and client_sid.strip().lower() != TARGET_SID.lower():
        response = make_response("0")
        response.headers['Content-Type'] = 'text/plain'
        return response

    if len(queue) > 0:
        next_char = str(queue.pop(0))
    else:
        next_char = "0"
        
    response = make_response(next_char)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
