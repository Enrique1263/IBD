
import streamlit as st


# Web page configuration ---------------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Avatar Generator")


model_for_query = None
client = None
# Define your code here
def articles_from_text(input_text, model_for_query, client):
    # Example: Print the input text
    print("You have written:", input_text)
    '''
    embedded_vector = model_for_query.embedd_texts([input_text])

    limit = 5
    

    res = client.search(
        collection_name="news", # Replace with the actual name of your collection
        # Replace with your query vector
        data=embedded_vector,
        limit=limit, # Max. number of search results to return
        search_params={"metric_type": "COSINE", "params": {}}, # Search parameters
        output_fields=["url", "title"] # Output fields
    )
    '''
    #write an example of the search results to test

    res = [
        {
            "title": "Example title 1",
            "url": "https://example.com/1"
        },
        {
            "title": "Example title 2",
            "url": "https://example.com/2"
        },
        {
            "title": "Example title 3",
            "url": "https://example.com/3"
        }
    ]




    # Print the search results in teh streamlit app
    st.write("### Search Results")
    for i, r in enumerate(res):
        st.write(f"### {r['title']}")
        st.write(f"{r['url']}")
        st.write("---------------------------------------------------")



# Streamlit app
def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)


    st.write("## Enter a descprition to find the most similar images")
    # Get user input
    input_text = st.text_input("Enter text")

    # Execute code when button is clicked
    if st.button("Execute", key="text"):
        
        articles_from_text(input_text, model_for_query, client)
        st.write("You have written:", input_text)





# Run the app
if __name__ == "__main__":
    main()