from flask import Flask, render_template_string, jsonify
from miio import Yeelight, DeviceException

app = Flask(__name__)

LAMP_IP = "192.168.2.101"
LAMP_TOKEN = "88e2d4e75f2644f8f5d4363fbc986c11"

try:
    lamp = Yeelight(LAMP_IP, LAMP_TOKEN)
except Exception as e:
    print(f"初始化连接失败: {e}")

# 定义简单的网页 HTML
HTML_PAGE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的米家台灯控制</title>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background-color: #f0f2f5; }
        .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #333; }
        button {
            padding: 15px 30px; font-size: 18px; margin: 10px; border: none; border-radius: 8px; cursor: pointer; transition: 0.2s;
        }
        .btn-on { background-color: #4CAF50; color: white; }
        .btn-off { background-color: #f44336; color: white; }
        button:hover { opacity: 0.9; transform: scale(1.05); }
        #status { margin-top: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="card">
        <h1>💡 台灯控制中心</h1>
        <p>设备: Yeelight Lamp1</p>
        <div>
            <button class="btn-on" onclick="control('on')">开灯</button>
            <button class="btn-off" onclick="control('off')">关灯</button>
        </div>
        <div id="status">准备就绪</div>
    </div>

    <script>
        function control(action) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerText = '正在发送指令...';
            
            fetch('/' + action)
                .then(response => response.json())
                .then(data => {
                    statusDiv.innerText = data.message;
                    if(data.success) {
                        statusDiv.style.color = 'green';
                    } else {
                        statusDiv.style.color = 'red';
                    }
                })
                .catch(err => {
                    statusDiv.innerText = '请求失败，请检查服务器';
                    statusDiv.style.color = 'red';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/on')
def turn_on():
    try:
        lamp.on()
        return jsonify({"success": True, "message": "已开启"})
    except DeviceException as e:
        return jsonify({"success": False, "message": f"控制失败: {str(e)}"})

@app.route('/off')
def turn_off():
    try:
        lamp.off()
        return jsonify({"success": True, "message": "已关闭"})
    except DeviceException as e:
        return jsonify({"success": False, "message": f"控制失败: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2778)
