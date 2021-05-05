import flask
import math
from flask import Flask, render_template, request, jsonify
import os
import sys

sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
from web_interface import cs_to_html

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cs_analysis_step_1', methods = ['GET'])
def cs_analysis():
    content = {'b_sup':1534, 'b_inf':1234}
    return render_template('geometry_input.html', content = content)

@app.route('/optimize', methods = ['GET'])
def optimize():
    return render_template('optimize_input.html', a="Optimize")

@app.route('/cs_analysis_step_1', methods = ['POST'])
def cs_analysis_input_1():
    content = {}
    b_sup = int(request.form['b_sup'])
    b_inf = int(request.form['b_inf'])
    h = int(request.form['h'])
    t_side = int(request.form['t_side'])
    content.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "t_side":t_side})
    num_side = int(request.form['btm_stiffener_number'])
    #for i in range(num_side):
    #    try:
    #        b1 = int(request.form['hallo'])
    #    except KeyError:
    #        b1 = 10
    initial_cs = cs_to_html.create_initial_cs(b_sup, b_inf, h, t_side, t_side, t_side)
    image = cs_to_html.print_cs(initial_cs)
    file = open(r"web_interface\templates\figure.html", 'w')
    file.write(image)
    file.close()
    return render_template('geometry_input.html', content = content, image = image)

@app.route('/cs_analysis_step_2', methods = ['POST'])
def cs_analysis_input_2():
    return render_template('forces_input.html')

@app.route('/results', methods = ['GET'])
def reultpage():
    return render_template('resultpage.html')

if __name__ == '__main__':
   app.run(debug = True)
