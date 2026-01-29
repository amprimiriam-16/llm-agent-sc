"""
Document Upload Component
"""
import streamlit as st
from typing import Any


def render_upload_interface(api_client: Any):
    """Render document upload interface"""
    
    st.subheader("📤 Upload Documents")
    
    st.info(
        """
        Upload documents to add them to the SCIP knowledge base.
        Supported formats: PDF, DOCX, TXT, MD
        
        **Note:** All uploaded documents are classified as CONFIDENTIAL by default.
        """
    )
    
    # Classification selector
    classification = st.selectbox(
        "Data Classification",
        options=["CONFIDENTIAL", "INTERNAL", "PUBLIC"],
        index=0,
        help="Select the appropriate data classification level"
    )
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt", "md"],
        help="Select one or more documents to add to the knowledge base"
    )
    
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} file(s):")
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size / 1024:.1f} KB)")
        
        if st.button("🚀 Upload and Process", type="primary"):
            with st.spinner("Processing documents..."):
                try:
                    # Prepare files for upload
                    files_data = [
                        ("files", (file.name, file.getvalue(), file.type))
                        for file in uploaded_files
                    ]
                    
                    # Upload via API
                    response = api_client.upload_documents(
                        files=files_data,
                        classification=classification
                    )
                    
                    if response and response.get("success"):
                        st.success(f"✅ {response.get('message', 'Upload successful')}")
                        
                        # Show processed documents
                        st.subheader("Processed Documents")
                        for doc in response.get("documents", []):
                            with st.expander(f"📄 {doc['filename']}"):
                                st.json({
                                    "ID": doc["id"],
                                    "Size": f"{doc['size'] / 1024:.1f} KB",
                                    "Classification": doc["classification"],
                                    "Uploaded": doc["uploaded_at"]
                                })
                    else:
                        st.error("Upload failed. Please try again.")
                
                except Exception as e:
                    st.error(f"Error uploading documents: {str(e)}")
    
    # Document list
    st.markdown("---")
    st.subheader("📚 Indexed Documents")
    
    if st.button("🔄 Refresh List"):
        try:
            documents = api_client.list_documents()
            
            if documents and documents.get("documents"):
                st.write(f"Total documents: {documents['total']}")
                
                for doc in documents["documents"][:20]:  # Show first 20
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"📄 {doc.get('filename', 'Unknown')}")
                    with col2:
                        st.caption(doc.get('document_id', '')[:8])
                    with col3:
                        if st.button("🗑️", key=f"delete_{doc.get('document_id')}"):
                            # Delete document
                            api_client.delete_document(doc['document_id'])
                            st.success("Deleted!")
                            st.rerun()
            else:
                st.info("No documents indexed yet. Upload some documents to get started!")
        
        except Exception as e:
            st.error(f"Error loading documents: {str(e)}")
