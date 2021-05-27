import flask
import math
from flask import Flask, render_template, request, jsonify
import os
import sys
import copy

sys.path.insert(0, './')
#sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
#sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
from user_interface import cs_to_html
from user_interface import form_values
from user_interface import stiffener_transform
from deck_and_initial_cs import initial_cs
from deck_and_initial_cs import deck
from data_and_defaults import defaults
from data_and_defaults import data
from assembly import merge
from cs_analysis_tool import cs_analysis_tool
from cs_optimization_tool import opt_iterative_steps
from cs_optimization_tool import opt_equal_pressure

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Startpage
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

#Input Page 1 Optimize
@app.route('/optimize_step_1', methods = ['GET'])
def optimize():
    form_values.values = copy.deepcopy(form_values.default_cs)
    val = form_values.values
    first_cs = initial_cs.create_initial_cs(val.get("b_sup"), val.get("b_inf"), val.get("h"), val.get("t_side"), val.get("t_deck"), val.get("t_btm"))
    image = cs_to_html.print_cs(first_cs)
    return render_template('optimize_input.html', image = image, content = val)

#Input Page 1 Optimize
@app.route('/optimize_step_1', methods = ['POST'])
def optimize_input_1():
    val = None
    try:
        b_sup = int(request.form['b_sup'])
        b_inf = int(request.form['b_inf'])
        h = int(request.form['h'])
        a = int(request.form['a'])
        L_e = int(request.form['L_e'])
        form_values.values = copy.deepcopy(form_values.default_cs)
        val = form_values.values
        val.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "a":a, "L_e":L_e})
    except KeyError:
        val = form_values.values

    first_cs = initial_cs.create_initial_cs(val.get("b_sup"), val.get("b_inf"), val.get("h"), 1,1,1)
    image = cs_to_html.print_cs(first_cs)
    return render_template('optimize_input.html', image = image, content = val)

#Input Page 2 Optimize
@app.route('/optimize_step_2', methods = ['POST'])
def optimize_input_2():
    b_sup = int(request.form['b_sup'])
    b_inf = int(request.form['b_inf'])
    h = int(request.form['h'])
    a = int(request.form['a'])
    L_e = int(request.form['L_e'])
    form_values.values = copy.deepcopy(form_values.default_cs)
    val = form_values.values
    val.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "a":a, "L_e":L_e})
    return render_template('load_input.html')


#Resultpage Optimize
@app.route('/results_optimize', methods = ['POST'])
def resultpage_optimize():
    #set defaults
    cs_position = request.form["cs_position"]
    data.input_data.update({"cs_position": cs_position})
    #read input
    val = form_values.values
    M_Ed = int(request.form['M_Ed'])*10**6
    V_Ed = int(request.form['V_Ed'])*10**3
    T_Ed = int(request.form['T_Ed'])*10**6
    data.input_data.update({"M_Ed":M_Ed, "V_Ed":V_Ed, "T_Ed":T_Ed})
    f_y = int(request.form['fy'])
    data.constants.update({"f_y":f_y})
    data.input_data.update({"b_sup":val.get("b_sup"), "b_inf":val.get("b_inf"), "h":val.get("h"), "a":val.get("a"), "L_e":val.get("L_e"), "t_deck":defaults.t_deck})
    optimizer_num = int(request.form['opt'])
    goal = int(request.form['goal'])
    data.input_data.update({"goal":goal})
    welding_cost = int(request.form['welding_cost'])
    data.input_data.update({"welding_cost":welding_cost})
    steel_cost = int(request.form['material_cost'])
    data.input_data.update({"steel_cost":steel_cost})
    try:
        ei = int(request.form['ei'])*10**3
        data.input_data.update({"ei":ei})
    except KeyError:
        pass 
    if optimizer_num == 0:
        opt_equal_pressure.opt_eqpressure()
    else:
        opt_iterative_steps.optimize()
    return render_template('resultpage_optimize.html')

#Input Page 1 Analysis Tool
@app.route('/cs_analysis_step_1', methods = ['GET'])
def cs_analysis():
    form_values.content = copy.deepcopy(form_values.default_cs)
    cont = form_values.content
    data.input_data.update({"a":cont.get("a")})
    first_cs = initial_cs.create_initial_cs(cont.get("b_sup"), cont.get("b_inf"), cont.get("h"), cont.get("t_side"), cont.get("t_deck"), cont.get("t_btm"))
    deck_stiffeners = deck.deck(cont.get("b_sup"), False)
    form_values.stiffeners = []
    form_values.stiffeners += deck_stiffeners
    end_cs = merge.merge(first_cs, form_values.stiffeners)
    image = cs_to_html.print_cs(end_cs)
    return render_template('geometry_input.html', image = image, content = cont)

