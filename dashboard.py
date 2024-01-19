import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.title("AI Fact Checker")
st.image("ai_graphic.png")
st.write("**About the tool:**")
st.write("Welcome to the AI Fact Checker Tool! This powerful tool is designed to identify potential fake and misinformation news circulating on the X platform (formerly known as Twitter). Gain insights into the veracity of news stories, backed by accurate sources and referenced text extracted from the collective knowledge within the Twitter community notes.")

st.write("**What are Community Notes?**")
st.write('''
            Community Notes aim to create a better informed world by empowering people on X to collaboratively add context to potentially misleading posts. 
            Contributors can leave notes on any post and if enough contributors from different points of view rate that note as helpful, the note will be publicly shown on a post.
        ''')

# The connection string, database name, and collection name
connection_string = "mongodb+srv://" + st.secrets["DB_USERNAME"] + ":" + st.secrets["DB_PASSWORD"] + "@" + st.secrets["DB_CLUSTER"] + ".actfwm5.mongodb.net/"
database_name = st.secrets["DB_NAME"]
collection_name = st.secrets["DB_COLLECTION"]

# Create a MongoClient
client = MongoClient(connection_string)

# Access the specified database and collection
db = client[database_name]
collection = db[collection_name]

# Count the number of documents in the collection
document_count = collection.count_documents({})

# Print the result
st.write("*Number of potential fake news in the Database: " + str(document_count) + "*")



# Query to get the last 50 documents
last_50_documents = collection.find().sort("_id", -1).limit(50)

st.header("Top recent 50 Fake News :point_down:")
# Convert the query result to a list of dictionaries
documents_list = list(last_50_documents)
for fc_no, document in enumerate(documents_list, 1):
    st.divider()
    st.subheader("False News No. " + str(fc_no))
    if document['verified'] == True:
        verified_status = ":ballot_box_with_check:"
    else:
        verified_status = ""
    st.write("**Name:** " + document['name'] + " *(" + document['username'] + ")* " + verified_status)
    profile_link = "https://twitter.com/" + document['username']
    st.write("**User Profile Link:** " + profile_link)
    st.write("**Date**: " + document['datetime'].strftime("%d-%m-%Y"))
    st.write("**Claim:** :x: " + document['tweet'])
    st.write("**Reality:** :heavy_check_mark: " + document['reality'])
    st.write("**Sources:**")
    for count, source in enumerate(document['source'], 1):
        st.markdown(f"{count}. [{source}]({document['source_link'][count-1]})")
    st.write("**Tweet Link:** " + document['tweet_link'])

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(documents_list)

# Print or use the DataFrame as needed
st.write(df)