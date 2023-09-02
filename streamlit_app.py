import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avacado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display results
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
#new section
try :
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a food to get information.")
    streamlit.write('The user entered ', fruit_choice)
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/ + fruit_choice")
    # take the jason version of form and normailze it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # output in table form
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("My fruit load list contains:")
streamlit.dataframe(my_data_rows)

#second section
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice1 = streamlit.text_input('Any other fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice1)

fruityvice_response1 = requests.get("https://fruityvice.com/api/fruit/apple")

# take the jason version of form and normailze it
fruityvice_normalized1 = pandas.json_normalize(fruityvice_response1.json())
# output in table form
streamlit.dataframe(fruityvice_normalized1)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")



  
