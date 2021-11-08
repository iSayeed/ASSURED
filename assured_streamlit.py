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


st.image('./ASSURED.jpg')


st.subheader("Bus Line information ")





data = {'Barcelona H16': [8,5,15,1,2,600,100,455,270,570,313,588,306, 450,273,23.8,6,10,20,75], 
        'Barcelona L33': [8,8,15,1,2,600,100,392,245,468,278,463,274, 395,247,19.4,8,10,20,75],
        'Gothenburg R55': [0,8,15,2,1,290,150,0,421,0,388,0,388, 0,455,15.2,13,10,20,75],
        'Osnabrück L33': [2,2,15,1,1,600,100,625,436,625,438,614,437, 657,444,12.2,13,10,20,75]}
st.sidebar.subheader("Bus Route")
busline = st.sidebar.radio('', ['Barcelona H16', 'Barcelona L33', 'Gothenburg R55', 'Osnabrück L33'])

country = {'Barcelona H16': 'ES', 
        'Barcelona L33': 'ES',
        'Gothenburg R55': 'SE',
        'Osnabrück L33': 'DE'}
# st.sidebar.write(busline)
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
    
    june18 = int(june[0].text_input("Energy demand per day of a 18m bus - June (kWh)", data[busline][9]  ))
    june12 = int(june[1].text_input("Energy demand per day of a 12m bus - June (kWh)", data[busline][10]  ))
    
    st.write('Energy consumption in a day in the month of September')
    sept = st.beta_columns(2)
    
    sept18 = int(sept[0].text_input("Energy demand per day of a 18m bus - September (kWh)", data[busline][11]  ))
    sept12 = int(sept[1].text_input("Energy demand per day of a 12m bus - September (kWh)", data[busline][12]  ))
    
    st.write('Energy consumption in a day in the month of December')
    dec = st.beta_columns(2)
    
    dec18 = int(dec[0].text_input("Energy demand per day of a 18m bus - December (kWh)", data[busline][13]  ))
    dec12 = int(dec[1].text_input("Energy demand per day of a 12m bus - December (kWh)", data[busline][14]  ))
    
    st.subheader('Diesel bus fuel consumption')
    fuel_rate = st.beta_columns(2)
    
    diesel12fuel_consumption = float(fuel_rate[0].text_input('Fuel consumption rate of 12m bus (L/100 km)', 40))
    diesel18fuel_consumption = float(fuel_rate[1].text_input('Fuel consumption rate of 18m bus (L/100 km)', 70))
    
    st.subheader('Route Details')
    route = st.beta_columns(5)
    
    return_trip_distance = float(route[0].text_input("Return Trip Distance (km)", data[busline][15]  ))
    number_of_return_trip_per_day = int(route[1].text_input("Number of return trip per day", data[busline][16] ))
    average_passengers_12m = int(route[2].text_input("Average Passenger per trip in 12m bus", data[busline][17]  ))
    average_passengers_18m = int(route[3].text_input("Average Passenger per trip in 18m bus", data[busline][18]  ))
    passenger_weight = int(route[4].text_input("Average Passenger Mass (kg)", data[busline][19]))
    
    submitted = st.form_submit_button('Update')

st.sidebar.subheader(busline + ' bus line')
st.sidebar.write("Number of buses:")
if n18m_bus !=0: 
    st.sidebar.image(('./18m bus.png'), caption = str(n18m_bus) + ' units of' +' 18m Buses', width =300)
if n12m_bus !=0:
    st.sidebar.image(('./12m bus.png'), caption = str(n12m_bus) + ' units of' +' 12m Buses', width =250)

st.sidebar.write("Route distance")
st.sidebar.image(('./route.png'), width = 100)
# st.sidebar.image(('./depot charger.png'), width = 100)
st.sidebar.write('Single route -- ' + str(return_trip_distance/2) + ' km')
st.sidebar.write('Return trip per day -- ' + str(number_of_return_trip_per_day) + ' times')
st.sidebar.write('Daily travel by a single bus -- ' + str(return_trip_distance*number_of_return_trip_per_day) + ' km')
 #calculate lca
    
