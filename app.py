import streamlit as st
import pandas as pd
import os
from aws_utils import upload_to_s3, fetch_receipts
from dotenv import load_dotenv
load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

st.title("📄 Receipt Automation with AWS")

with st.expander("📌 View Architecture Diagram"):
    st.image("Receipt Processing Pipeline with Streamlit and AWS.png", use_column_width=True)
    st.caption("This diagram shows how AWS services interact to automate receipt processing.")

st.subheader("Upload a Receipt")
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    if st.button("Upload to S3"):
        msg = upload_to_s3(uploaded_file, uploaded_file.name, S3_BUCKET)
        st.success(msg)
        st.success("Email notification sent.")

st.subheader("Processed Receipts")
if st.button("Fetch from DynamoDB"):
    data = fetch_receipts(DYNAMODB_TABLE)
    if data:
        df = pd.DataFrame(data)
        df["View Receipt"] = df["s3_url"].apply(lambda x: f"[Open]({x})")
        df = df.drop(columns=["s3_path", "s3_url"])
        st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)
    else:
        st.warning("No data found.")
