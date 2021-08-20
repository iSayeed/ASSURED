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





data = {'Barcelona H16': [8,5,15,1,2,600,100,455,270,570,313,588,306, 450,273,23.8,6,10,20], 
        'Barcelona L33': [8,8,15,1,2,600,100,392,245,468,278,463,274, 395,247,19.4,8,10,20],
        'Gothenburg R55': [0,8,15,2,1,290,150,0,421,0,388,0,388, 0,455,15.2,13,10,20],
        'Onsaburk L33': [2,2,15,1,1,600,100,625,436,625,438,614,437, 657,444,12.2,13,10,20]}
busline = st.radio('Select bus line', ['Barcelona H16', 'Barcelona L33', 'Gothenburg R55', 'Onsaburk L33'])
st.write(busline)
# button = st.button('Calculate')

# if button: 
with st.form(key = 'Bus Info') : 
    
    st.subheader('Number of buses')
    cols = st.beta_columns(3)
    
    n18m_bus = int(cols[0].text_input("Number of 18m bus", data[busline][0] ))
    n12m_bus = int(cols[1].text_input("Number of 12m bus", data[busline][1] ))
    lifetime = int(cols[2].text_input("Bus lifetime (year)", data[busline][2]  ))
        
    st.subheader('Charging infrastructures')
    charger = st.beta_columns(2)
    
    fc = int(charger[0].text_input("Number of Fast Charger", data[busline][3]  ))

    oc = int(charger[1].text_input("Number of Overnight chargers", data[busline][4]  ))
    
    charger_power = st.beta_columns(2)
    
    fc_power = int(charger_power[0].text_input("Power of a Fast Charger (kW)", data[busline][5]  ))

    oc_power = int(charger_power[1].text_input("Power of a Overnight charger (kW)", data[busline][6]  ))
    
    st.subheader('Energy consumption per day on each season')
    st.write('Energy consumption in a day in the month of March')
    march = st.beta_columns(2)
    
    march18 = int(march[0].text_input("Energy demand per day of a 18m bus - March (kWh)", data[busline][7]  ))
    march12 = int(march[1].text_input(" Energy demand per day of a 12m bus - March (kWh)", data[busline][8]  ))
  
    
    st.write('Energy consumption in a day in the month of June')
    june = st.beta_columns(2)
    
    june18 = int(june[0].text_input("Energy demand per day of a 18m bus - Jun (kWh)e", data[busline][9]  ))
    june12 = int(june[1].text_input("Energy demand per day of a 12m bus - June (kWh)", data[busline][10]  ))
    
    st.write('Energy consumption in a day in the month of September')
    sept = st.beta_columns(2)
    
    sept18 = int(sept[0].text_input("Energy demand per day of a 18m bus - September (kWh)", data[busline][11]  ))
    sept12 = int(sept[1].text_input("Energy demand per day of a 12m bus - September (kWh)", data[busline][12]  ))
    
    st.write('Energy consumption in a day in the month of December')
    dec = st.beta_columns(2)
    
    dec18 = int(dec[0].text_input("Energy demand per day of a 18m bus - December (kWh)", data[busline][13]  ))
    dec12 = int(dec[1].text_input("Energy demand per day of a 12m bus - December (kWh)", data[busline][14]  ))
    
    st.subheader('Route Details')
    route = st.beta_columns(4)
    
    return_trip_distance = float(route[0].text_input("Return Trip Distance (km)", data[busline][15]  ))
    number_of_return_trip_per_day = int(route[1].text_input("Number of return trip per day", data[busline][16] ))
    average_passengers_12m = int(route[2].text_input("Average Passenger per trip in 12m bus", data[busline][17]  ))
    average_passengers_18m = int(route[3].text_input("Average Passenger per trip in 18m bus", data[busline][18]  ))
    
    submitted = st.form_submit_button('Calculate')

