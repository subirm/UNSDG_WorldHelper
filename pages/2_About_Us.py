import streamlit as st

# Team Members Information
team_members = [
    {"name": "John Doe", "role": "Data Scientist", "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "profile_pic": "./assets/megan.jpg"},
    {"name": "Jane Smith", "role": "Software Engineer", "bio": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "profile_pic": "./assets/luna.jpg"},
    {"name": "Alice Johnson", "role": "UX Designer", "bio": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.", "profile_pic": "./assets/vidya.jpg"}
]

# Display Team Members
st.title("About Us")

for member in team_members:
    st.subheader(member["name"])
    st.image(member["profile_pic"], width=200)
    st.write(f"**Role:** {member['role']}")
    st.write(member["bio"])
