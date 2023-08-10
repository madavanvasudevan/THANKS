import streamlit as st
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: cover;
}}
[data-testid="stSidebar"] > div:first-child {{
background-color: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=200 height=150></p>",unsafe_allow_html=True)