def do_lca(fu, method = ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100')): 
    
    lca = bw.LCA({fu:1}, method)
    lca.lci()
    lca.lcia()
    do_lca.counter += 1

    return lca.score
do_lca.counter = 0 

#variables 

drivingmass18 = average_passengers_18m * passenger_weight
drivingmass12 = average_passengers_12m * passenger_weight

lca = st.button('Calculate LCA')        
if lca:         
    
    yearly_consumption_18m =( march18 + june18 + sept18 + dec18) *3*30
    yearly_consumption_12m =( march12 + june12 + sept12 + dec12) *3*30
    
    # st.write(yearly_consumption_18m)
    # st.write(yearly_consumption_12m)
        
    annual_distance = return_trip_distance * number_of_return_trip_per_day * 365
    
    # brightway2  
    
    bw.projects.set_current('ASSURED 5')
    
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
        # electricity = [x for x in usephase.technosphere() if 'electricity supply for electric vehicles, 2030' in x['name']][0]
        medium_voltage = [x for x in usephase.technosphere() if 'medium voltage' in x['name']]
        #set all medium voltage to zero before seeting for a country 
        for exc in medium_voltage: 
            exc['amount'] = 0
            exc.save()
        #set the country now 
        electricity = [x for x in usephase.technosphere() if 'medium voltage' in x['name'] and bw.get_activity(x['input'])['location'] == country[busline]][0]
        # print(electricity)
        personkm = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * avg_passenger
        electricity['amount'] = yearly_consumption*lifetime / personkm
        electricity.save()
        
        # set the maintenance 
        maintenance = [x for x in usephase.technosphere() if 'maintenance, bus' in x['name']][0]
        maintenance['amount'] = 1/personkm
        maintenance.save()
        
        # set also the road share 
        drivingmass = avg_passenger * passenger_weight 
        
        road = [x for x in usephase.technosphere() if 'market for road' == x['name']][0]
        road['amount'] = drivingmass * 0.00000053
        road.save()
        
        
    
    def setup_diesel_bus_usephase(fuel_rate, annual_distance, lifetime, bussize):
        lifetime_diesel_liter = (fuel_rate/100) * annual_distance * lifetime
                                    
        lifetime_co2 = lifetime_diesel_liter * 2.68  # 1 liter of diesel produces 2.68 kg CO2
        
        lifetime_diesel_kg = lifetime_diesel_liter*0.832  # 1 liter of diesel 0.832 kg of diesel 
        
        #cadmium 
        cd = (0.01/1000000)*lifetime_diesel_kg
        #copper
        cu = (1.7/1000000)*lifetime_diesel_kg
        #Chromium 
        cr = (0.05/1000000)*lifetime_diesel_kg
        #Nickel 
        ni = (0.07/1000000)*lifetime_diesel_kg
        #selenium 
        se = (0.01/1000000)*lifetime_diesel_kg
        #zinc 
        zn = (1/1000000)*lifetime_diesel_kg
        #lead 
        pb = (0.00000011/1000000)*lifetime_diesel_kg
        #mercury
        hg = (0.00002/1000000)*lifetime_diesel_kg
        #chromium IV
        crvi = (0.001/1000000)*lifetime_diesel_kg
        
        #sulfur 
        so2 = (0.035/349.8)*lifetime_diesel_kg
       
        metal = {'Cadmium':cd, 'Copper':cu, 'Chromium':cr, 'Nickel':ni, 
                 'Selenium':se, 'Zinc':zn, 'Lead':pb, 'Mercury':hg, 
                 'Chromium VI':crvi, 'Sulfur dioxide':so2}
        
        
        if bussize == 18: 
            avgpassenger = average_passengers_18m
            drivingmass = drivingmass18
        else: 
            avgpassenger = average_passengers_12m 
            drivingmass = drivingmass12
        
        personkm = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * avgpassenger
        
        
        # set the diesel kg in the use phase activity 
        usephasebus = [x for x in busdb if 'use phase passenger-bus, diesel, ' +str(bussize)+'m ASSURED' in x['name']][0] 
        
        market_diesel = [x for x in usephasebus.technosphere() if 'market for diesel' in x['name']][0]
        market_diesel['amount'] = lifetime_diesel_kg/personkm
        market_diesel.save()
        
        #set the co2 emission in the biosphere
        #first set all the biosphere to zero 
        # all_bio = [x for x in usephasebus.biosphere()]
        
        # for x in all_bio: 
        #     x['amount']= 0
        #     x.save()
        
        
        co2 = [x for x in usephasebus.biosphere() if 'Carbon dioxide, fossil' in x['name']][0]
        co2['amount'] = lifetime_co2/personkm
        co2.save()
        
        # set the maintenance 
        maintenance = [x for x in usephasebus.technosphere() if 'maintenance, bus' in x['name']][0]
        maintenance['amount'] = 1/personkm
        maintenance.save()
        
        #heavy metal emission setup
        def heavy_metal(name, amount): 
            emission = [x for x in usephasebus.biosphere() if name == x['name'] and 'air' in bw.get_activity(x['input'])['categories'] ][0]
            emission['amount'] = amount /personkm
            emission.save()
        
        for name, amount in metal.items(): 
            heavy_metal(name, amount)
        
        # other emissions 
        # road share 
        road = [x for x in usephasebus.technosphere() if 'market for road' == x['name']][0]
        road['amount'] = drivingmass * 0.00000053
        road.save()
        
        
            
        
    
    #18m bus
    if n18m_bus != 0: 
        bus18mproduction = [x for x in busdb if 'Passenger bus, electric - opportunity charging, 18m ASSURED' in x['name']][0]
        usephase18m = [x for x in busdb if 'use phase opportunity charging, 18m ASSURED - single bus' in x['name'] 
                                                                                           and 'Backup' not in x['name'] 
                                                                                           and 'busEnergyMix' not in x['name']][0]
        
        bus18mdieselproduction = [x for x in busdb if 'Passenger bus, diesel, 18m ASSURED' in x['name']][0]
        use18mdiesel = [x for x in busdb if 'use phase passenger-bus, diesel, 18m ASSURED' in x['name']][0] 
        
        personkm18m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
        set_charger_share_usephase(usephase18m,personkm18m, 1)
        set_electric_demand(usephase18m, average_passengers_18m, yearly_consumption_18m)
    
    
    # 12m bus 
    bus12mproduction = [x for x in busdb if 'Passenger bus, electric - opportunity charging, 13m ASSURED' in x['name']][0]
    
    usephase12m = [x for x in busdb if 'use phase opportunity charging, 13m ASSURED - single bus' in x['name'] 
                                                                                           and 'Backup' not in x['name']
                                                                                            and 'busEnergyMix' not in x['name']][0]
    
    bus12mdieselproduction = [x for x in busdb if 'Passenger bus, diesel, 13m ASSURED' in x['name']][0]
    use12mdiesel = [x for x in busdb if 'use phase passenger-bus, diesel, 13m ASSURED' in x['name']][0] 
    
    personkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
    set_charger_share_usephase(usephase12m,personkm12m, 1)
    set_electric_demand(usephase12m, average_passengers_12m, yearly_consumption_12m)
    
    
    
    
   
    
    # list of fast chargers 
    
    fast_charger_activity = [x for x in busdb if 'charger' in x['name'] and 'transformer' in x['name']]
    overnight_charger_activity = [x for x in busdb if 'charger' in x['name'] and 'transformer' not in x['name'] 
                                                                                        and 'panto' not in x['name']
                                                                                        and '200' not in x['name']]
    

    
    # Set up the diesel bus 
    setup_diesel_bus_usephase(diesel18fuel_consumption,annual_distance, 12, 18 )
    
    setup_diesel_bus_usephase(diesel12fuel_consumption,annual_distance, 12, 13)
    
    
    
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
    
    
    def update_names_in_exchanges(activity): 
        for x in activity.technosphere(): 
            x['name'] = bw.get_activity(x['input'])['name']
            x.save()
            
    
    # plotting ref: https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html
    st.subheader('Single bus comparison')
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
        plt.style.use('seaborn')
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
        plt.style.use('seaborn')
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
    df['Co2 per km '] = df['Production + EoL'] + df['Use Phase']
    
    # update the co2 per km 
    
    # make a column if the bus is 12 or not 
    df['12m?'] = df['Buses'].str.contains('12m')
    #make a column of total sum of co2 
    df['co2'] = df['Production + EoL'] + df['Use Phase']
    
    #now co2 per km column 
    
    new_co2 = []

    for co2, size in zip(df['co2'], df['12m?']): 
        if size == True : 
            new_co2.append(co2*average_passengers_12m)
        else: 
            new_co2.append(co2*average_passengers_18m)
    # st.write([average_passengers_12m, average_passengers_18m])
    # st.write(new_co2)
            
    df['co2 per km'] = new_co2
    
    
    
    
    # st.write(df)
    df.to_csv(busline + ' single bus.csv')
#plotting of total fleet of CO2 
    st.subheader('Fleet comparison')
    # before that, let's make the charger share to zero 
    if n18m_bus != 0: 
        set_charger_share_usephase(usephase18m,personkm18m, 0)
        
    set_charger_share_usephase(usephase12m,personkm12m, 0)
    
    
    if n18m_bus != 0:
        pkmavg = np.mean([personkm18m, personkm12m])
        total_imact_bus = n18m_bus*assured18production + n12m_bus*assured12production
        #total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
        total_use_impact_assured = n18m_bus*assured18use + n12m_bus*assured12use
        charger_impact = (fc*do_lca(fu_fc)/pkmavg)*1000 + (oc*do_lca(fu_oc)/pkmavg)*1000
            
        
        total_diesel_bus_impact = diesel12production*n12m_bus + \
                                  diesel18production*n18m_bus
        
        total_use_impact_diesel = diesel18use*n18m_bus + \
                                  diesel12use*n12m_bus
        #
        # absolute numbers 
        # st.write('diesel technology')
        # st.write([total_diesel_bus_impact, total_use_impact_diesel ])
        
        labels = ['Diesel Technology', 'ASSURED Technology']
        production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
        charger =np.array([0, charger_impact])
        use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
        width = 0.35       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        plt.style.use('seaborn')
        ax.bar(labels, production_phase, width, label='Production + EoL')
        ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
        ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
               label='Use phase')
        
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
        plt.style.use('seaborn')
        ax.bar(labels, production_phase, width, label='Production + EoL')
        ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
        ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
               label='Use phase')
        
        ax.set_ylabel('g CO2-eq /pkm')
        ax.legend()
        
        st.pyplot(fig) 
    
    fleet_dict = {'Fleets': labels, 'Production + Eol': production_phase, 'Chargers': charger, 'Use Phase': use_phase}
    df2 = pd.DataFrame(fleet_dict)
    df2.set_index('Fleets')
# for other nox and pm 
    # nox = ('CML 2001 (obsolete)', 'eutrophication potential', 'average European')
    # pm10 = ('ReCiPe Midpoint (E) V1.13 no LT', 'particulate matter formation', 'PMFP')
    # if n18m_bus != 0: 
    #     diesel18production =(do_lca(bus18mdieselproduction, method = pm10)/personkmdiesel18)
    #     diesel18use = do_lca(use18mdiesel, method = pm10)
    #     assured18production =(do_lca(bus18mproduction, method = pm10)/personkm18m)
    #     assured18use =do_lca(usephase18m, method = pm10)
    
    # diesel12production =(do_lca(bus12mdieselproduction, method = pm10)/personkmdiesel12)
    # diesel12use =do_lca(use12mdiesel, method = pm10)
    # assured12production=(do_lca(bus12mproduction, method = pm10)/personkm12m)
    # assured12use =do_lca(usephase12m, method = pm10)
    
    # if n18m_bus != 0: 
    #     labels = ['Diesel Bus 12m', 'Diesel Bus 18m', 'ASSURED Bus 12m', 'ASSURED Bus 18m']
    #     production_phase = [diesel12production,diesel18production,assured12production,assured18production ]
    #     use_phase = [diesel12use,diesel18use,assured12use,assured18use]
    #     width = 0.35       # the width of the bars: can also be len(x) sequence
        
    #     fig, ax = plt.subplots()
    #     plt.style.use('seaborn')
    #     ax.bar(labels, production_phase, width, label='Production + EoL')
    #     ax.bar(labels, use_phase, width, bottom=production_phase,
    #            label='Use phase')
        
    #     ax.set_ylabel('g PMFP-eq /pkm')
    #     ax.legend()
        
    #     st.pyplot(fig)
    # else: 
    #     labels = ['Diesel Bus 12m',  'ASSURED Bus 12m']
    #     production_phase = [diesel12production,assured12production]
    #     use_phase = [diesel12use,assured12use]
    #     width = 0.35       # the width of the bars: can also be len(x) sequence
        
    #     fig, ax = plt.subplots()
    #     plt.style.use('seaborn')
    #     ax.bar(labels, production_phase, width, label='Production + EoL')
    #     ax.bar(labels, use_phase, width, bottom=production_phase,
    #            label='Use phase')
        
    #     ax.set_ylabel('g PMFP-eq /pkm')
    #     ax.legend()
        
    #     st.pyplot(fig)
    
    # #make dataframe 
    
    # bus_dict = { 'Buses': labels, 'Production + EoL': production_phase, 'Use Phase': use_phase }
    # df = pd.DataFrame(bus_dict)
    # df.set_index('Buses')
    # df['PMFP per km '] = df['Production + EoL'] + df['Use Phase']
    
    # # update the co2 per km 
    
    # # make a column if the bus is 12 or not 
    # df['12m?'] = df['Buses'].str.contains('12m')
    # #make a column of total sum of pm 
    # df['pm'] = df['Production + EoL'] + df['Use Phase']
    
    # #now co2 per km column 
    
    # new_pm = []

    # for pm, size in zip(df['pm'], df['12m?']): 
    #     if size == True : 
    #         new_pm.append(pm*average_passengers_12m)
    #     else: 
    #         new_pm.append(pm*average_passengers_18m)
    # st.write([average_passengers_12m, average_passengers_18m])
    # st.write(new_pm)
            
    # df['pm per km'] = new_pm
    
    
    
    # st.write('Other emissions')
    # st.write(df)
    # df.to_csv(busline + ' single bus other emissions.csv')    
