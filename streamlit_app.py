    # Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)

name_on_order= st.text_input("Name On Smoothie:")
st.write('Name On Smoothie will be:',name_on_order)


#title = st.text_input('Movie title', 'Life of Brian')
#st.write('The current movie title is', title)

#option = st.selectbox(
#    'What is your favourite fruit?',
#    ('Banana', 'Strawberries', 'Peaches'))

#st.write('Your favorite fruite is:', option)
cnx=st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
)
if ingredients_list:
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen  in ingredients_list:
        ingredients_string+=fruit_chosen +' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_string)
    ##Build Statement to inset the values
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order,order_filled)
            values ('""" + ingredients_string + """','"""+name_on_order+"""',FALSE)"""

    st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


