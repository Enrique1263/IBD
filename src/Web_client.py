
import streamlit as st
from sentence_transformers import SentenceTransformer
import pymilvus


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
pymilvus.connections.connect("default", host="milvus-standalone", port="19530")
collection = pymilvus.Collection(name="articles")


# Web page configuration ---------------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Article Search Engine", page_icon="🔍", initial_sidebar_state="expanded")


# Define your code here
def articles_from_text(input_text, model_for_query):

    # Get the embedding of the input text
    query_embedding = model_for_query.encode(input_text)

    limit = 10
    # load the collection

    res = collection.search(
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {}},
        data=[query_embedding.tolist()],
        limit=limit, # Max. number of search results to return
        output_fields=["url","title", "description", "source"], # Fields to return in the search results
    )


    results = res[0]

    # Print the search results in teh streamlit app
    st.write("## Search Results")
    for r in results:
        data = r
        print(data)
        print('\n\n')
        title = data.get('title')
        description = data.get('description')
        source = data.get('source')
        url = data.get('url')

        # embed the url into the title
        st.write(f"### [{title}]({url})")
        st.write(f"###### {description}")
        st.write(f"Source: {source}")
        st.write('\n\n')
        st.write('---')
        



# Streamlit app
def main():


    st.write("## Enter a descprition to find news articles")
    # Get user input
    input_text = st.text_input("Enter text")

    # Execute code when button is clicked
    if st.button("Execute", key="text"):
        
        articles_from_text(input_text, model)
        





# Run the app
if __name__ == "__main__":
    main()