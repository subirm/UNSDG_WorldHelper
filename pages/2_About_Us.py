import streamlit as st

# Team Members Information
team_members = [
    {"name": "\n\n Megan", "role": "Data Scientist", "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "profile_pic": "./assets/megan.jpg"},
    {"name": "\n\n Luna", "role": "Software Engineer", "bio": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "profile_pic": "./assets/luna.jpg"},
    {"name": "\n\n Vidya", "role": "UX Designer", "bio": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.", "profile_pic": "./assets/vidya.jpg"}
]

# Display Team Members
st.title("About Us")

for member in team_members:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(member["profile_pic"], width=200)
    
    with col2:
        st.subheader(member["name"])
        st.write(f"**Role:** {member['role']}")
        st.write(member["bio"])
