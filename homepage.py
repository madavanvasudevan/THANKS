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

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title('THANKS-APP', anchor=None)


st.subheader("TH-Theomics")
st.subheader("AN-Analysis")
st.subheader("K-Kit")
st.subheader("S-For Science")
