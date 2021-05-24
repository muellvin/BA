from data_and_defaults import defaults

#t_deck is set in defaults
#defaults cs values for gui 
default_cs = {"b_sup": 4000, "b_inf":3000, "h":2000, "t_side":10, "t_btm":10, "t_deck":defaults.t_deck, "num_side":0, "num_btm":0, "a":4000, "L_e":10000}


# intermediate container for analysis input
content = {}

#stiffeners intermediate container
stiffeners = []


#intermediate container for optimizer input
values = {}
