import requests
import streamlit as st

#We have mode the following value to config.py and imported it there
FASTAPI_URL = "http://localhost:8000"

st.title("🧭 AI Problem Solving Assistant")
st.markdown("Ask about question on uploaded document - we'll find the best suggestions for you!")

# Sidebar for File Upload
with st.sidebar:
    st.subheader("📁 Upload Document that you have query")
    uploaded_file = st.file_uploader("Upload a PDF formatted document (optional)", type="pdf")

    if uploaded_file:
        if st.button("Process Study Guide"):
            with st.spinner("Processing the uploaded document..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(f"{FASTAPI_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(f"Error: {response.json().get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error uploading file: {str(e)}")

# Main content
st.subheader("❓ Ask Your Question")
query = st.text_input("Enter your question related to uploaded document:(For example What is Artificial Intelligence)")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{FASTAPI_URL}/ask", json={"query": query})
                if response.status_code == 200:
                    answer = response.json()["response"]
                    st.success("Here’s your suggested answer:")
                    st.write(answer)
                else:
                    st.error("Server error! Try again later.")
            except Exception as e:
                st.error(f"Could not reach the FastAPI server: {e}")
    else:
        st.warning("Please enter a query.")
