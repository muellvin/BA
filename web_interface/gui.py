import flask
import math
from flask import Flask, render_template, request, jsonify
import os
import sys
import copy

sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
from web_interface import cs_to_html
from web_interface import form_values
from web_interface import stiffener_transform
import initial_cs
import deck
import data
from classes import merge

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cs_analysis_step_1', methods = ['GET'])
def cs_analysis():
    form_values.content = copy.deepcopy(form_values.default_cs)
    cont = form_values.content
    initial_cs = cs_to_html.create_initial_cs(cont.get("b_sup"), cont.get("b_inf"), cont.get("h"), cont.get("t_side"), cont.get("t_deck"), cont.get("t_btm"))
    image = cs_to_html.print_cs(initial_cs)
    return render_template('geometry_input.html', image = image, content = cont)

@app.route('/optimize', methods = ['GET'])
def optimize():
    return render_template('optimize_input.html', a="Optimize")

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
    image = cs_to_html.print_cs(first_cs)
    return render_template('geometry_input.html', content = cont, image = image)

@app.route('/cs_analysis_step_2', methods = ['POST'])
def cs_analysis_input_2():
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

@app.route('/results', methods = ['POST'])
def reultpage():
    M_Ed = int(request.form['M_Ed'])
    V_Ed = int(request.form['V_Ed'])
    T_Ed = int(request.form['T_Ed'])
    data.input_data.update({"M_Ed":M_Ed, "V_Ed":V_Ed, "T_Ed":T_Ed})
    f_y = int(request.form['fy'])
    data.constants.update({"f_y":f_y})
    
    return render_template('resultpage.html')

if __name__ == '__main__':
   app.run(debug = True)
