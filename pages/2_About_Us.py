import streamlit as st

# Team Members Information
team_members = [
    {"name": "Megan", "role": "Data Scientist", "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "profile_pic": "./assets/megan.jpg"},
    {"name": "Luna", "role": "Software Engineer", "bio": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "profile_pic": "./assets/luna.jpg"},
    {"name": "Vidya", "role": "UX Designer", "bio": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.", "profile_pic": "./assets/vidya.jpg"}
]

# Display Team Members
st.title("About Us")

st.write("""World Helper is an app that helps communities make the world a
better place. This app helps you learn about the UN Sustainable
Development Goals. It also helps you plan events that support the
UN Sustainable Development Goals. \n 
World Helper was created by Megan, Vidya, and Luna. We are
three friends who attend Osler Elementary School in Vancouver,
Canada. This is our second Technovation project. We each have
had a special role to play in creating World Helper. Megan is head
of organization; Vidya leads on the technology side; and Luna
brings our artwork to life.\n\n""")

st.write("\n\n\n\n")

for member in team_members:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(member["profile_pic"], width=200)
    
    with col2:
        st.write("\n")
        st.markdown(f"<h4>{member['name']}</h4>", unsafe_allow_html=True)  # Adjust the header size here
        st.write(f"**Role:** {member['role']}")
        st.write(member["bio"])
