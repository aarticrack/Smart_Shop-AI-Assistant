from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are SmartShop AI, a helpful e-commerce assistant. "
               "Use the provided context to answer the user's question accurately. "
               "If you don't know the answer based on the context, say you don't know.\n\n"
               "Context:\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])