# for other nox and pm function 
    nox = ('CML 2001 (obsolete)', 'eutrophication potential', 'average European')
    pm10 = ('ReCiPe Midpoint (E) V1.13 no LT', 'particulate matter formation', 'PMFP')
    co2 = ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100')
    methods_single = [nox, pm10, co2]
    def perkm_single(method):
        if n18m_bus != 0: 
            diesel18production =(do_lca(bus18mdieselproduction, method = method)/personkmdiesel18)
            diesel18use = do_lca(use18mdiesel, method = method)
            assured18production =(do_lca(bus18mproduction, method = method)/personkm18m)
            assured18use =do_lca(usephase18m, method = method)
        
        diesel12production =(do_lca(bus12mdieselproduction, method = method)/personkmdiesel12)
        diesel12use =do_lca(use12mdiesel, method = method)
        assured12production=(do_lca(bus12mproduction, method = method)/personkm12m)
        assured12use =do_lca(usephase12m, method = method)
        
        if n18m_bus != 0: 
            labels = ['Diesel Bus 12m', 'Diesel Bus 18m', 'ASSURED Bus 12m', 'ASSURED Bus 18m']
            production_phase = [diesel12production,diesel18production,assured12production,assured18production ]
            use_phase = [diesel12use,diesel18use,assured12use,assured18use]
            width = 0.35       # the width of the bars: can also be len(x) sequence
            
            # fig, ax = plt.subplots()
            # plt.style.use('seaborn')
            # ax.bar(labels, production_phase, width, label='Production + EoL')
            # ax.bar(labels, use_phase, width, bottom=production_phase,
            #        label='Use phase')
            
            # ax.set_ylabel('g PMFP-eq /pkm')
            # ax.legend()
            
            # st.pyplot(fig)
        else: 
            labels = ['Diesel Bus 12m',  'ASSURED Bus 12m']
            production_phase = [diesel12production,assured12production]
            use_phase = [diesel12use,assured12use]
            width = 0.35       # the width of the bars: can also be len(x) sequence
            
            # fig, ax = plt.subplots()
            # plt.style.use('seaborn')
            # ax.bar(labels, production_phase, width, label='Production + EoL')
            # ax.bar(labels, use_phase, width, bottom=production_phase,
            #        label='Use phase')
            
            # ax.set_ylabel('g PMFP-eq /pkm')
            # ax.legend()
            
            # st.pyplot(fig)
        
        #make dataframe 
        
        bus_dict = { 'Buses': labels, 'Production + EoL': production_phase, 'Use Phase': use_phase }
        df = pd.DataFrame(bus_dict)
        df.set_index('Buses')
        df[method[1]] = df['Production + EoL'] + df['Use Phase']
        
        # update the co2 per km 
        
        # make a column if the bus is 12 or not 
        df['12m?'] = df['Buses'].str.contains('12m')
        #make a column of total sum of pm 
        df['sum'] = df['Production + EoL'] + df['Use Phase']
        
        #now co2 per km column 
        
        new_pm = []
    
        for pm, size in zip(df['sum'], df['12m?']): 
            if size == True : 
                new_pm.append(pm*average_passengers_12m)
            else: 
                new_pm.append(pm*average_passengers_18m)
        # st.write([average_passengers_12m, average_passengers_18m])
        # st.write(new_pm)
                
        df[method[1] +' per km'] = new_pm
        
        
        
        # st.write('Other emissions')
        # st.write(df)
        # df.to_csv(busline + ' single bus other emissions.csv')   
        return df 
    
    #pkm calculations
    # perkm = []
    # for m in methods_single: 
    #     perkm.append(perkm_single(m))
    # pkmsingle = pd.concat(perkm, axis = 0)
    #calctuation for other emissions 
    # st.title('pkm single')
    # st.write(pkmsingle)
    # pkmsingle.to_csv(busline + ' single bus other emission.csv')
        

    
    #st.write(df2)
    

    # if n18m_bus != 0: 
        
    
    # assured12use =do_lca(usephase12m)*1000
    # diesel12use =do_lca(use12mdiesel)*1000
    #st.write('per km calculation')
# per km calculation 
#     nox = ('CML 2001 (obsolete)', 'eutrophication potential', 'average European')
#     pm10 = ('ReCiPe Midpoint (E) V1.13 no LT', 'particulate matter formation', 'PMFP')
#     if n18m_bus != 0:
#         perkm18m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 
#         perkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 
#         pkmavg = np.mean([perkm18m, perkm12m])
#         total_imact_bus = n18m_bus*(do_lca(bus18mproduction, method =nox  )/perkm18m) 
#         + n12m_bus*(do_lca(bus12mproduction, method = nox)/perkm12m)
        
#         # use phases are already in person km unit
#         diesel18use = do_lca(use18mdiesel, method = nox)* average_passengers_18m # to convert from personkm to just km
#         assured18use =do_lca(usephase18m, method = nox) * average_passengers_18m
#         assured12use =do_lca(usephase12m, method = nox) * average_passengers_12m
#         diesel12use =do_lca(use12mdiesel, method = nox) * average_passengers_12m
        
#         total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
#         charger_impact = (fc*do_lca(fu_fc, method = nox)/pkmavg) + (oc*do_lca(fu_oc, method = nox)/pkmavg)
            
        
#         perkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 
#         perkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 
        
#         diesel12production =(do_lca(bus12mdieselproduction, method = nox)/perkmdiesel12)
#         diesel18production =(do_lca(bus18mdieselproduction, method = nox)/perkmdiesel18)
        
#         total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
#         total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
        
#         st.write('diesel technology')
#         st.write([total_diesel_bus_impact, total_use_impact_diesel ])
        
#         labels = ['Diesel Technology', 'ASSURED Technology']
#         production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
#         charger =np.array([0, charger_impact])
#         use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
#         width = 0.35       # the width of the bars: can also be len(x) sequence
        
#         fig, ax = plt.subplots()
#         plt.style.use('seaborn')
#         ax.bar(labels, production_phase, width, label='Production + EoL')
#         ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
#         ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
#                label='Use phase')
        
#         ax.set_ylabel('nox-eq /per km')
#         ax.legend()
        
#         st.pyplot(fig)  
    
#     else: 
#         perkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365
#         total_imact_bus =  n12m_bus*(do_lca(bus12mproduction, method = nox)/perkm12m)
#         assured12use =do_lca(usephase12m, method = nox) * average_passengers_12m
#         total_use_impact_assured =  assured12use* n12m_bus
#         charger_impact = (fc*do_lca(fu_fc, method = nox)/perkm12m) + (oc*do_lca(fu_oc, method = nox)/perkm12m)
            
        
#         perkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365
#         diesel12production =(do_lca(bus12mdieselproduction, method = nox)/perkmdiesel12)
#         diesel12use =do_lca(use12mdiesel, method = nox) * average_passengers_12m
        
