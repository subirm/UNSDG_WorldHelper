# First, we're getting our tool ready. It's like opening your box of crayons before you start drawing.
import streamlit as st

# Here, we're setting up our drawing board, giving it a name so everyone knows it's about Team Cherry Blossoms.
st.set_page_config(page_title="Team Cherry Blossoms")

# We're deciding to put a special picture on the side of our drawing board. It's like sticking a sticker on the side of your notebook.
with st.sidebar:
    st.image("./assets/pippy.jpg", width=200)  # Showing a cool picture on the side.

# Now, we're making a list of our team, like writing down the names of your friends who helped you with a big school project.
team_members = [
    {"name": "Megan", "role": "Team Leader", "bio": "Megan bio", "profile_pic": "./assets/megan.jpg"},  # Megan is the team captain!
    {"name": "Luna", "role": "Design and Artwork", "bio": "Luna bio", "profile_pic": "./assets/luna.jpg"},  # Luna makes things look pretty.
    {"name": "Vidya", "role": "Technology Lead", "bio": "Vidya bio", "profile_pic": "./assets/vidya.jpg"}  # Vidya is the tech wizard.
]

# Now, we're writing a little story about our app, like the introduction to a  book.
st.write("""World Helper is an app that helps communities make the world a
better place. This app helps you learn about the UN Sustainable
Development Goals. It also helps you plan events that support the
UN Sustainable Development Goals. \n 
World Helper was created by Megan, Vidya, and Luna. We are
three friends who attend Osler Elementary School in Vancouver,
Canada. This is our second Technovation project. We each have
had a special role to play in creating World Helper. Megan is the team leader; Vidya leads on the technology side, and Luna
brings our artwork to life.\n\n""")

# Adding some space to make our page look nice, like when you skip a line before starting a new paragraph.
st.write("\n\n\n\n")

# Now, we're going to show off our team, like putting pictures of everyone on a poster board for a school project.
for member in team_members:
    col1, col2 = st.columns([1, 2])  # We're splitting our poster board into two parts: one for pictures and one for words.
    
    with col1:
        st.image(member["profile_pic"], width=200)  # Showing a picture of each team member.
    
    with col2:
        st.write("\n")  # Skipping a line to make things look neat.
        st.markdown(f"<h4>{member['name']}</h4>", unsafe_allow_html=True)  # Writing their name in big letters.
        st.write(f"**Role:** {member['role']}")  # Telling everyone what they do in the team.
        st.write(member["bio"])  # Sharing a little story about them.
        st.write("\n\n")  # Skipping some lines to make our poster board look nice and organized.
