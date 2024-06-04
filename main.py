# BASIC






import streamlit as st
import vanna
from vanna.remote import VannaDefault
import pandas as pd
import io
import base64

# Streamlit app title
st.title("VannaDefault Query App")

# Input for API key
api_key = st.text_input("Enter your Vanna API Key:", type="default")

# Input for user question
user_question = st.text_input("Enter your question:")

# Function to handle the button click event
def run_query():
    if api_key and user_question:
        try:
            # Show "Thinking" message
            with st.spinner('Thinking...'):
                # Connect to Vanna with the provided API key
                vn = VannaDefault(model='chinook', api_key=vanna.get_api_key(api_key))
                vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')

                # Ask the question and display the result
                response = vn.ask(user_question)
                st.write("Response:")
                st.write(response)


                # Generate SQL query and run it
                sql = vn.generate_sql(user_question)
                df = vn.run_sql(sql)

                # Display the resulting dataframe
                st.write("Table:")
                st.dataframe(df)

                # Add option to download the dataframe as CSV
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings
                href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Generate plotly code and create plot chart
                plotly_code = vn.generate_plotly_code(question=user_question, sql=sql, df=df)
                fig = vn.get_plotly_figure(plotly_code=plotly_code, df=df)

                

                # Display the plot chart
                st.write("Chart:")
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Button to run the query
if st.button('Run Query'):
    run_query()
