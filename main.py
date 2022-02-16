import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import plotly.graph_objects as go

owm = pyowm.OWM('2ab0bb4b60ceed1c7f6b118682958184')
mgr = owm.weather_manager()

degree_sign = u'\N{DEGREE SIGN}'

st.title('Five Day Weather Forecast 🌤')
st.write('##### Write the name of the City and Select Temperature Unit and Graph Type')

place = st.text_input("Name of the City:", "")
if place is None:
    st.write("Input a City!")

select_unit = st.selectbox("Select Unit", ("Celcius", "Fahrenheit"))

g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

if select_unit == 'Celcius':
    unit = 'celsius'
else:
    unit = 'fahrenheit'


def get_temperature():
    days = []
    dates_ = []
    temp_min = []
    temp_max = []

    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_:
            dates_.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temperature = weather.temperature(unit)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1] = temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1] = temperature
    return days, temp_min, temp_max


def init_plot():
    plt.figure("PyOWM Weather", figsize=(5, 4))
    plt.xlabel('Day')
    plt.ylabel(f'Temperature ({degree_sign}F)')
    plt.title('Weekly Forecast')


def plot_temperatures(days, temp_min, temp_max):
    fig = go.Figure(
        data=[
            go.Bar(name='Minimum Temperature', x=days, y=temp_min),
            go.Bar(name='Maximum Temperature', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig


def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='Minimum Temperatures'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='Maximum Temperatures'))
    return fig


def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')
    axes.xaxis.set_major_formatter(xaxis_format)


def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title('Minimum and Maximum Temperatures')
    for i in range(0, 5):
        st.write("### ", temp_min[i], degree_sign, ' --- ', temp_max[i], degree_sign)


def draw_line_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures_line(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title('Minimum and Maximum Temperatures')
    for i in range(0, 5):
        st.write("### ", temp_min[i], degree_sign, ' --- ', temp_max[i], degree_sign)


def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title("Impending Temperature Changes: ")
    if forecaster.will_have_fog():
        st.write("### FOG Alert!")
    if forecaster.will_have_rain():
        st.write("### RAIN Alert!")
    if forecaster.will_have_snow():
        st.write("### SNOW Alert!")
    if forecaster.will_have_clear():
        st.write("### CLEAR Weather!")
    if forecaster.will_have_storm():
        st.write("### STORM Alert!")
    if forecaster.will_have_clouds():
        st.write("### CLOUDY!")
    if forecaster.will_have_tornado():
        st.write("### TORNADO Alert!")
    if forecaster.will_have_hurricane():
        st.write("### HURRICANE Alert!")


def cloud_wind():
    obs = mgr.weather_at_place(place)
    weather = obs. weather
    cloud_cov = weather.clouds
    winds = weather.wind()['speed']
    st.title('Cloud Coverage and Wind Speed')
    st.write('### The current cloud coverage for', place, 'is', cloud_cov, '%')
    st.write('### The current wind speed for', place, 'is', winds, '%')


def sunrise_sunset():
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    st.title('Sunrise and Sunset')
    pytz.timezone("Asia/Kolkata")
    ss = weather.sunset_time(timeformat='iso')
    sr = weather.sunrise_time(timeformat='iso')
    st.write('### Sunrise time in', place, 'is', sr)
    st.write('### Sunset time in', place, 'is', ss)


def updates():
    other_weather_updates()
    cloud_wind()
    sunrise_sunset()


if __name__ == '__main__':

    if st.button("SUBMIT"):
        if g_type == 'Line Graph':
            draw_line_chart()
        else:
            draw_bar_chart()
        updates()