#         total_diesel_bus_impact = diesel12production*n12m_bus 
#         total_use_impact_diesel = diesel12use* n12m_bus
        
#         labels = ['Diesel Technology', 'ASSURED Technology']
#         production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
#         charger =np.array([0, charger_impact])
#         use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
#         width = 0.35       # the width of the bars: can also be len(x) sequence
        
#         fig, ax = plt.subplots()
#         plt.style.use('seaborn')
#         ax.bar(labels, production_phase, width, label='Production + EoL')
#         ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
#         ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
#                label='Use phase')
        
#         ax.set_ylabel('nox-eq /per km')
#         ax.legend()
        
#         st.pyplot(fig) 
    
#     fleet_dict = {'Fleets': labels, 'Production + Eol': production_phase, 'Chargers': charger, 'Use Phase': use_phase}
#     df2 = pd.DataFrame(fleet_dict)
#     df2.set_index('Fleets')
    
#     st.write(df2)
#     df2.to_csv(busline + ' fleet level.csv')

# # per km calculation function
#     nox = ('CML 2001 (obsolete)', 'eutrophication potential', 'average European')
#     pm10 = ('ReCiPe Midpoint (E) V1.13 no LT', 'particulate matter formation', 'PMFP')
#     co2 = ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100')
#     perkm_methods = [nox, pm10, co2]
#     def perkm_fleet(method): 

#         if n18m_bus != 0:
#             perkm18m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 
#             perkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 
#             pkmavg = np.mean([perkm18m, perkm12m])
#             total_imact_bus = n18m_bus*(do_lca(bus18mproduction, method =method  )/perkm18m) 
#             + n12m_bus*(do_lca(bus12mproduction, method = method)/perkm12m)
            
#             # use phases are already in person km unit
#             diesel18use = do_lca(use18mdiesel, method = method)* average_passengers_18m # to convert from personkm to just km
#             assured18use =do_lca(usephase18m, method = method) * average_passengers_18m
#             assured12use =do_lca(usephase12m, method = method) * average_passengers_12m
#             diesel12use =do_lca(use12mdiesel, method = method) * average_passengers_12m
            
#             total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
#             charger_impact = (fc*do_lca(fu_fc, method = method)/pkmavg) + (oc*do_lca(fu_oc, method = method)/pkmavg)
                
            
#             perkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 
#             perkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 
            
#             diesel12production =(do_lca(bus12mdieselproduction, method = method)/perkmdiesel12)
#             diesel18production =(do_lca(bus18mdieselproduction, method = method)/perkmdiesel18)
            
#             total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
#             total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
            
#             # st.write('diesel technology')
#             # st.write([total_diesel_bus_impact, total_use_impact_diesel ])
            
#             labels = ['Diesel Technology', 'ASSURED Technology']
#             production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
#             charger =np.array([0, charger_impact])
#             use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
#             width = 0.35       # the width of the bars: can also be len(x) sequence
            
#             # fig, ax = plt.subplots()
#             # plt.style.use('seaborn')
#             # ax.bar(labels, production_phase, width, label='Production + EoL')
#             # ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
#             # ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
#             #        label='Use phase')
            
#             # ax.set_ylabel('nox-eq /per km')
#             # ax.legend()
            
#             # st.pyplot(fig)  
        
#         else: 
#             perkm12m = lifetime* return_trip_distance * number_of_return_trip_per_day * 365
#             total_imact_bus =  n12m_bus*(do_lca(bus12mproduction, method = method)/perkm12m)
#             assured12use =do_lca(usephase12m, method = method) * average_passengers_12m
#             total_use_impact_assured =  assured12use* n12m_bus
#             charger_impact = (fc*do_lca(fu_fc, method = method)/perkm12m) + (oc*do_lca(fu_oc, method = method)/perkm12m)
                
            
#             perkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365
#             diesel12production =(do_lca(bus12mdieselproduction, method = method)/perkmdiesel12)
#             diesel12use =do_lca(use12mdiesel, method = method) * average_passengers_12m
            
#             total_diesel_bus_impact = diesel12production*n12m_bus 
#             total_use_impact_diesel = diesel12use* n12m_bus
            
#             labels = ['Diesel Technology', 'ASSURED Technology']
#             production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
#             charger =np.array([0, charger_impact])
#             use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
#             width = 0.35       # the width of the bars: can also be len(x) sequence
            
#             # fig, ax = plt.subplots()
#             # plt.style.use('seaborn')
#             # ax.bar(labels, production_phase, width, label='Production + EoL')
#             # ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
#             # ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
#             #        label='Use phase')
            
#             # ax.set_ylabel(method[1] +'/per km')
#             # ax.legend()
            
#             # st.pyplot(fig) 
        
#         fleet_dict = {'Fleets': labels, 'Production + Eol': production_phase, 'Chargers': charger, 'Use Phase': use_phase}
#         df2 = pd.DataFrame(fleet_dict)
#         df2.set_index('Fleets')
        
#         # st.write(df2)
#         #df2.to_csv(busline + ' fleet level.csv')
#         return df2
# # calculate all emissions as once 
#     perkmdf =[]
#     for m in perkm_methods: 
#         perkmdf.append(perkm_fleet(m))
#     pkmdf = pd.concat(perkmdf, axis = 0)
#     pkmdf.to_csv(busline + ' allemissions single bus.csv')
    
# #future scenerio 
#     #set the new usephase activity 
#     usephase18m = [x for x in busdb if 'busEnergyMix' in x['name'] and '18m' in x['name']][0]
#     usephase12m = [x for x in busdb if 'busEnergyMix' in x['name'] and '13m' in x['name']][0]
    
#     def set_electric_demand_future(usephase, avg_passenger, yearly_consumption, year): 
#         # list of electricity mix of the country of the year 2030, 2040, 2050 
        
#         allelectricity = [x for x in usephase.technosphere() if 'electricity supply for electric vehicles' in x['name']]
        
#         for x in allelectricity: 
#             # print(x['amount'])
#             x['amount'] = 0
#             x.save()
            
        
#         personkm = lifetime* return_trip_distance * number_of_return_trip_per_day * 365 * avg_passenger
            
#         electriciy = [x for x in usephase.technosphere() if 'electricity supply for electric vehicles' in x['name']
#                                                                                   and bw.get_activity(x['input'])['location'] == country[busline]
#                                                                                   and str(year) in x['name'] ][0]
#         electriciy['amount'] = yearly_consumption*lifetime / personkm
#         electriciy.save()
        
    
#     if n18m_bus != 0:
#         pkmavg = np.mean([personkm18m, personkm12m])
#         total_imact_bus = n18m_bus*(do_lca(bus18mproduction)/personkm18m)*1000 + n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
#         charger_impact = (fc*do_lca(fu_fc)/pkmavg)*1000 + (oc*do_lca(fu_oc)/pkmavg)*1000
        
#         total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
#         total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
        
#         st.write('diesel technology')
#         st.write([total_diesel_bus_impact, total_use_impact_diesel ])
            
#         use_phase_results = {}
#         for year in [2025, 2030, 2035, 2040, 2045, 2050]: 
#             set_electric_demand_future(usephase18m, average_passengers_18m, yearly_consumption_18m, year)
#             if year not in use_phase_results: 
#                 use_phase_results[year] = [do_lca(usephase18m)*n18m_bus*1000]
#             else: 
#                 use_phase_results[year].append(do_lca(usephase18m)*n18m_bus*1000)
        
#         for year in [2025, 2030, 2035, 2040, 2045, 2050]: 
#             set_electric_demand_future(usephase12m, average_passengers_12m, yearly_consumption_12m, year)
#             if year not in use_phase_results: 
#                 use_phase_results[year] = [do_lca(usephase12m)*n12m_bus*1000]
#             else: 
#                 use_phase_results[year].append(do_lca(usephase12m)*n12m_bus*1000)
        
#         st.write(use_phase_results) 
        
#         st.write([x for x in use_phase_results])
            
#         labels = ['Diesel Technology', '2025 \n ASSURED\n Techonology', '2030 \n ASSURED\n Techonology', 
#                   '2035 \n ASSURED\n Techonology', '2040 \n ASSURED\n Techonology', '2045 \n ASSURED\n Techonology' ,'2050 \n ASSURED\n Techonology' ]
        
