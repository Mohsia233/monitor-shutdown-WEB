import psutil
from flask import Flask, render_template, jsonify, send_from_directory
import os
import platform

app = Flask(__name__)

def get_system_info():
    """获取系统资源使用情况"""
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    mem_total = round(mem.total / (1024 ** 3), 2)  # GB
    mem_used = round(mem.used / (1024 ** 3), 2)    # GB
    return {
        "cpu": cpu_percent,
        "mem": mem_percent,
        "mem_used": mem_used,
        "mem_total": mem_total
    }

@app.route('/')
def index():
    print("正在渲染 index.html")
    return render_template('index.html')

@app.route('/system-data')
def system_data():
    data = get_system_info()
    print(f"返回系统数据: {data}")
    return jsonify(data)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")
        return "关机命令已发送"
    else:
        return "此功能仅支持Windows系统"

# 添加 favicon 路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)