#Input Page 1 Analysis Tool
@app.route('/cs_analysis_step_1', methods = ['POST'])
def cs_analysis_input_1():
    cont = None
    try:
        b_sup = int(request.form['b_sup'])
        b_inf = int(request.form['b_inf'])
        h = int(request.form['h'])
        t_side = int(request.form['t_side'])
        t_btm = int(request.form['t_btm'])
        num_side = int(request.form['num_side'])
        num_btm = int(request.form['num_btm'])
        a = int(request.form['a'])
        L_e = int(request.form['L_e'])
        form_values.content = copy.deepcopy(form_values.default_cs)
        cont = form_values.content
        cont.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "t_side":t_side, "t_btm":t_btm, "num_side":num_side, "num_btm":num_btm, "a":a, "L_e":L_e})

        for i in range(num_side):
            code = ["location" + str(i+1), "b_sup" + str(i+1), "b_inf" + str(i+1), "h" + str(i+1), "t" + str(i+1)]
            location_st = float(request.form[code[0]])
            b_sup_st = float(request.form[code[1]])
            b_inf_st = float(request.form[code[2]])
            h_st = float(request.form[code[3]])
            t_st = float(request.form[code[4]])
            cont.update({code[0]:location_st, code[1]:b_sup_st, code[2]:b_inf_st, code[3]:h_st, code[4]:t_st})
        sym = math.ceil(num_btm/2)
        for i in range(30, 30+sym, 1):
            code = ["location" + str(i+1), "b_sup" + str(i+1), "b_inf" + str(i+1), "h" + str(i+1), "t" + str(i+1)]
            #try except clause because of disabled field
            try:
                location_st = float(request.form[code[0]])
            except KeyError:
                location_st = 0
            b_sup_st = float(request.form[code[1]])
            b_inf_st = float(request.form[code[2]])
            h_st = float(request.form[code[3]])
            t_st = float(request.form[code[4]])
            cont.update({code[0]:location_st, code[1]:b_sup_st, code[2]:b_inf_st, code[3]:h_st, code[4]:t_st})
    except KeyError:
        cont = form_values.content
        a = cont.get("a")
    first_cs = initial_cs.create_initial_cs(cont.get("b_sup"), cont.get("b_inf"), cont.get("h"), cont.get("t_side"), cont.get("t_deck"), cont.get("t_btm"))
    data.input_data.update({"a":a})
    deck_stiffeners = deck.deck(cont.get("b_sup"), False)
    num_top = len(deck_stiffeners)
    cont.update({"num_top":num_top})
    form_values.stiffeners = []
    form_values.stiffeners += deck_stiffeners
    stiffener_transform.input_to_prop(cont.get("num_top"), cont.get("num_side"), cont.get("num_btm"))
    rest_stiffeners = stiffener_transform.prop_to_draw(first_cs)
    form_values.stiffeners += rest_stiffeners
    end_cs = merge.merge(first_cs, form_values.stiffeners)
    image = cs_to_html.print_cs(end_cs)
    return render_template('geometry_input.html', content = cont, image = image)

#Input Page 2 Analysis Tool
@app.route('/cs_analysis_step_2', methods = ['POST'])
def cs_analysis_input_2():
    b_sup = int(request.form['b_sup'])
    b_inf = int(request.form['b_inf'])
    h = int(request.form['h'])
    t_side = int(request.form['t_side'])
    t_btm = int(request.form['t_btm'])
    num_side = int(request.form['num_side'])
    num_btm = int(request.form['num_btm'])
    a = int(request.form['a'])
    L_e = int(request.form['L_e'])
    form_values.content = copy.deepcopy(form_values.default_cs)
    cont = form_values.content
    cont.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "t_side":t_side, "t_btm":t_btm, "num_side":num_side, "num_btm":num_btm, "a":a, "L_e":L_e})

    for i in range(num_side):
        code = ["location" + str(i+1), "b_sup" + str(i+1), "b_inf" + str(i+1), "h" + str(i+1), "t" + str(i+1)]
        location_st = float(request.form[code[0]])
        b_sup_st = float(request.form[code[1]])
        b_inf_st = float(request.form[code[2]])
        h_st = float(request.form[code[3]])
        t_st = float(request.form[code[4]])
        cont.update({code[0]:location_st, code[1]:b_sup_st, code[2]:b_inf_st, code[3]:h_st, code[4]:t_st})
    sym = math.ceil(num_btm/2)
    for i in range(30, 30+sym, 1):
        code = ["location" + str(i+1), "b_sup" + str(i+1), "b_inf" + str(i+1), "h" + str(i+1), "t" + str(i+1)]
        #try except clause because of disabled field
        try:
            location_st = float(request.form[code[0]])
        except KeyError:
            location_st = 0
        b_sup_st = float(request.form[code[1]])
        b_inf_st = float(request.form[code[2]])
        h_st = float(request.form[code[3]])
        t_st = float(request.form[code[4]])
        cont.update({code[0]:location_st, code[1]:b_sup_st, code[2]:b_inf_st, code[3]:h_st, code[4]:t_st})
    first_cs = initial_cs.create_initial_cs(cont.get("b_sup"), cont.get("b_inf"), cont.get("h"), cont.get("t_side"), cont.get("t_deck"), cont.get("t_btm"))
    data.input_data.update({"a":cont.get("a")})
    deck_stiffeners = deck.deck(cont.get("b_sup"), False)
    num_top = len(deck_stiffeners)
    cont.update({"num_top":num_top})
    stiffener_transform.input_to_prop(cont.get("num_top"), cont.get("num_side"), cont.get("num_btm"))
    data.input_data.update({"b_sup":cont.get("b_sup"), "b_inf":cont.get("b_inf"), "h":cont.get("h"), \
    "t_deck":defaults.t_deck, "t_side":cont.get("t_side"), "t_bottom":cont.get("t_btm"), "a":cont.get("a"), "L_e":cont.get("L_e")})
    return render_template('forces_input.html')

#Resultpage Analysis Tool
@app.route('/results_analysis', methods = ['POST'])
def resultpage_analysis():
    cs_position = request.form["cs_position"]
    data.input_data.update({"cs_position": cs_position})
    M_Ed = int(request.form['M_Ed'])*10**6
    V_Ed = int(request.form['V_Ed'])*10**3
    T_Ed = int(request.form['T_Ed'])*10**6
    data.input_data.update({"M_Ed":M_Ed, "V_Ed":V_Ed, "T_Ed":T_Ed})
    f_y = int(request.form['fy'])
    data.constants.update({"f_y":f_y})
    results = cs_analysis_tool.cs_analysis_gui()
    return render_template('resultpage_analysis.html', results = results)

#Run GUI
if __name__ == '__main__':
   app.run(debug = True)
