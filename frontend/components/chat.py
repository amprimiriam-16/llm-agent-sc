"""
Chat Interface Component
"""
import streamlit as st
from typing import Any
import time


def render_chat_interface(
    api_client: Any,
    use_agentic: bool,
    max_sources: int,
    temperature: float
):
    """Render the chat interface"""
    
    # Chat container
    st.subheader("💬 Ask Questions")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source {i}: {source['source']}</strong><br>
                            Score: {source['score']:.3f}<br>
                            <em>{source['content'][:200]}...</em>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Show reasoning if available
            if message["role"] == "assistant" and "reasoning" in message and message["reasoning"]:
                with st.expander("🧠 Agent Reasoning"):
                    st.markdown(message["reasoning"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about supply chain, procurement, logistics..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    start_time = time.time()
                    
                    response = api_client.ask_question(
                        question=prompt,
                        use_agentic=use_agentic,
                        max_sources=max_sources,
                        temperature=temperature,
                        conversation_id=st.session_state.conversation_id
                    )
                    
                    elapsed_time = time.time() - start_time
                    
                    if response and "answer" in response:
                        # Display answer
                        st.markdown(response["answer"])
                        
                        # Show metadata
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.caption(f"⏱️ {elapsed_time:.2f}s")
                        with col2:
                            st.caption(f"📄 {len(response.get('sources', []))} sources")
                        with col3:
                            st.caption(f"🤖 {response.get('model_used', 'GPT-4')}")
                        
                        # Store conversation ID
                        st.session_state.conversation_id = response.get("conversation_id")
                        
                        # Add assistant message to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["answer"],
                            "sources": response.get("sources", []),
                            "reasoning": response.get("agent_reasoning")
                        })
                        
                        # Show sources
                        if response.get("sources"):
                            with st.expander("📚 View Sources"):
                                for i, source in enumerate(response["sources"], 1):
                                    st.markdown(f"""
                                    <div class="source-card">
                                        <strong>Source {i}: {source['source']}</strong><br>
                                        Score: {source['score']:.3f}<br>
                                        <em>{source['content'][:200]}...</em>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Show reasoning if available
                        if response.get("agent_reasoning"):
                            with st.expander("🧠 Agent Reasoning"):
                                st.markdown(response["agent_reasoning"])
                    
                    else:
                        st.error("Failed to get response from API")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Clear conversation button
    if st.session_state.messages:
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.rerun()
