# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 15:43:44 2021

@author: anassyed
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
import brightway2 as bw

st.title("ASSURED project")
#st.sidebar.title("Common parameters of Buses")

# ( battery, electricity, diesel_price=0)


# st.sidebar.subheader("Common prices")
# battery_price = st.sidebar.number_input("Battery Price kWh/km",  min_value = 30, max_value = 500, value = 350, step = 5)
# #electricity_price = float(st.sidebar.text_input("Electricity Price euro/kWh", 0.13))
# electricity_price = st.sidebar.number_input('Electricity Price euro/kWh', min_value = 0.05, max_value = 2.0, value = 0.13, step = 0.01)
# #diesel_price = float(st.sidebar.text_input("Diesel Price euro/L", 1.49))
# diesel_price =st.sidebar.number_input("Diesel Price euro/L", value =1.57, min_value = 0.01, max_value = 3.0, step= 0.01)
# t.price = t.Price(battery_price, electricity_price, diesel_price)


# st.sidebar.subheader("Discount Rate")
# #dr = float(st.sidebar.text_input("Discount rate", -0.0183))

# dr2 = st.sidebar.slider('Discount rate in % ', min_value=-3.0, max_value= 2.0, step= 0.003, value = -0.32)

# st.sidebar.write(dr2/100)


#st.sidebar.write(t.npv.discount_rate)

# st.sidebar.subheader("Route Details")
#( route_length, return_trip_perday, drive_time_route, active_days_year)
#route = t.Route(17, 5, 50, 365)

st.subheader("Bus Line Information")


with st.form(key = 'Bus Info') : 
    
    st.subheader('Number of buses')
    cols = st.beta_columns(3)
    
    n18m_bus = int(cols[0].text_input("Number of 18m bus", 8 ))
    n12m_bus = int(cols[1].text_input("Number of 12m bus", 8))
    lifetime = int(cols[2].text_input("Bus lifetime (year)", 15 ))
    
    st.subheader('Charging infrastructures')
    charger = st.beta_columns(2)
    
    fc = int(charger[0].text_input("Number of Fast Charger", 1 ))
    
    oc = int(charger[1].text_input("Number of Overnight chargers", 2 ))
    
    charger_power = st.beta_columns(2)
    
    fc_power = int(charger_power[0].text_input("Power of a Fast Charger (kW)", 600 ))
    
    oc_power = int(charger_power[1].text_input("Power of a Overnight charger (kW)", 100 ))
    
    st.subheader('Energy consumption per day on each season')
    st.write('Energy consumption in a day in the month of March')
    march = st.beta_columns(2)
    
    march18 = int(march[0].text_input("Energy demand per day of a 18m bus - March (kWh)", 455 ))
    march12 = int(march[1].text_input(" Energy demand per day of a 12m bus - March (kWh)", 270 ))
  
    
    st.write('Energy consumption in a day in the month of June')
    june = st.beta_columns(2)
    
    june18 = int(june[0].text_input("Energy demand per day of a 18m bus - Jun (kWh)e", 570 ))
    june12 = int(june[1].text_input("Energy demand per day of a 12m bus - June (kWh)", 313 ))
    
    st.write('Energy consumption in a day in the month of September')
    sept = st.beta_columns(2)
    
    sept18 = int(sept[0].text_input("Energy demand per day of a 18m bus - September (kWh)", 558 ))
    sept12 = int(sept[1].text_input("Energy demand per day of a 12m bus - September (kWh)", 306 ))
    
    st.write('Energy consumption in a day in the month of December')
    dec = st.beta_columns(2)
    
    dec18 = int(dec[0].text_input("Energy demand per day of a 18m bus - December (kWh)", 450 ))
    dec12 = int(dec[1].text_input("Energy demand per day of a 12m bus - December (kWh)", 273 ))  
    
    st.subheader('Route Details')
    route = st.beta_columns(4)
    
    return_trip_distance = float(route[0].text_input("Return Trip Distance (km)", 19.4 ))
    number_of_return_trip_per_day = int(route[1].text_input("Number of return trip per day", 8))
    average_passengers_12m = int(route[2].text_input("Average Passenger per trip in 12m bus", 10 ))
    average_passengers_18m = int(route[3].text_input("Average Passenger per trip in 18m bus", 20 ))
    
    submitted = st.form_submit_button('Calculate')
    

yearly_consumption_18m =( march18 + june18 + sept18 + dec18) *3*30
yearly_consumption_12m =( march12 + june12 + sept12 + dec12) *3*30

st.write(yearly_consumption_18m)
st.write(yearly_consumption_12m)
    
#lifetimekm = 

# brightway2 

bw.projects.set_current('ASSURED')

busdb = bw.Database('assured bus')

# select the 18m bus 

bus18mproduction = [x for x in busdb if 'Passenger bus, electric - opportunity charging, 18m ASSURED' in x['name']][0]

usephase18m = [x for x in busdb if 'use phase opportunity charging, 18m ASSURED' in x['name']][0]

# electricity in the use phase 
electricity = [x for x in usephase18m.technosphere() if 'electricity supply for electric vehicles, 2030' in x['name']][0]
personkm18m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
electricity['amount'] = yearly_consumption_18m*lifetime / personkm18m
electricity.save()

# 12m bus 
bus12mproduction = [x for x in busdb if 'Passenger bus, electric - opportunity charging, 13m ASSURED' in x['name']][0]

usephase12m = [x for x in busdb if 'use phase - opportunity charging, 13m ASSURED' in x['name']][0]

# electricity in the use phase 
electricity12 = [x for x in usephase12m.technosphere() if 'electricity supply for electric vehicles, 2030' in x['name']][0]
personkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
electricity12['amount'] = yearly_consumption_12m*lifetime / personkm12m
electricity12.save()




#calculate lca

def do_lca(fu, method = ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100')): 
    
    lca = bw.LCA({fu:1}, method)
    lca.lci()
    lca.lcia()
    
    return lca.score

st.write('18m bus')
st.write((do_lca(bus18mproduction)/personkm18m)*1000)
st.write(do_lca(usephase18m)*1000)

st.write('12m bus')
st.write((do_lca(bus12mproduction)/personkm12m)*1000)
st.write(do_lca(usephase12m)*1000)