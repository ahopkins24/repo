"""
Name: Aidan Hopkins
CS230: Section 005
Data: NCAA Stadiums
URL: Link to your web application online
Description:
This program takes data from all NCAA Division 1 Football stadiums and compiles them into a user-friendly Streamlit app.
The user can sort by division, conference, and popular rivalries to get more information on the stadiums all 253 NCAA
Division 1 Football teams play in.
"""

python -m pip install folium
import os
import webbrowser
import folium
import pandas as pd
import csv
import pprint as pp
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components
import pyautogui



df_stadiums = pd.read_csv("stadiums.csv") # creates a dataframe that looks like the original CSV file w some columns/rows hidden
df_stadiums = df_stadiums.sort_values(by=['team']) #sort df by team name alphabetically


with open('stadiums.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        key = csv_reader.fieldnames
        dict_stadiums = {}
        for row in csv_reader:
            dict_stadiums[row['team']] = row
columns = list(df_stadiums.columns)


st.title("NCAA Stadiums") # Name webpage
rad_select = st.sidebar.radio("See schools by: ", ("Division","Rivalries"))#UI Control- radio buttons
if rad_select == "Division":
    global divis
    divis = st.sidebar.radio("Select a Division", ("FCS","FBS")) # page design features- sidebar
    def division(dict,d): #one function that has two parameters that returns a value
        global fcs
        global fbs
        fcs = {}
        fbs = {}
        d = d.lower()
        if d == "fcs":
            for i in dict:
                if dict[i]['div'] == d:
                    fcs[i] = dict[i]
                else:
                    fbs[i] = dict[i]
        else:
            for i in dict:
                if dict[i]['div'] == d:
                    fbs[i] = dict[i]
                else:
                    fcs[i] = dict[i]

        return(fcs, fbs)
    division(dict_stadiums,divis)
    fcs_conferences = []
    fbs_conferences = []
    for i in dict_stadiums:
        if dict_stadiums[i]['div'] == "fcs":
            if dict_stadiums[i]['conference'] not in fcs_conferences:
                fcs_conferences.append(dict_stadiums[i]['conference'])
        else:
            if dict_stadiums[i]['conference'] not in fbs_conferences:
                fbs_conferences.append(dict_stadiums[i]['conference'])


    def divconf(n): # function that does not return a value
        global conference_selection
        if n == "FCS":
            conference_selection = st.sidebar.radio("Select a Conference", fcs_conferences)
        else:
            conference_selection = st.sidebar.radio("Select a Conference", fbs_conferences)

    divconf(divis) #run function to create radio button containing all the conferences in the selected division


    def confSelect(conference):
        global single
        global schools
        st.header(f'The {conference} Conference')
        df_conference = df_stadiums.loc[df_stadiums["conference"]==conference, ["team"]] #creating a new dataframe based on selected data
        schools = df_conference['team'].tolist()
        single = st.selectbox("Please select a school", schools) #UI Control- drop down
        for i in range(len(df_stadiums)): # a loop that iterates through items in a list, dictionary, or tuple
            if df_stadiums.at[i, "team"] == single:
                if pd.isna(df_stadiums.at[i, "expanded"]) == True:
                    st.write(f'{df_stadiums.at[i, "stadium"]} is in {df_stadiums.at[i, "city"]}, {df_stadiums.at[i, "state"]}, with a capacity of {df_stadiums.at[i, "capacity"]:,}. It was built in {df_stadiums.at[i, "built"]}.')
                else:
                    expanded_var = df_stadiums.at[i, "expanded"]
                    st.write(f'{df_stadiums.at[i, "stadium"]} is in {df_stadiums.at[i, "city"]}, {df_stadiums.at[i, "state"]}, with a capacity of {df_stadiums.at[i, "capacity"]:,}. It was built in {df_stadiums.at[i, "built"]} and first expanded in {expanded_var[0:4]}.')


    confSelect(conference_selection) # print onto the main page, allow user to select one of the teams in the selected conference


    filters = st.radio(f"Would you like to see only schools in the {conference_selection} Conference, in the {divis} division, or all schools ?", (conference_selection, divis, "All"))
    if filters == "All":
        global small
        small = st.slider(f"Show stadiums of capacity greater than: ", 2000, 110000)
    if filters == divis:
        small = st.slider(f"Show {divis} stadiums of capacity greater than: ", 2000, 110000)




    def showonmap(placelist):
        center = [39.82852302607694, -98.57894326018148]  # The [lat, lon] of the center of the United States
        stadiumsmap = folium.Map(location = center, zoom_start=4)


        for i in range(len(placelist)):
            lat = placelist.at[i, "latitude"]
            lon = placelist.at[i, "longitude"]
            d = placelist.at[i, "div"]
            conf = placelist.at[i, 'conference']
            name = placelist.at[i, "stadium"]
            cap = placelist.at[i, "capacity"]
            t = placelist.at[i, "team"]

            if filters == conference_selection:
                if conf == conference_selection:
                    if t == single:
                        icon = folium.Icon(icon= 'football-ball', prefix="fa", color='green')
                        folium.Marker(location=[lat, lon],
                                        tooltip= name,
                                        icon = icon).add_to(stadiumsmap)
                    else:
                        if d == "fbs": # color codes by division
                            icon = folium.Icon(icon= 'football-ball', prefix="fa", color="lightblue")
                            folium.Marker(location=[lat, lon],
                                            tooltip= name,
                                            icon = icon).add_to(stadiumsmap)
                        else:
                            icon = folium.Icon(icon= 'football-ball', prefix="fa", color="lightred")
                            folium.Marker(location=[lat, lon],
                                            tooltip= name,
                                            icon = icon).add_to(stadiumsmap)

            elif filters == divis:
                if d == divis.lower():
                    if cap > small:
                        if t == single:
                            icon = folium.Icon(icon= 'football-ball', prefix="fa", color='green')
                            folium.Marker(location=[lat, lon],
                                            tooltip= name,
                                            icon = icon).add_to(stadiumsmap)
                        else:
                            if d == "fbs":
                                icon = folium.Icon(icon= 'football-ball', prefix="fa", color="lightblue")
                                folium.Marker(location=[lat, lon],
                                                tooltip= name,
                                                icon = icon).add_to(stadiumsmap)
                            else:
                                icon = folium.Icon(icon= 'football-ball', prefix="fa", color="lightred")
                                folium.Marker(location=[lat, lon],
                                                tooltip= name,
                                                icon = icon).add_to(stadiumsmap)
            else:
                if cap > small:
                        if t == single:
                            icon = folium.Icon(icon= 'football-ball', prefix="fa", color='green') # page design features- colors
                            folium.Marker(location=[lat, lon],
                                            tooltip= name,
                                            icon = icon).add_to(stadiumsmap)
                        else:
                            if d == "fbs":
                                icon = folium.Icon(icon= 'football-ball', prefix="fa", color="lightblue")
                                folium.Marker(location=[lat, lon],
                                                tooltip= name,
                                                icon = icon).add_to(stadiumsmap)
                            else:
                                icon = folium.Icon(icon= 'football-ball', prefix="fa", color="lightred")
                                folium.Marker(location=[lat, lon],
                                                tooltip= name,
                                                icon = icon).add_to(stadiumsmap)


        filePath = os.getcwd() + "\\stadiumsmap.html"
        stadiumsmap.save(filePath)

    def main():
        stadiums = df_stadiums
        showonmap(stadiums)

    main()

    st.header("Maps")

    HtmlFile = open("stadiumsmap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    print(source_code)
    components.html(source_code, height = 600)

    st.write(f'The map above is displaying the location of various stadiums. The green pin is the stadium of {single}, red pins are stadiums of schools that compete in the FCS division, and blue pins are stadiums of schools that compete in the FBS division.')

    if filters == "All":
        df_caps = df_stadiums.loc[:,["capacity"]]
        caps = df_caps["capacity"].tolist()
        breaks = [0,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000]
        fig0, ax0 = plt.subplots() # chart
        ax0.hist(caps, bins = breaks, color = "y")
        ax0.set_xticklabels(breaks, rotation = 33, fontsize = 10, ha='right')
        plt.xticks(breaks)
        plt.xlabel("Capacity")
        plt.ylabel("No. of Stadiums in NCAA Football")
        plt.title(f'Histogram of Stadium Capacity')
        st.pyplot(fig0)
        st.write("The histogram above shows that the most frequenct capacity size of stadiums in NCAA Divsion 1 is between 10,000 and 20,000")
        df_stadiums['direction'] = pd.cut(df_stadiums['latitude'], bins=[0, 39.82852302607694, float('Inf')], labels=['South', 'North'])
        pivot = pd.pivot_table(df_stadiums, values='capacity',
                                index='div',
                                columns='direction',
                                aggfunc=np.mean)
        st.write(pivot)
        st.write("The table above displays average capacity of stadium by division as well as region (North or South, based on latitude)")



    df_cap = df_stadiums.loc[df_stadiums["conference"]==conference_selection, ["team","capacity"]]
    df_cap = df_cap.sort_values(by=["capacity"])
    x = df_cap["team"].tolist()
    y = df_cap["capacity"].tolist()

    colors = []
    for i in x:
        if i == single:
            colors.append("green")
        else:
            colors.append("gray")
    fig, ax = plt.subplots() # chart
    ax.barh(x,y, color=colors)
    plt.xlabel("Capacity")
    plt.ylabel("Schools")
    plt.title(f'Capacity by School in the {conference_selection} Conference')
    st.pyplot(fig)



    range_tuple = st.slider("**THE SLIDER BELOW ONLY INCLUDES STADIUMS THAT HAVE BEEN EXPANDED**", 1890,2020, (1890, 2000))#UI Control- slider
    min = range_tuple[0]
    max = range_tuple[1]
    st.write(f'Schools in the {conference_selection} Conference that were built before {min} and first expanded after {max}:')



    slider_list = []
    for i in dict_stadiums:
        if dict_stadiums[i]['conference'] == conference_selection:
            if dict_stadiums[i]['expanded'] != '':
                built = int(dict_stadiums[i]['built'])
                expanded0 = dict_stadiums[i]['expanded']
                expanded = int(expanded0[0:4])
                if built<=min and expanded>=max:
                    slider_list.append((i, dict_stadiums[i]['stadium'], dict_stadiums[i]['built'], (dict_stadiums[i]['expanded'])[0:4]))

    slider_list.sort(key=lambda x:x[2])
    for items in slider_list:
        st.write(f'\n{items[0]:<30}: {items[1]} was built in {items[2]} and first expanded in {items[3]}')
    if slider_list == []:
        st.write(f'Looks like no schools in the {conference_selection} Conference were built before {min} and/or expanded after {max}.\n Please try a broader range.')

else:
    rivalry_list = []
    rivalry_teams_tuples = [("Army","Navy"),("Alabama","Auburn"),("Michigan","Ohio State"),("Oklahoma","Texas"),("Southern California","Notre Dame"),("Harvard Crimson","Yale Bulldogs"),("Florida","Florida State"),("California","Stanford"),("Clemson","South Carolina"),("Lafayette Leopards","Lehigh Mountain Hawks")] # got this data on the Top 25 Rivalries in College Football from Athlon Sports
    for rivalries in rivalry_teams_tuples: #list comprehension
        riv = (f'{rivalries[0]} vs {rivalries[1]}')
        rivalry_list.append(riv)
    select_rivalry = st.sidebar.radio("Select a Rivalry", rivalry_list)

    st.write("*The rivalries on this page came from [here](https://athlonsports.com/college-football/ranking-top-25-rivalries-college-football-history-2015)")
    st.header(f'The {select_rivalry} Rivalry')
    def rivalries(selection, df=df_stadiums): #a function with a default input
        global j1
        global j2
        global cap1
        global cap2
        global stad1
        global stad2
        teams = selection.split(" vs ")
        j1 = teams[0]
        j2 = teams[1]
        for i in range(len(df)):
            if df.at[i, "team"]==j1:
                st.write(f'{j1} ({df.at[i, "conference"]}-{(df.at[i, "div"]).upper()}) plays in {df.at[i, "city"]}, {df.at[i, "state"]} at the {df.at[i, "stadium"]} with capacity {df.at[i, "capacity"]:,}.')
                cap1 = df.at[i, "capacity"]
                stad1 = df.at[i, "stadium"]
            elif df.at[i, "team"]==j2:
                st.write(f'{j2} ({df.at[i, "conference"]}-{(df.at[i, "div"]).upper()}) plays in {df.at[i, "city"]}, {df.at[i, "state"]} at the {df.at[i, "stadium"]} with capacity {df.at[i, "capacity"]:,}.')
                cap2 = df.at[i, "capacity"]
                stad2 = df.at[i, "stadium"]
        #max cap
        if cap1 > cap2:
            st.write(f'{stad1} is the larger stadium.')
        else:
            st.write(f'{stad2} is the larger stadium.')

        return(st.write(f'Both stadiums together can hold {(cap1+cap2):,} people.'))

    rivalries(select_rivalry)
    def showonmap(placelist):
        # see http://fontawesome.io/icons/ for fancy icons
        center = [39.82852302607694, -98.57894326018148]  # The [lat, lon] of the center of the United States
        stadiumsmap = folium.Map(location = center, zoom_start=4) #Create the map object


        for i in range(len(placelist)):
            lat = placelist.at[i, "latitude"]
            lon = placelist.at[i, "longitude"]
            conf = placelist.at[i, 'conference']
            name = placelist.at[i, "stadium"]
            cap = placelist.at[i, "capacity"]
            t = placelist.at[i, "team"]

            if t == j1 or j2:
                if t == j1:
                    if cap1 > cap2:
                        icon = folium.Icon(icon= 'football-ball', prefix="fa", color='green')
                        folium.Marker(location=[lat, lon],
                                        tooltip= name,
                                        icon = icon).add_to(stadiumsmap)
                    else:
                        icon = folium.Icon(icon= 'football-ball', prefix="fa", color='gray')
                        folium.Marker(location=[lat, lon],
                                        tooltip= name,
                                        icon = icon).add_to(stadiumsmap)
                elif t == j2:
                    if cap2 > cap1:
                        icon = folium.Icon(icon= 'football-ball', prefix="fa", color='green')
                        folium.Marker(location=[lat, lon],
                                        tooltip= name,
                                        icon = icon).add_to(stadiumsmap)
                    else:
                        icon = folium.Icon(icon= 'football-ball', prefix="fa", color='gray')
                        folium.Marker(location=[lat, lon],
                                        tooltip= name,
                                        icon = icon).add_to(stadiumsmap)


        #Save the html file in the local directory
        filePath = os.getcwd() + "\\stadiumsmap.html"
        stadiumsmap.save(filePath)
        #webbrowser.open('file://' + filePath)

    def main():
        stadiums = df_stadiums
        showonmap(stadiums)


    main()

    st.header("Maps")

    HtmlFile = open("stadiumsmap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    print(source_code)
    components.html(source_code, height = 600)

    if cap1>cap2:
        st.write(f'The green pin represents {stad1} and the gray pin represents {stad2}')
    else:
        st.write(f'The green pin represents {stad2} and the gray pin represents {stad1}')









if st.button("Click this button to reset page and clear current selections"): #resets the page
    pyautogui.hotkey("ctrl","F5")


