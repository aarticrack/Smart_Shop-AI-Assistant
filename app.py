import streamlit as st
import requests
import uuid

st.set_page_config(page_title="SmartShop AI", layout="wide")

# 1. Generated a unique session ID for history 
# This ID is crucial for the Backend...
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🛒 SmartShop AI Assistant")
st.subheader("Your Intelligent E-commerce Partner")

# 2. Initializing chat history for the UI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can help you find products across Electronics, Furniture, Kitchen, and more. What are you looking for?"}
    ]

# 3. Displayed chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User input and Chat Logic
if prompt := st.chat_input("Ask about a product, budget, or specifications..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Displayed user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Calling FastAPI Backend with session_id for Multi-Turn support
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # For a "thinking" feel
        message_placeholder.markdown("Searching the catalog...")
        
        try:
            # The backend uses 'session_id' to retrieve previous context (e.g., Furniture vs Laptops)
            response = requests.post(
                "http://localhost:8000/api/v1/chat",
                json={
                    "message": prompt, 
                    "session_id": st.session_state.session_id
                },
                #timeout=30 # Extended timeout for LLM extraction + RAG
            )
            
            if response.status_code == 200:
                answer = response.json().get("answer", "I found some information, but couldn't format it correctly.")
                message_placeholder.markdown(answer)
                
                # Adding assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"Backend Issue: Received Status {response.status_code}"
                st.error(error_msg)
                message_placeholder.empty()
                
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Is your FastAPI server (main.py) running on port 8000?")
            message_placeholder.empty()
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            message_placeholder.empty()