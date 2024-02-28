import streamlit as st

# Function to display team members
def display_team_members():
    # Team Members Information
    team_members = [
        {"name": "Megan", "role": "Team Leader", "bio": "Megan bio", "profile_pic": "./assets/megan.jpg"},
        {"name": "Luna", "role": "Design and Artwork", "bio": "Luna bio", "profile_pic": "./assets/luna.jpg"},
        {"name": "Vidya", "role": "Technology Lead", "bio": "Vidya bio", "profile_pic": "./assets/vidya.jpg"}
    ]

    # Display Team Members
    for member in team_members:
        col1, col2 = st.columns([1, 4])

        with col1:
            st.image(member["profile_pic"], width=200)

        with col2:
            st.subheader(member["name"])
            st.write(f"**Role:** {member['role']}")
            st.write(member["bio"])

# Main Page
def main_page():
    st.title("Team Cherry Blossoms")
    st.rerun()

    # Load the content for this specific page
    display_team_members()

# Display the main page
main_page()
