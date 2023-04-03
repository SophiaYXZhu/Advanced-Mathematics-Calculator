from flask import Flask, render_template, request, redirect
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os
from triangles import calculate
from truthtable import output
from derivative import combine
from taylorexpansion import taylor_series
from graph import gen_topological_order

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

matplotlib.use('Agg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods=["POST", "GET"])
def graph():
    if request.method == 'POST':
        job_number = request.form.get("job_number")
        paths_length = request.form.get("paths_length")
        job_data = request.form.get("job_data")
        result = gen_topological_order(job_number, job_data, paths_length)
        result.update({"job_number": request.form.get("job_number"), "paths_length": request.form.get("paths_length"), "job_data": request.form.get("job_data")})
        return render_template("graph.html", result=result)
    else:
        return render_template("graph.html", result=None)

@app.route('/triangles', methods=["POST", "GET"])
def triangles():
    if request.method == 'POST':
        result = calculate(request)
        return render_template("triangles.html", result=result)
    else:
        return render_template("triangles.html", result=None)

@app.route('/truthtable', methods=['POST', 'GET'])
def truthtable():
    if request.method == 'POST':
        result = output(request)
        return render_template("truthtable.html", result=result)
    else:
        return render_template("truthtable.html", result=None)

@app.route('/derivative', methods=['POST', 'GET'])
def derivative():
    if request.method == 'POST':
        expression = request.form.get("expression")
        variable = request.form.get("variable")
        degree = request.form.get("degree")
        result = combine(expression, variable, degree)
        return render_template("derivative.html", result=result)
    else:
        return render_template("derivative.html", result=None)

# @app.route('/taylorexpansion', methods=['POST', 'GET'])
# def taylorexpansion():
#     if request.method == 'POST':
#         expression = request.form.get("expression")
#         variable = request.form.get("variable")
#         degree= request.form.get("degree")
#         center = request.form.get("center")
#         result = taylor_series(expression, variable, center, degree)
#         return render_template("taylorexpansion.html", result=result)
#     else:
#         return render_template("taylorexpansion.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)