#         production_phase = np.array([total_diesel_bus_impact, total_imact_bus, total_imact_bus, total_imact_bus,  total_imact_bus, total_imact_bus, total_imact_bus])
        
#         charger_production = np.array([0,charger_impact,charger_impact,charger_impact,charger_impact,charger_impact,charger_impact])
        
#         use_phase = np.array([total_use_impact_diesel,sum(use_phase_results[2025]), sum(use_phase_results[2030]), sum(use_phase_results[2035]), sum(use_phase_results[2040]), sum(use_phase_results[2045]), sum(use_phase_results[2050])])
        
#         st.write(use_phase)
            
      
        
#         fig, ax = plt.subplots()
#         # sns.set_style('darkgrid')
#         plt.style.use('seaborn')
#         ax.bar(labels, production_phase, width, label='Production + EoL')
#         ax.bar(labels, charger_production, width, bottom =production_phase, label='Charger')
#         ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger_production]),
#                 label='Use phase')
        
#         ax.set_ylabel('g CO2-eq /pkm')
#         ax.legend()
#         plt.xticks(rotation= 0, size = 10) 
        
#         st.pyplot(fig)  
        
#         st.write('number of lca calculation')
#         st.write(do_lca.counter)
    
#     else: 
#         # pkmavg = np.mean([personkm18m, personkm12m])
#         total_imact_bus= n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
#         charger_impact = (fc*do_lca(fu_fc)/personkm12m)*1000 + (oc*do_lca(fu_oc)/personkm12m)*1000
        
#         total_diesel_bus_impact = diesel12production*n12m_bus 
#         total_use_impact_diesel = diesel12use* n12m_bus
        
#         st.write('diesel technology')
#         st.write([total_diesel_bus_impact, total_use_impact_diesel ])
            
#         use_phase_results = {}
                
#         for year in [2025, 2030, 2035, 2040, 2045, 2050]: 
#             set_electric_demand_future(usephase12m, average_passengers_12m, yearly_consumption_12m, year)
#             if year not in use_phase_results: 
#                 use_phase_results[year] = [do_lca(usephase12m)*n12m_bus*1000]
#             else: 
#                 use_phase_results[year].append(do_lca(usephase12m)*n12m_bus*1000)
        
#         st.write(use_phase_results)
        
#         st.write([x for x in use_phase_results])
            
#         labels = ['Diesel Technology', '2025 \n ASSURED\n Techonology', '2030 \n ASSURED\n Techonology', 
#                   '2035 \n ASSURED\n Techonology', '2040 \n ASSURED\n Techonology', '2045 \n ASSURED\n Techonology' ,'2050 \n ASSURED\n Techonology' ]
        
#         production_phase = np.array([total_diesel_bus_impact, total_imact_bus, total_imact_bus, total_imact_bus,  total_imact_bus, total_imact_bus, total_imact_bus])
        
#         charger_production = np.array([0,charger_impact,charger_impact,charger_impact,charger_impact,charger_impact,charger_impact])
        
#         use_phase = np.array([total_use_impact_diesel,sum(use_phase_results[2025]), sum(use_phase_results[2030]), sum(use_phase_results[2035]), sum(use_phase_results[2040]), sum(use_phase_results[2045]), sum(use_phase_results[2050])])
        
#         st.write(use_phase)
            
      
        
#         fig, ax = plt.subplots()
#         plt.style.use('seaborn')
#         ax.bar(labels, production_phase, width, label='Production + EoL')
#         ax.bar(labels, charger_production, width, bottom =production_phase, label='Charger')
#         ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger_production]),
#                 label='Use phase')
        
