import streamlit as st
import pandas as pd

st.title('My Mom\'s New Healthy Diner')

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

# New Section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
info_fruit = st.text_input("What fruit would you like information about?", "Kiwi")
st.write('The user entered', info_fruit)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+info_fruit)
# st.text(fruityvice_response.json()) # just writes the data to the screen

# take the json version of the response and normalize it 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output it the screen as a table
st.dataframe(fruityvice_normalized)

# set up Streamlit to work with snowflake
import snowflake.connector

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

# All the end user to add  a fruit to the list
add_my_fruit = st.text_input("What fruit would you like to add?", "jackfruit")
st.write('Thanks for adding', add_my_fruit)
