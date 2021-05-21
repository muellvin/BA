import flask
import math
from flask import Flask, render_template, request, jsonify
import os
import sys
import copy

sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
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

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/optimize_step_1', methods = ['GET'])
def optimize():
    defaults.do_deck_as_prop=False
    form_values.values = copy.deepcopy(form_values.default_cs)
    val = form_values.values
    initial_cs = cs_to_html.create_initial_cs(val.get("b_sup"), val.get("b_inf"), val.get("h"), val.get("t_side"), val.get("t_deck"), val.get("t_btm"))
    image = cs_to_html.print_cs(initial_cs)
    return render_template('optimize_input.html', image = image, content = val)

@app.route('/optimize_step_1', methods = ['POST'])
def optimize_input_1():
    defaults.do_deck_as_prop=False
    val = None
    try:
        b_sup = int(request.form['b_sup'])
        b_inf = int(request.form['b_inf'])
        h = int(request.form['h'])
        form_values.values = copy.deepcopy(form_values.default_cs)
        val = form_values.values
        val.update({"b_sup":b_sup, "b_inf":b_inf, "h":h})
    except KeyError:
        val = form_values.values
    first_cs = initial_cs.create_initial_cs(val.get("b_sup"), val.get("b_inf"), val.get("h"), 1,1,1)
    image = cs_to_html.print_cs(first_cs)
    return render_template('optimize_input.html', image = image, content = val)

@app.route('/optimize_step_2', methods = ['POST'])
def optimize_input_2():
    defaults.do_deck_as_prop=False
    b_sup = int(request.form['b_sup'])
    b_inf = int(request.form['b_inf'])
    h = int(request.form['h'])
    form_values.values = copy.deepcopy(form_values.default_cs)
    val = form_values.values
    val.update({"b_sup":b_sup, "b_inf":b_inf, "h":h})
    return render_template('load_input.html')


@app.route('/results_optimize', methods = ['POST'])
def resultpage_optimize():
    defaults.do_deck_as_prop=True
    #set defaults
    cs_a = 10000
    cs_L_e = 15000
    cs_bending_type = "sagging bending"
    cs_cs_position = "neither"
    data.input_data.update({"a": cs_a})
    data.input_data.update({"L_e": cs_L_e})
    data.input_data.update({"bending type": cs_bending_type})
    data.input_data.update({"cs position": cs_cs_position})
    #read input
    val = form_values.values
    M_Ed = int(request.form['M_Ed'])*10**6
    V_Ed = int(request.form['V_Ed'])*10**3
    T_Ed = int(request.form['T_Ed'])*10**6
    data.input_data.update({"M_Ed":M_Ed, "V_Ed":V_Ed, "T_Ed":T_Ed})
    f_y = int(request.form['fy'])
    data.constants.update({"f_y":f_y})
    data.input_data.update({"b_sup":val.get("b_sup"), "b_inf":val.get("b_inf"), "h":val.get("h"), "t_deck":14})
    optimizer_num = int(request.form['opt'])
    if optimizer_num == 0:
        opt_equal_pressure.opt_eqpressure()
    else:
        opt_iterative_steps.optimize()
    return render_template('resultpage_optimize.html')


@app.route('/cs_analysis_step_1', methods = ['GET'])
def cs_analysis():
    defaults.do_deck_as_prop=False
    form_values.content = copy.deepcopy(form_values.default_cs)
    cont = form_values.content
    first_cs = cs_to_html.create_initial_cs(cont.get("b_sup"), cont.get("b_inf"), cont.get("h"), cont.get("t_side"), cont.get("t_deck"), cont.get("t_btm"))
    deck_stiffeners = deck.deck(cont.get("b_sup"))
    form_values.stiffeners = []
    form_values.stiffeners += deck_stiffeners
    end_cs = merge.merge(first_cs, form_values.stiffeners)
    image = cs_to_html.print_cs(end_cs)
    return render_template('geometry_input.html', image = image, content = cont)


@app.route('/cs_analysis_step_1', methods = ['POST'])
def cs_analysis_input_1():
    defaults.do_deck_as_prop=False
    cont = None
    try:
        b_sup = int(request.form['b_sup'])
        b_inf = int(request.form['b_inf'])
        h = int(request.form['h'])
        t_side = int(request.form['t_side'])
        t_btm = int(request.form['t_btm'])
        num_side = int(request.form['num_side'])
        num_btm = int(request.form['num_btm'])
        form_values.content = copy.deepcopy(form_values.default_cs)
        cont = form_values.content
        cont.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "t_side":t_side, "t_btm":t_btm, "num_side":num_side, "num_btm":num_btm})

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
    first_cs = initial_cs.create_initial_cs(cont.get("b_sup"), cont.get("b_inf"), cont.get("h"), cont.get("t_side"), cont.get("t_deck"), cont.get("t_btm"))
    deck_stiffeners = deck.deck(cont.get("b_sup"))
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

@app.route('/cs_analysis_step_2', methods = ['POST'])
def cs_analysis_input_2():
    defaults.do_deck_as_prop=False
    b_sup = int(request.form['b_sup'])
    b_inf = int(request.form['b_inf'])
    h = int(request.form['h'])
    t_side = int(request.form['t_side'])
    t_btm = int(request.form['t_btm'])
    num_side = int(request.form['num_side'])
    num_btm = int(request.form['num_btm'])
    form_values.content = copy.deepcopy(form_values.default_cs)
    cont = form_values.content
    cont.update({"b_sup":b_sup, "b_inf":b_inf, "h":h, "t_side":t_side, "t_btm":t_btm, "num_side":num_side, "num_btm":num_btm})

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
    deck_stiffeners = deck.deck(cont.get("b_sup"))
    num_top = len(deck_stiffeners)
    cont.update({"num_top":num_top})
    stiffener_transform.input_to_prop(cont.get("num_top"), cont.get("num_side"), cont.get("num_btm"))
    data.input_data.update({"b_sup":cont.get("b_sup"), "b_inf":cont.get("b_inf"), "h":cont.get("h"), \
    "t_deck":cont.get("t_deck"), "t_side":cont.get("t_side"), "t_bottom":cont.get("t_btm")})
    return render_template('forces_input.html')

@app.route('/results_analysis', methods = ['POST'])
def resultpage_analysis():
    defaults.do_deck_as_prop=False
    M_Ed = int(request.form['M_Ed'])*10**6
    V_Ed = int(request.form['V_Ed'])*10**3
    T_Ed = int(request.form['T_Ed'])*10**6
    data.input_data.update({"M_Ed":M_Ed, "V_Ed":V_Ed, "T_Ed":T_Ed})
    f_y = int(request.form['fy'])
    data.constants.update({"f_y":f_y})
    results = cs_analysis_tool.cs_analysis_gui()
    return render_template('resultpage_analysis.html', results = results)


if __name__ == '__main__':
   app.run(debug = True)