#         ax.set_ylabel('g CO2-eq /pkm')
#         ax.legend()
#         # plt.xticks(rotation= 45) 
#         st.pyplot(fig)  
        
    def endpoint_plot(method, plotnum =2): 
        if n18m_bus != 0: 
            set_charger_share_usephase(usephase18m,personkm18m, 0)
        
        set_charger_share_usephase(usephase12m,personkm12m, 0)
        
        if n18m_bus != 0: 
            diesel18use = do_lca(use18mdiesel, method = method)
            assured18use =do_lca(usephase18m, method = method)
        
        assured12use =do_lca(usephase12m, method = method)
        diesel12use =do_lca(use12mdiesel, method = method)
        
        # st.write('use phase values of ' + method[2])
        # st.write([diesel18use,assured18use, assured12use, diesel12use])
        
        if n18m_bus != 0: 
            personkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
            diesel18production =(do_lca(bus18mdieselproduction, method = method)/personkmdiesel18)
            # assured18production =(do_lca(bus18mproduction)/personkm18m)*1000
    
        personkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
        diesel12production =(do_lca(bus12mdieselproduction, method = method)/personkmdiesel12)
        # assured12production=(do_lca(bus12mproduction)/personkm12m)*1000
    
    
        if n18m_bus != 0:
            pkmavg = np.mean([personkm18m, personkm12m])
            total_imact_bus = n18m_bus*(do_lca(bus18mproduction, method = method)/personkm18m) 
            + n12m_bus*(do_lca(bus12mproduction, method = method)/personkm12m)
            
            total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
            
            charger_impact = (fc*do_lca(fu_fc, method = method)/pkmavg)
            + (oc*do_lca(fu_oc, method = method)/pkmavg)
                
            
            total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
            total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
            
            # st.write('use phase values of ' + method[2])
            # st.write([total_imact_bus,total_use_impact_assured, charger_impact, total_diesel_bus_impact,total_use_impact_diesel ])
            # st.write('diesel technology')
            # st.write([total_diesel_bus_impact, total_use_impact_diesel ])
            
            labels = ['Diesel Technology', 'ASSURED Technology']
            production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
            charger =np.array([0, charger_impact])
            use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
            width = 0.35       # the width of the bars: can also be len(x) sequence
            
            fig, ax = plt.subplots()
            plt.style.use('seaborn')
            ax.bar(labels, production_phase, width, label='Production + EoL')
            ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
            ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
                   label='Use phase')
            
            ax.set_ylabel(method[plotnum] + ' ' + bw.methods.get(method).get('unit'))
            ax.legend()
            #plt.savefig(fname = busline + ' ' + method[plotnum] )
            st.pyplot(fig) 
        
        else: 
            total_imact_bus =  n12m_bus*(do_lca(bus12mproduction, method = method)/personkm12m)
            total_use_impact_assured =  assured12use* n12m_bus
            charger_impact = (fc*do_lca(fu_fc, method = method)/personkm12m) + (oc*do_lca(fu_oc, method = method)/personkm12m)
                
            
            total_diesel_bus_impact = diesel12production*n12m_bus 
            total_use_impact_diesel = diesel12use* n12m_bus
            
            labels = ['Diesel Technology', 'ASSURED Technology']
            production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
            charger =np.array([0, charger_impact])
            use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
            width = 0.35       # the width of the bars: can also be len(x) sequence
            
            fig, ax = plt.subplots()
            plt.style.use('seaborn')
            ax.bar(labels, production_phase, width, label='Production + EoL')
            ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
            ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
                   label='Use phase')
            
            ax.set_ylabel(method[plotnum] + ' ' + bw.methods.get(method).get('unit'))
            ax.legend()
            plt.savefig(fname = busline + ' ' + method[plotnum] )
            st.pyplot(fig)
            
    
    
    
    
    # Endpoints 
    methods = [('ReCiPe Endpoint (H,A) (obsolete)','human health','climate change, human health'),
                 ('ReCiPe Endpoint (H,A) (obsolete)', 'human health', 'human toxicity'),
                 ('ReCiPe Endpoint (H,A) (obsolete)', 'human health', 'ionising radiation'),
                 ('ReCiPe Endpoint (H,A) (obsolete)', 'human health', 'ozone depletion'),
                 ('ReCiPe Endpoint (H,A) (obsolete)','human health','particulate matter formation'),
                 ('ReCiPe Endpoint (H,A) (obsolete)','human health','photochemical oxidant formation'),
                 ('ReCiPe Endpoint (H,A) (obsolete)', 'human health', 'total')]
    
    # st.write(methods[0]) 
    # endpoint_plot(methods[0])
    
    # for m in methods: 
    #     endpoint_plot(m)
    


    def endpoint_plot_stacked(method): 
        if n18m_bus != 0: 
            set_charger_share_usephase(usephase18m,personkm18m, 0)
        
        set_charger_share_usephase(usephase12m,personkm12m, 0)
        
        if n18m_bus != 0: 
            diesel18use = do_lca(use18mdiesel, method = method)
            assured18use =do_lca(usephase18m, method = method)
        
        assured12use =do_lca(usephase12m, method = method)
        diesel12use =do_lca(use12mdiesel, method = method)
        
        # st.write('use phase values of ' + method[2])
        # st.write([diesel18use,assured18use, assured12use, diesel12use])
        
        if n18m_bus != 0: 
            personkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
            diesel18production =(do_lca(bus18mdieselproduction, method = method)/personkmdiesel18)
            # assured18production =(do_lca(bus18mproduction)/personkm18m)*1000
    
        personkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
        diesel12production =(do_lca(bus12mdieselproduction, method = method)/personkmdiesel12)
        # assured12production=(do_lca(bus12mproduction)/personkm12m)*1000
    
    
        if n18m_bus != 0:
            pkmavg = np.mean([personkm18m, personkm12m])
            total_imact_bus = n18m_bus*(do_lca(bus18mproduction, method = method)/personkm18m) 
            + n12m_bus*(do_lca(bus12mproduction, method = method)/personkm12m)
            
            total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
            
            charger_impact = (fc*do_lca(fu_fc, method = method)/pkmavg)
            + (oc*do_lca(fu_oc, method = method)/pkmavg)
                
            
            total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
            total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
            
            
            #https://www.python-graph-gallery.com/13-percent-stacked-barplot
            # labels = ['Diesel Technology', 'ASSURED Technology']
            # production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
            # charger =np.array([0, charger_impact])
            # use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
            # width = 0.35       # the width of the bars: can also be len(x) sequence
            
            raw_data = {
                'production_phase': [total_diesel_bus_impact,total_imact_bus], 
                'charger': [0, charger_impact], 
                'use_phase': [total_use_impact_diesel,total_use_impact_assured]
                }
            df = pd.DataFrame(raw_data)
            
            totals = [i+j+k for i,j,k in zip(df['production_phase'], df['charger'], df['use_phase'])]
            production_phase = [i/j * 100 for i,j in zip(df['production_phase'], totals)]
            charger = [i/j * 100 for i,j in zip(df['charger'], totals)]
            use_phase = [i/j * 100 for i,j in zip(df['use_phase'], totals)]
            
            
            #plot 
            fig, ax = plt.subplots()
            barWidth = 0.35 
            labels = ['Diesel Technology', 'ASSURED Technology']
            # r = [0,1]
            # Create production phase bar
            ax.bar(labels, production_phase, width = barWidth, label = 'Production + EoL')
            ax.bar(labels, charger, bottom = production_phase, width = barWidth, label = 'Charger')
            ax.bar(labels, use_phase, bottom = [i+j for i,j in zip(production_phase,charger)]
                                                           , width = barWidth, 
                                                           label = 'Use Phase')
            ax.set_ylabel(method[2])
            ax.legend()
            
            

            st.pyplot(fig) 
        
        else: 
            total_imact_bus =  n12m_bus*(do_lca(bus12mproduction, method = method)/personkm12m)
            total_use_impact_assured =  assured12use* n12m_bus
            charger_impact = (fc*do_lca(fu_fc, method = method)/personkm12m) + (oc*do_lca(fu_oc, method = method)/personkm12m)
                
            
            total_diesel_bus_impact = diesel12production*n12m_bus 
            total_use_impact_diesel = diesel12use* n12m_bus
            
            raw_data = {
                'production_phase': [total_diesel_bus_impact,total_imact_bus], 
                'charger': [0, charger_impact], 
                'use_phase': [total_use_impact_diesel,total_use_impact_assured]
                }
            df = pd.DataFrame(raw_data)
            
            totals = [i+j+k for i,j,k in zip(df['production_phase'], df['charger'], df['use_phase'])]
            production_phase = [i/j * 100 for i,j in zip(df['production_phase'], totals)]
            charger = [i/j * 100 for i,j in zip(df['charger'], totals)]
            use_phase = [i/j * 100 for i,j in zip(df['use_phase'], totals)]
            
            
            #plot 
            fig, ax = plt.subplots()
            barWidth = 0.35 
            labels = ['Diesel Technology', 'ASSURED Technology']
            # r = [0,1]
            # Create production phase bar
            ax.bar(labels, production_phase, width = barWidth, label = 'Production + EoL')
            ax.bar(labels, charger, bottom = production_phase, width = barWidth, label = 'Charger')
            ax.bar(labels, use_phase, bottom = [i+j for i,j in zip(production_phase,charger)]
                                                           , width = barWidth, 
                                                           label = 'Use Phase')
            ax.set_ylabel(method[2])
            ax.legend()
            st.pyplot(fig)
    
    
    # with all midpoints         
    all_midpoint_recipe = [('ReCiPe Midpoint (H) V1.13', 'freshwater ecotoxicity', 'FETPinf'),
                             ('ReCiPe Midpoint (H) V1.13', 'human toxicity', 'HTPinf'),
                             ('ReCiPe Midpoint (H) V1.13', 'marine ecotoxicity', 'METPinf'),
                             ('ReCiPe Midpoint (H) V1.13', 'terrestrial ecotoxicity', 'TETPinf'),
                             ('ReCiPe Midpoint (H) V1.13', 'metal depletion', 'MDP'),
                             ('ReCiPe Midpoint (H) V1.13', 'agricultural land occupation', 'ALOP'),
                             ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100'),
                             ('ReCiPe Midpoint (H) V1.13', 'fossil depletion', 'FDP'),
                             ('ReCiPe Midpoint (H) V1.13', 'freshwater eutrophication', 'FEP'),
                             ('ReCiPe Midpoint (H) V1.13', 'ionising radiation', 'IRP_HE'),
                             ('ReCiPe Midpoint (H) V1.13', 'marine eutrophication', 'MEP'),
                             ('ReCiPe Midpoint (H) V1.13', 'natural land transformation', 'NLTP'),
                             ('ReCiPe Midpoint (H) V1.13', 'ozone depletion', 'ODPinf'),
                             ('ReCiPe Midpoint (H) V1.13', 'particulate matter formation', 'PMFP'),
                             ('ReCiPe Midpoint (H) V1.13', 'photochemical oxidant formation', 'POFP'),
                             ('ReCiPe Midpoint (H) V1.13', 'terrestrial acidification', 'TAP100'),
                             ('ReCiPe Midpoint (H) V1.13', 'urban land occupation', 'ULOP'),
                             ('ReCiPe Midpoint (H) V1.13', 'water depletion', 'WDP')]
    # define multi lca function
    def multi_lca(activity, methods = all_midpoint_recipe): 
        
        
      inventory = [{activity.key:1}]  
      bw.calculation_setups['production'] = {'inv':inventory, 'ia':  methods} 
      lcaresults = bw.MultiLCA('production')  
      
      return lcaresults.results
        
  # #Fleet lca 
  #   if n18m_bus != 0: 
  #       personkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
  #       diesel18production =(do_lca(bus18mdieselproduction)/personkmdiesel18)*1000
  #       assured18production =(do_lca(bus18mproduction)/personkm18m)*1000
    
  #   personkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
  #   diesel12production =(do_lca(bus12mdieselproduction)/personkmdiesel12)*1000
  #   assured12production=(do_lca(bus12mproduction)/personkm12m)*1000
    
    
  #   if n18m_bus != 0: 
  #       diesel18use = do_lca(use18mdiesel)*1000
  #       assured18use =do_lca(usephase18m)*1000
    
  #   assured12use =do_lca(usephase12m)*1000
  #   diesel12use =do_lca(use12mdiesel)*1000
    
  #   if n18m_bus != 0: 
  #       total_imact_bus = n18m_bus*(do_lca(bus18mproduction)/personkm18m)*1000 + n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
  #   else: 
  #       total_imact_bus = n12m_bus*(do_lca(bus12mproduction)/personkm12m)*1000
    
  #   fu_fc = [x for x in fast_charger_activity if str(fc_power) in x['name']][0]
  #   fu_oc = [x for x in overnight_charger_activity if str(oc_power) in x['name']][0]
    
  #   if n18m_bus != 0: 
  #       fc_charger_impact = (fc*do_lca(fu_fc)/personkm18m)*1000 + (oc*do_lca(fu_oc)/personkm18m)*1000
  #   else: 
  #       fc_charger_impact = (fc*do_lca(fu_fc)/personkm12m)*1000 + (oc*do_lca(fu_oc)/personkm12m)*1000    
  
        #   pkmavg = np.mean([personkm18m, personkm12m])
        # total_imact_bus = n18m_bus*assured18production + n12m_bus*assured12production
        # #total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
        # total_use_impact_assured = n18m_bus*assured18use + n12m_bus*assured12use
        # charger_impact = (fc*do_lca(fu_fc)/pkmavg)*1000 + (oc*do_lca(fu_oc)/pkmavg)*1000
    
        
    st.subheader(" Relative aggregated results of ReCiPe midpoint impact categories")    
    if n18m_bus != 0:   
        dieseltotal = (multi_lca(bus18mdieselproduction)/personkmdiesel18)*n18m_bus + (multi_lca(bus12mdieselproduction)/personkmdiesel12)*n18m_bus +\
                       multi_lca(use18mdiesel)*n18m_bus+ multi_lca(use12mdiesel)*n12m_bus 
            
        pkmavg = np.mean([personkm18m, personkm12m])
        assuredtotal = (multi_lca(bus18mproduction)/personkmdiesel18)*n18m_bus + (multi_lca(bus12mproduction)/personkmdiesel12)*n18m_bus +\
                       multi_lca(usephase18m)*n18m_bus+ multi_lca(usephase12m)*n12m_bus +\
                           fc*multi_lca(fu_fc)/pkmavg + oc*multi_lca(fu_oc)/pkmavg
        
        # st.write(dieseltotal)
        # st.write(assuredtotal)
        
        col_name = [x[1] for x in all_midpoint_recipe]
        d  = pd.DataFrame(columns = col_name, index = ['Diesel Technology', 'ASSURED Technology'])
        d.loc['Diesel Technology'] = dieseltotal
        d.loc['ASSURED Technology'] = assuredtotal
        
        d1 = d.div(d.iloc[0])
        d2 = d1.T 
        
        
        
        import plotly.graph_objects as go 
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['Diesel Technology'], 
            name = 'Diesel Technology', 
            marker_color = 'indianred'
            
            ))
        
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['ASSURED Technology'], 
            name = 'ASSURED Technology', 
            marker_color = 'lightsalmon'   
            
            ))
        fig.update_layout(barmode = 'group', xaxis_tickangle = 90)
        fig.update_layout(
            #title="Plot Title",
            #xaxis_title="x Axis Title",
            
            yaxis_title="Relative results",
           autosize = False, 
                        width = 900, 
                        height = 600,
            
        )          
        
        st.plotly_chart(fig)
    else: 
        dieseltotal = ( multi_lca(bus12mdieselproduction)/personkmdiesel12)*n12m_bus +\
                        multi_lca(use12mdiesel)*n12m_bus
            
        # pkmavg = np.mean([personkm18m, personkm12m])
        assuredtotal = (multi_lca(bus12mproduction)/personkm12m)*n12m_bus +\
                        multi_lca(usephase12m)*n12m_bus +\
                           fc*multi_lca(fu_fc)/personkm12m + oc*multi_lca(fu_oc)/personkm12m  
        
        # st.write(dieseltotal)
        # st.write(assuredtotal)
        
        col_name = [x[1] for x in all_midpoint_recipe]
        d  = pd.DataFrame(columns = col_name, index = ['Diesel Technology', 'ASSURED Technology'])
        d.loc['Diesel Technology'] = dieseltotal
        d.loc['ASSURED Technology'] = assuredtotal
        
        d1 = d.div(d.iloc[0])
        d2 = d1.T 
        
        
        
        import plotly.graph_objects as go 
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['Diesel Technology'], 
            name = 'Diesel Technology', 
            marker_color = 'indianred'
            
            ))
        
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['ASSURED Technology'], 
            name = 'ASSURED Technology', 
            marker_color = 'lightsalmon'   
            
            ))
        fig.update_layout(barmode = 'group', xaxis_tickangle = 90)
        fig.update_layout(
            #title="Plot Title",
            #xaxis_title="x Axis Title",
            
            yaxis_title="Relative results",
           autosize = False, 
                        width = 900, 
                        height = 600,
            
        )    
        
        st.plotly_chart(fig)

    #production phase 
    st.subheader('Relative results of Production and EoL phase')
    if n18m_bus != 0:   
        dieselproduction = (multi_lca(bus18mdieselproduction)/personkmdiesel18)*n18m_bus + (multi_lca(bus12mdieselproduction)/personkmdiesel12)*n18m_bus
            
        pkmavg = np.mean([personkm18m, personkm12m])
        assuredproduction = (multi_lca(bus18mproduction)/personkmdiesel18)*n18m_bus + (multi_lca(bus12mproduction)/personkmdiesel12)*n12m_bus +\
                           fc*multi_lca(fu_fc)/pkmavg + oc*multi_lca(fu_oc)/pkmavg
        
        # st.write(dieseltotal)
        # st.write(assuredtotal)
        
        col_name = [x[1] for x in all_midpoint_recipe]
        d  = pd.DataFrame(columns = col_name, index = ['Diesel Technology', 'ASSURED Technology'])
        d.loc['Diesel Technology'] = dieselproduction
        d.loc['ASSURED Technology'] = assuredproduction
        
        d1 = d.div(d.iloc[0])
        d2 = d1.T 
        
        
        
        import plotly.graph_objects as go 
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['Diesel Technology'], 
            name = 'Diesel Technology', 
            marker_color = 'indianred'
            
            ))
        
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['ASSURED Technology'], 
            name = 'ASSURED Technology', 
            marker_color = 'lightsalmon'   
            
            ))
        fig.update_layout(barmode = 'group', xaxis_tickangle = 90)
        fig.update_layout(
            #title="Plot Title",
            #xaxis_title="x Axis Title",
            
            yaxis_title="Relative results",
           autosize = False, 
                        width = 900, 
                        height = 600,
            
        )          
        
        st.plotly_chart(fig)
    else: 
        dieseltotal = ( multi_lca(bus12mdieselproduction)/personkmdiesel12)*n12m_bus 
            
        # pkmavg = np.mean([personkm18m, personkm12m])
        assuredtotal = (multi_lca(bus12mproduction)/personkm12m)*n12m_bus +\
                           fc*multi_lca(fu_fc)/personkm12m + oc*multi_lca(fu_oc)/personkm12m  
        
        # st.write(dieseltotal)
        # st.write(assuredtotal)
        
        col_name = [x[1] for x in all_midpoint_recipe]
        d  = pd.DataFrame(columns = col_name, index = ['Diesel Technology', 'ASSURED Technology'])
        d.loc['Diesel Technology'] = dieseltotal
        d.loc['ASSURED Technology'] = assuredtotal
        
        d1 = d.div(d.iloc[0])
        d2 = d1.T 
        
        
        
        import plotly.graph_objects as go 
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['Diesel Technology'], 
            name = 'Diesel Technology', 
            marker_color = 'indianred'
            
            ))
        
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['ASSURED Technology'], 
            name = 'ASSURED Technology', 
            marker_color = 'lightsalmon'   
            
            ))
        fig.update_layout(barmode = 'group', xaxis_tickangle = 90)
        fig.update_layout(
            #title="Plot Title",
            #xaxis_title="x Axis Title",
            
            yaxis_title="Relative results",
           autosize = False, 
                        width = 900, 
                        height = 600,
            
        )    
        
        st.plotly_chart(fig)
        
    st.subheader('Relative results of Use phase') 
    if n18m_bus != 0:   
        dieseltotal = multi_lca(use18mdiesel)*n18m_bus+ multi_lca(use12mdiesel)*n12m_bus 
            
        
        assuredtotal = (multi_lca(usephase18m))*n18m_bus+ multi_lca(usephase12m)*n12m_bus
        
        # st.write(dieseltotal)
        # st.write(assuredtotal)
        
        col_name = [x[1] for x in all_midpoint_recipe]
        d  = pd.DataFrame(columns = col_name, index = ['Diesel Technology', 'ASSURED Technology'])
        d.loc['Diesel Technology'] = dieseltotal
        d.loc['ASSURED Technology'] = assuredtotal
        
        d1 = d.div(d.iloc[0])
        d2 = d1.T 
        
        
        
        import plotly.graph_objects as go 
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['Diesel Technology'], 
            name = 'Diesel Technology', 
            marker_color = 'indianred'
            
            ))
        
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['ASSURED Technology'], 
            name = 'ASSURED Technology', 
            marker_color = 'lightsalmon'   
            
            ))
        fig.update_layout(barmode = 'group', xaxis_tickangle = 90)
        fig.update_layout(
            #title="Plot Title",
            #xaxis_title="x Axis Title",
            
            yaxis_title="Relative results",
           autosize = False, 
                        width = 900, 
                        height = 600,
            
        )     
        fig.update_traces(marker=dict(size=12,
                          line=dict(width=2,
                                    color='DarkSlateGrey')),
              selector=dict(mode='markers'))
        
        st.plotly_chart(fig)
    else: 
        dieseltotal = multi_lca(use12mdiesel)*n12m_bus
            
        # pkmavg = np.mean([personkm18m, personkm12m])
        assuredtotal = multi_lca(usephase12m)*n12m_bus 
        
        # st.write(dieseltotal)
        # st.write(assuredtotal)
        
        col_name = [x[1] for x in all_midpoint_recipe]
        d  = pd.DataFrame(columns = col_name, index = ['Diesel Technology', 'ASSURED Technology'])
        d.loc['Diesel Technology'] = dieseltotal
        d.loc['ASSURED Technology'] = assuredtotal
        
        d1 = d.div(d.iloc[0])
        d2 = d1.T 
        
        
        
        import plotly.graph_objects as go 
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['Diesel Technology'], 
            name = 'Diesel Technology', 
            marker_color = 'indianred'
            
            ))
        
        fig.add_trace(go.Bar(
            x = col_name, 
            y = d2['ASSURED Technology'], 
            name = 'ASSURED Technology', 
            marker_color = 'lightsalmon'   
            
            ))
        fig.update_layout(barmode = 'group', xaxis_tickangle = 90)
        fig.update_layout(
            #title="Plot Title",
            #xaxis_title="x Axis Title",
            
            yaxis_title="Relative results",
           autosize = False, 
                        width = 900, 
                        height = 600,
            
        )  
        fig.update_traces(marker=dict(size=15,
                          line=dict(width=2,
                                    color='DarkSlateGrey')),
              selector=dict(mode='markers'))
        
        st.plotly_chart(fig)

    #check other midpoints 
    midpoints = [x for x in bw.methods if 'recipe' in str(x).lower()
                                    and 'midpoint (h)' in str(x).lower()
                                    and 'obsolete' not in str(x).lower()
                                    and 'LT' not in str(x)]
    endpoints = [x for x in bw.methods if '2016' in str(x) and 'ReCiPe' in str(x) 
                                                 and 'DALY' in bw.methods.get(x).get('unit') and 'Hierarchist' in str(x)]
    # for m in midpoints: 
    #     endpoint_plot(m,plotnum =2)
    
    # st.write('Endpoints')
    # for m in endpoints: 
    #     endpoint_plot(m,plotnum =4)
        
    st.subheader('ReCiPe 2016(H) - Human health, Aggregated DALY ')
    endpoint_plot(('ReCiPe 2016',
  '1.1 (20180117)',
  'Endpoint',
  'Human health',
  'Aggregated',
  'Hierarchist'), plotnum =4)   


        
    # st.write('number of lca calculation')
    # st.write(do_lca.counter) 
    def endpoint_plot_relative(method, plotnum =2): 
        if n18m_bus != 0: 
            set_charger_share_usephase(usephase18m,personkm18m, 0)
        
        set_charger_share_usephase(usephase12m,personkm12m, 0)
        
        if n18m_bus != 0: 
            diesel18use = do_lca(use18mdiesel, method = method)
            assured18use =do_lca(usephase18m, method = method)
        
        assured12use =do_lca(usephase12m, method = method)
        diesel12use =do_lca(use12mdiesel, method = method)
        
        # st.write('use phase values of ' + method[2])
        # st.write([diesel18use,assured18use, assured12use, diesel12use])
        
        if n18m_bus != 0: 
            personkmdiesel18 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_18m
            diesel18production =(do_lca(bus18mdieselproduction, method = method)/personkmdiesel18)
            # assured18production =(do_lca(bus18mproduction)/personkm18m)*1000
    
        personkmdiesel12 = 12* return_trip_distance * number_of_return_trip_per_day * 365 * average_passengers_12m
        diesel12production =(do_lca(bus12mdieselproduction, method = method)/personkmdiesel12)
        # assured12production=(do_lca(bus12mproduction)/personkm12m)*1000
    
    
        if n18m_bus != 0:
            pkmavg = np.mean([personkm18m, personkm12m])
            total_imact_bus = n18m_bus*(do_lca(bus18mproduction, method = method)/personkm18m) 
            + n12m_bus*(do_lca(bus12mproduction, method = method)/personkm12m)
            
            total_use_impact_assured = assured18use*n18m_bus + assured12use* n12m_bus
            
            charger_impact = (fc*do_lca(fu_fc, method = method)/pkmavg)
            + (oc*do_lca(fu_oc, method = method)/pkmavg)
                
            
            total_diesel_bus_impact = diesel12production*n12m_bus + diesel18production*n18m_bus
            total_use_impact_diesel = diesel18use*n18m_bus + diesel12use* n12m_bus
            
            # st.write('use phase values of ' + method[2])
            # st.write([total_imact_bus,total_use_impact_assured, charger_impact, total_diesel_bus_impact,total_use_impact_diesel ])
            # st.write('diesel technology')
            # st.write([total_diesel_bus_impact, total_use_impact_diesel ])
            
            labels = ['Diesel Technology', 'ASSURED Technology']
            production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
            charger =np.array([0, charger_impact])
            use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
            width = 0.35       # the width of the bars: can also be len(x) sequence
            
            total = production_phase + use_phase + charger
            
            # total = np.array([diseltotal, assuredtotal]). So 
            # total/total[0] will be [1, assuredtotal/dieseltolal] which will 
            #give relative total result 
            relative_total = total/total[0]
            
            fig, ax = plt.subplots()
            plt.style.use('seaborn')
            ax.bar(labels, relative_total, width, label='Relative result')
            # ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
            # ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
            #        label='Use phase')
            
            ax.set_ylabel(method[plotnum] + ' ' + bw.methods.get(method).get('unit'))
            ax.legend()
            #plt.savefig(fname = busline + ' ' + method[plotnum] )
            st.pyplot(fig) 
        
        else: 
            total_imact_bus =  n12m_bus*(do_lca(bus12mproduction, method = method)/personkm12m)
            total_use_impact_assured =  assured12use* n12m_bus
            charger_impact = (fc*do_lca(fu_fc, method = method)/personkm12m) + (oc*do_lca(fu_oc, method = method)/personkm12m)
                
            
            total_diesel_bus_impact = diesel12production*n12m_bus 
            total_use_impact_diesel = diesel12use* n12m_bus
            
            labels = ['Diesel Technology', 'ASSURED Technology']
            production_phase = np.array([total_diesel_bus_impact,total_imact_bus])
            charger =np.array([0, charger_impact])
            use_phase = np.array([total_use_impact_diesel,total_use_impact_assured])
            width = 0.35       # the width of the bars: can also be len(x) sequence

            total = production_phase + use_phase + charger
            
            # total = np.array([diseltotal, assuredtotal]). So 
            # total/total[0] will be [1, assuredtotal/dieseltolal] which will 
            #give relative total result 
            relative_total = total/total[0]
            
            fig, ax = plt.subplots()
            plt.style.use('seaborn')
            ax.bar(labels, relative_total, width)
            # ax.bar(labels, charger, width, bottom =production_phase, label='Charger')
            # ax.bar(labels, use_phase, width, bottom=sum([production_phase,charger]),
            #        label='Use phase')
            
            ax.set_ylabel(method[plotnum] + ' ' + bw.methods.get(method).get('unit'))
            ax.legend()
            plt.savefig(fname = busline + ' ' + method[plotnum] )
            st.pyplot(fig)

    st.subheader('ReCiPe 2016(H) - Human health, Aggregated DALY ')
    endpoint_plot_relative(('ReCiPe 2016',
  '1.1 (20180117)',
  'Endpoint',
  'Human health',
  'Aggregated',
  'Hierarchist'), plotnum =4) 