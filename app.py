import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

st.title("Motor vehicles collisions in New York")
st.markdown("##### This application is an interactive streamlit dashboard")

DATA_URL = "/Users/primeschool/Documents/vs and shit/ml/Motor_Vehicle_Collisions_-_Crashes.csv"

@st.cache_data(persist = True)

def load_data(nrows):
    
    # nrows parameter is used to specify the number of rows to read from the CSV file. This can be useful if you only want to read a subset of the data, rather than the entire file.
    # parse_dates parameter is a dictionary that specifies that the first two columns of the CSV file (specified by [0, 1]) should be parsed as a single datetime column called 'date/time'.
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates={'date/time': [0, 1]})
    
    # dropping any rows that contain missing values (also known as NaN values) in the columns 'LATITUDE' or 'LONGITUDE'
    # The 'subset' parameter is used to specify the columns that should be checked for missing values.
    data.dropna(subset = ['LATITUDE', 'LONGITUDE'], inplace = True)
    
    # fuction that converts its argument into lowercase
    lowercase = lambda x: str(x).lower()
    
    # axis='columns' parameter is used to specify that the renaming should be performed on the columns (as opposed to the rows).
    data.rename(lowercase, axis='columns', inplace=True)
    
    # renaming column name
    data.rename(columns = {'crash_date_crash_time' : 'date/time'}, inplace = True)
    
    # returning the modified data dataframe
    return data

# passing 100000 rows as an argument
data = load_data(100000)

original_data = data

st.header('Where are the most people injured in NYC?')

# declaring a variable and assigning it a slider with values ranging from 0 - 19
injured_people = st.slider('Number of persons injured in collisions', 1, 19)

# renaming the column name, setting inplace = true so the change in dataframe is permanent
# data.rename(columns = {'number of persons injured' : 'injured_persons'}, inplace = True)

# data.query() is being used to filter the rows of the DataFrame to include only those where the number of injured persons >= value of injured_people
# The resulting DataFrame is then subsetted to include only the 'latitude' and 'longitude' columns, which are the columns needed for the scatterplot.
st.map(data.query("`number of persons injured` >= @injured_people")[['latitude', 'longitude']].dropna(how= 'any'))


# Display a header in the Streamlit app
st.header('How many collisions occur during a given time in a day?')

# Create a slider for selecting an hour of the day and store the selected hour in the `hour` variable
hour = st.slider('Hour to look at', 0, 23)

# Filter the `data` dataset to include only rows with the selected hour
data = data[data['date/time'].dt.hour == hour]

# Compute the number of rows in the filtered dataset and display it in a Markdown block
num_rows = data.shape[0]
st.markdown('##### Vehicle collisions between %i:00 and %i:00: %i' % (hour, (hour + 1) % 24, num_rows))

# Compute the midpoint of the latitude and longitude coordinates in the filtered dataset and display it on a map
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = {  
        'latitude': 40.720,
        'longitude': -73.890,
        'zoom': 10.8,
        'pitch': 50,              
    }, 
    layers = [
        pdk.Layer(
        "HexagonLayer",
        data = data[['date/time', 'longitude', 'latitude']],
        get_position = ['longitude', 'latitude'],
        radius = 100,
        extruded = True,
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0, 1000],
        ),
    ],
))

# Set subheader for display with formatted string showing hour range
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))

# Filter data to include only rows where hour is within the range of the current hour and the next hour
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour+1))
]

# Calculate the frequency distribution of minutes within the hour using numpy histogram function
hist = np.histogram(filtered['date/time'].dt.minute, bins = 60, range=(0, 60))[0]

#Create a pandas DataFrame with minute and corresponding crashes count for plotting
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})

# Create a bar plot using plotly express with minute and crashes count as x and y axis, and minute and crashes count as hover_data
# Set plot height to 400 pixels
fig = px.bar(chart_data, x='minute', y='crashes', hover_data = ['minute', 'crashes'], height = 400)

# Write plot to Streamlit app
st.write(fig)

st.header('Top 5 dangerous streets by affected type')

select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'pedestrians':
    st.write(original_data.query('`number of pedestrians injured` > 1')[['on street name', 'number of pedestrians injured']].sort_values(by = ['number of pedestrians injured'], ascending = False).dropna(how = 'any')[:5])

elif select == 'Cyclists':
    st.write(original_data.query('`number of cyclist injured` > 1')[['on street name', 'number of cyclist injured']].sort_values(by = ['number of cyclist injured'], ascending = False).dropna(how = 'any')[:5])
    
else:
    st.write(original_data.query('`number of motorist injured` > 1')[['on street name', 'number of motorist injured']].sort_values(by = ['number of motorist injured'], ascending = False).dropna(how = 'any')[:5])

if st.checkbox('Show raw data', False):
    st.subheader('Raw Data')
    st.write(data)
