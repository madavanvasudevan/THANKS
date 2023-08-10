import streamlit as st

st.set_page_config(layout="wide")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img1.wsimg.com/isteam/stock/DjDe1rQ/:/rs=w:767,m");
background-size: cover;
}}
[data-testid="stHeader"] {{
background-color: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
  st.title("**TH**eomics **AN**alytics **K**it **S**cience")
  # st.subheader("<span style='font-size: 42px;'>**TH**</span>eomics <span style='font-size: 42px;'>**AN**</span>alytics <span style='font-size: 42px;'>**K**</span>it <span style='font-size: 42px;'>**S**</span>cience", unsafe_allow_html=True)
with col2:
  # URL of the image from the web
  image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"
  
  # Display the image using Streamlit's image function
  st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)