lca = st.button('Calcualte LCA')        
if lca:         
    
    yearly_consumption_18m =( march18 + june18 + sept18 + dec18) *3*30
    yearly_consumption_12m =( march12 + june12 + sept12 + dec12) *3*30
    
    st.write(yearly_consumption_18m)
    st.write(yearly_consumption_12m)
        
    annual_distance = return_trip_distance * number_of_return_trip_per_day * 365
    
    # brightway2  
    
    bw.projects.set_current('ASSURED')
    
    busdb = bw.Database('assured bus')
    
    # select the 18m bus 
    
    
    
    def set_charger_share_usephase(usephase,pmkm, on): 
        chargers = [x for x in usephase.technosphere() if 'charger' in x['name']]
        
        #set all values to zero 
        for exc in chargers: 
            exc['amount'] = 0 
            exc.save()
            
        
            #fastcharger share 
        if on ==1:
            
            fc_act = [x for x in chargers if 'pantograph' in x['name'] and str(fc_power) in x['name']][0]
            fc_act['amount'] = (fc/(n18m_bus+n12m_bus))/pmkm
            fc_act.save()
            
            #oc charger share 
            
            oc_act = [x for x in chargers if 'pantograph' not in x['name'] and str(oc_power) in x['name']][0]
            oc_act['amount'] = (oc/(n18m_bus+n12m_bus))/pmkm
            oc_act.save()
    
    def set_electric_demand(usephase, avg_passenger, yearly_consumption): 
        electricity = [x for x in usephase.technosphere() if 'electricity supply for electric vehicles, 2030' in x['name']][0]
        personkm = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * avg_passenger
        electricity['amount'] = yearly_consumption*lifetime / personkm
        electricity.save()
    
    def setup_diesel_bus_usephase(fuel_rate, annual_distance, lifetime, bussize):
        lifetime_diesel_liter = (fuel_rate/100) * annual_distance * lifetime
                                    
        lifetime_co2 = lifetime_diesel_liter * 2.68  # 1 liter of diesel produces 2.68 kg CO2
        
        lifetime_diesel_kg = lifetime_diesel_liter*0.832  # 1 liter of diesel 0.832 kg of diesel 
        
        if bussize == 18: 
            avgpassenger = average_passengers_18m
        else: 
            avgpassenger = average_passengers_12m 
        
        personkm = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * avgpassenger
        
        
        # set the diesel kg in the use phase activity 
        usephasebus = [x for x in busdb if 'use phase passenger-bus, diesel, ' +str(bussize)+'m ASSURED' in x['name']][0] 
        
        market_diesel = [x for x in usephasebus.technosphere() if 'market for diesel' in x['name']][0]
        market_diesel['amount'] = lifetime_diesel_kg/personkm
        market_diesel.save()
        
        #set the co2 emission in the biosphere
        
        co2 = [x for x in usephasebus.biosphere()][0]
        co2['amount'] = lifetime_co2/personkm
        co2.save()
    
    #18m bus
    if n18m_bus != 0: 
        bus18mproduction = [x for x in busdb if 'Passenger bus, electric - opportunity charging, 18m ASSURED' in x['name']][0]
        usephase18m = [x for x in busdb if 'use phase opportunity charging, 18m ASSURED - single bus' in x['name']][0]
        
        bus18mdieselproduction = [x for x in busdb if 'Passenger bus, diesel, 18m ASSURED' in x['name']][0]
        use18mdiesel = [x for x in busdb if 'use phase passenger-bus, diesel, 18m ASSURED' in x['name']][0] 
        
        personkm18m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
        set_charger_share_usephase(usephase18m,personkm18m, 1)
        set_electric_demand(usephase18m, average_passengers_18m, yearly_consumption_18m)
    
    
    # 12m bus 
    bus12mproduction = [x for x in busdb if 'Passenger bus, electric - opportunity charging, 13m ASSURED' in x['name']][0]
    
    usephase12m = [x for x in busdb if 'use phase - opportunity charging, 13m ASSURED - single bus' in x['name']][0]
    
    bus12mdieselproduction = [x for x in busdb if 'Passenger bus, diesel, 13m ASSURED' in x['name']][0]
    use12mdiesel = [x for x in busdb if 'use phase passenger-bus, diesel, 13m ASSURED' in x['name']][0] 
    
    personkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
    set_charger_share_usephase(usephase12m,personkm12m, 1)
    set_electric_demand(usephase12m, average_passengers_12m, yearly_consumption_12m)
    
    
    
    
    #calculate lca
    
    def do_lca(fu, method = ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100')): 
        
        lca = bw.LCA({fu:1}, method)
        lca.lci()
        lca.lcia()
    
        return lca.score
    
    # list of fast chargers 
    
    fast_charger_activity = [x for x in busdb if 'charger' in x['name'] and 'Transformer' in x['name']]
    overnight_charger_activity = [x for x in busdb if 'charger' in x['name'] and 'Transformer' not in x['name'] and '600' not in x['name']]
    
    # st.write('18m bus')
    # st.write((do_lca(bus18mproduction)/personkm18m)*1000)
    # st.write(do_lca(usephase18m)*1000)
    
    # st.write('18m diesel')
    # setup_diesel_bus_usephase(70,annual_distance, 12, 18 )
    
    # st.write((do_lca(bus18mdieselproduction)/personkmdiesel18)*1000)
    # st.write(do_lca(use18mdiesel)*1000)
    # # for diesel 
    
    
    # st.write('12m bus')
    # st.write((do_lca(bus12mproduction)/personkm12m)*1000)
    # st.write(do_lca(usephase12m)*1000)
    
    # st.write('12m bus diesel')
    # setup_diesel_bus_usephase(40,annual_distance, 12, 13)
    
    # st.write((do_lca(bus12mdieselproduction)/personkmdiesel12)*1000)
    # st.write(do_lca(use12mdiesel)*1000)
    
    #for dieel 
    
    
    # '''
    # ['use phase passenger bus, diesel, 13m ASSURED' (passenger-kilometer, RER, None),
    #  'use phase, passenger bus, diesel, 18m ASSURED' (passenger-kilometer, RER, None)]
    # '''
    
    
    #Fleet lca 
    if n18m_bus != 0: 
        personkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
        diesel18production =(do_lca(bus18mdieselproduction)/personkmdiesel18)*1000
        assured18production =(do_lca(bus18mproduction)/personkm18m)*1000
    
    personkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
    diesel12production =(do_lca(bus12mdieselproduction)/personkmdiesel12)*1000
    assured12production=(do_lca(bus12mproduction)/personkm12m)*1000
    
    
    if n18m_bus != 0: 
        diesel18use = do_lca(use18mdiesel)*1000
        assured18use =do_lca(usephase18m)*1000
    
    assured12use =do_lca(usephase12m)*1000
    diesel12use =do_lca(use12mdiesel)*1000
    
    if n18m_bus != 0: 
        total_imact_bus = n18m_bus*(do_lca(bus18mproduction)/personkm18m)*1000 + n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
    else: 
        total_imact_bus = n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
    
    fu_fc = [x for x in fast_charger_activity if str(fc_power) in x['name']][0]
    fu_oc = [x for x in overnight_charger_activity if str(oc_power) in x['name']][0]
    
    if n18m_bus != 0: 
        fc_charger_impact = (fc*do_lca(fu_fc)/personkm18m)*1000 + (oc*do_lca(fu_oc)/personkm18m)*1000
    else: 
        fc_charger_impact = (fc*do_lca(fu_fc)/personkm12m)*1000 + (oc*do_lca(fu_oc)/personkm12m)*1000
    
    # st.write('total bus impact')
    # st.write(total_imact_bus)
    # st.write('total charger impact')
    # st.write(fc_charger_impact)
    # st.write('total use phase impact')
    # total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
    # st.write(total_use_impact_assured)
    
    # st.write('now for diesel')
    # st.write('total diesel bus impact')
    # total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
    # st.write(total_diesel_bus_impact)
    
    # st.write('total use phase impact')
    # total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
    # st.write(total_use_impact_diesel)
    
    # st.write(do_lca(fu_fc))
    # st.write(do_lca(fu_oc))
    # st.write(do_lca(bus18mproduction))
    
    def update_names_in_exchanges(activity): 
        for x in activity.technosphere(): 
            x['name'] = bw.get_activity(x['input'])['name']
            x.save()
            
    
    # plotting ref: https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html
    
    if n18m_bus != 0: 
        diesel18production =(do_lca(bus18mdieselproduction)/personkmdiesel18)*1000
        diesel18use = do_lca(use18mdiesel)*1000
        assured18production =(do_lca(bus18mproduction)/personkm18m)*1000
        assured18use =do_lca(usephase18m)*1000
    
    diesel12production =(do_lca(bus12mdieselproduction)/personkmdiesel12)*1000
    diesel12use =do_lca(use12mdiesel)*1000
    assured12production=(do_lca(bus12mproduction)/personkm12m)*1000
    assured12use =do_lca(usephase12m)*1000
    
    if n18m_bus != 0: 
        labels = ['Diesel Bus 12m', 'Diesel Bus 18m', 'ASSURED Bus 12m', 'ASSURED Bus 18m']
        production_phase = [diesel12production,diesel18production,assured12production,assured18production ]
        use_phase = [diesel12use,diesel18use,assured12use,assured18use]
        width = 0.35       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        sns.set_style("whitegrid")
        ax.bar(labels, production_phase, width, label='Production + EoL')
        ax.bar(labels, use_phase, width, bottom=production_phase,
               label='Use phase')
        
        ax.set_ylabel('g CO2-eq /pkm')
        ax.legend()
        
        st.pyplot(fig)
    else: 
        labels = ['Diesel Bus 12m',  'ASSURED Bus 12m']
        production_phase = [diesel12production,assured12production]
        use_phase = [diesel12use,assured12use]
        width = 0.35       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        sns.set_style("whitegrid")
        ax.bar(labels, production_phase, width, label='Production + EoL')
        ax.bar(labels, use_phase, width, bottom=production_phase,
               label='Use phase')
        
        ax.set_ylabel('g CO2-eq /pkm')
        ax.legend()
        
        st.pyplot(fig)
    
    #make dataframe 
    
    bus_dict = { 'Buses': labels, 'Production + EoL': production_phase, 'Use Phase': use_phase }
    df = pd.DataFrame(bus_dict)
    df.set_index('Buses')
    
    
    st.write(df)
    #plotting of total fleet
    # before that, let's make the charger share to zero 
    if n18m_bus != 0: 
        set_charger_share_usephase(usephase18m,personkm18m, 0)
        
    set_charger_share_usephase(usephase12m,personkm12m, 0)
    
    
    if n18m_bus != 0:
        pkmavg = np.mean([personkm18m, personkm12m])
        total_imact_bus = n18m_bus*(do_lca(bus18mproduction)/personkm18m)*1000 + n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
        total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
        charger_impact = (fc*do_lca(fu_fc)/pkmavg)*1000 + (oc*do_lca(fu_oc)/pkmavg)*1000
            
        
        total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
        total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
        
        labels = ['Diesel Technology', 'ASSURED Technology']
        production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
        charger =np.array([0, charger_impact])
        use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
        width = 0.35       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        sns.set_style("whitegrid")
        ax.bar(labels, production_phase, width, label='Production + EoL', color='#ff3333')
        ax.bar(labels, charger, width, bottom =production_phase, label='Charger', color='#33ff33')
        ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
               label='Use phase', color='#3333ff')
        
        ax.set_ylabel('g CO2-eq /pkm')
        ax.legend()
        
        st.pyplot(fig)  
    
    else: 
        total_imact_bus =  n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
        total_use_impact_assured =  assured12use* n12m_bus
        charger_impact = (fc*do_lca(fu_fc)/personkm12m)*1000 + (oc*do_lca(fu_oc)/personkm12m)*1000
            
        
        total_diesel_bus_impact = diesel12production*n12m_bus 
        total_use_impact_diesel = diesel12use* n12m_bus
        
        labels = ['Diesel Technology', 'ASSURED Technology']
        production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
        charger =np.array([0, charger_impact])
        use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
        width = 0.35       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        sns.set_style("whitegrid")
        ax.bar(labels, production_phase, width, label='Production + EoL', color='#ff3333')
        ax.bar(labels, charger, width, bottom =production_phase, label='Charger', color='#33ff33')
        ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
               label='Use phase', color='#3333ff')
        
        ax.set_ylabel('g CO2-eq /pkm')
        ax.legend()
        
        st.pyplot(fig) 
    
    fleet_dict = {'Fleets': labels, 'Production + Eol': production_phase, 'Chargers': charger, 'Use Phase': use_phase}
    df2 = pd.DataFrame(fleet_dict)
    df2.set_index('Fleets')
    
    st.write(df2)