from flask import Flask, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

# Route to run script1.py
@app.route('/zProbe')
def run_script1():
    subprocess.Popen(["python", "zProbe.py"], cwd="Flask2.0")
    return jsonify({"status": "Z-Probing started!"})

# Route to run script2.py
@app.route('/draw')
def run_script2():
    subprocess.Popen(["python", "draw.py"], cwd="Flask2.0")
    return jsonify({"status": "Drawing started!"})

# Route to run script3.py
@app.route('/recenter')
def run_script3():
    subprocess.Popen(["python", "recenter.py"], cwd="Flask2.0")
    return jsonify({"status": "Recentering started!"})

@app.route('/up')
def run_script4():
    subprocess.Popen(["python", "upJog.py"], cwd="Flask2.0")
    return jsonify({"status": "Jogging up started!"})

@app.route('/left')
def run_script5():
    subprocess.Popen(["python", "leftJog.py"], cwd="Flask2.0")
    return jsonify({"status": "Jogging left started!"})

@app.route('/right')
def run_script6():
    subprocess.Popen(["python", "right.py"], cwd="Flask2.0")
    return jsonify({"status": "Jogging right started!"})

@app.route('/down')
def run_script7():
    subprocess.Popen(["python", "downJog.py"], cwd="Flask2.0")
    return jsonify({"status": "Jogging down started!"})

if __name__ == '__main__':
    app.run(debug=True)
