import streamlit as st

# Team Members Information
team_members = [
    {"name": "Megan", "role": "Data Scientist", "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "profile_pic": "./assets/megan.jpg"},
    {"name": "Luna", "role": "Software Engineer", "bio": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "profile_pic": "./assets/luna.jpg"},
    {"name": "Vidya", "role": "UX Designer", "bio": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.", "profile_pic": "./assets/vidya.jpg"}
]

# Display Team Members
st.title("About Us")

for member in team_members:
    with st.beta_container():
        st.image(member["profile_pic"], width=200)
        st.subheader(member["name"])
        st.write(f"**Role:** {member['role']}")
        st.write(member["bio"])
