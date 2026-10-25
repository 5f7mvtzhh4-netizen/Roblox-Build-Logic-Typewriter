from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

queues = {}

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
        .status { margin-top: 15px; color: #a3e635; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 Build Logic Typewriter</h2>
        <p>Type your message below to queue it for Roblox.</p>
        
        <form action="/send" method="POST">
            <label for="sid">Session ID (Any 4-digit number):</label>
            <input type="text" id="sid" name="sid" placeholder="e.g. 1234" required autocomplete="off">
            
            <label for="msg">Message to Send:</label>
            <input type="text" id="msg" name="msg" placeholder="HELLO WORLD" required autocomplete="off">
            
            <button type="submit">Transmit to Queue</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/send', methods=['POST'])
def send_text():
    sid = request.form.get('sid', '').strip()
    msg = request.form.get('msg', '').upper()
    
    if not sid or not msg:
        return "Error: Session ID and Message are required.", 400
        
    char_codes = [ord(char) for char in msg]
    queues[sid] = char_codes
    
    return render_template_string(HTML_PAGE + f'<div class="status">✓ Enqueued {len(char_codes)} characters for SID {sid}! Ready for your transmitter.</div>')

@app.route('/get_char', methods=['GET'])
def get_character():
    sid = request.args.get('sid')
    
    if sid in queues and len(queues[sid]) > 0:
        next_char = queues[sid].pop(0)
        return jsonify({"char_code": next_char})
    
    return jsonify({"char_code": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
