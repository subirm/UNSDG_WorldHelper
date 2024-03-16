# We're using tools and helpers to make our project work.
import datetime  # This helps us know the date and time.
import requests  # This is like sending letters or making phone calls over the internet.
import pytz  # This helps us with time zones, so we know the time anywhere in the world.
import streamlit as st  # This helps us make a webpage where we can fill out forms and show info.
import time  # This helps us with time, like waiting or knowing how long something takes.
import json  # This helps us read and write information in a special format that computers like.

from datetime import datetime as dt  # A special tool for dates and times.

from langchain.chains import LLMChain  # A chain that links our ideas together.
from langchain.prompts import PromptTemplate  # A template for asking questions in a smart way.
from langchain_openai import OpenAI  # A AI that can understand and write text.

event_id = None

# These are like secret codes and addresses we need to send our information to the right place.
eventbrite_org_id = st.secrets["eventbrite_org_id"]
eventbrite_auth_key = st.secrets["eventbrite_auth_key"]

# This is like putting a stamp and address on our internet letter so it gets to the right place.
create_event_url = f"https://www.eventbriteapi.com/v3/organizations/{eventbrite_org_id}/events/"
update_event_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
create_venue_url = f"https://www.eventbriteapi.com/v3/organizations/{eventbrite_org_id}/venues/"
publish_event_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/publish/"

headers = {
    'Authorization': f"Bearer {eventbrite_auth_key}", 
    'Accept': 'application/json',
    'Content-Type': 'application/json' 
}

# We're setting up a question to help us understand how our event helps the world.
template = """Question: What UN SDG goals does the description in Event_Description meet

Event_Description : {event_description}

Answer: Let's think step by step and list at most 3 goals in decreasing order of relevance to the description in Event_Description. Don't list any goals if the results are not relevant.
Just list the goal names and goal number in brackets as JSON. Do not provide and explanation"""

prompt = PromptTemplate.from_template(template)

# This is our AI assistant that helps us find out which world goals our event supports.
llm = OpenAI(openai_api_key=st.secrets["openai_api_key"],
            model='gpt-3.5-turbo-instruct')

llm_chain = LLMChain(prompt=prompt, llm=llm)

# This function tells us which world goals our event helps with.
def get_unsdg_goals_met(description:str):
    
    if description:    
        llm_output = llm_chain.run(description)
        final_message = None
        
        if llm_output: 
            # We take the AI assistant's answer and make it ready to show on our webpage.
            json_string = llm_output.split('\n\n', 1)[1]  # We find the part of the answer that's in a special format.
            
            final_message = f"Your event meets the following goals:\n {json_string}"

        return final_message

# This function helps us figure out the exact time of our event, no matter where it is in the world.
def get_date_time(event_day, event_time, event_tz):
    combined_datetime = dt.combine(event_day, event_time)
    timezone = pytz.timezone(event_tz)
    timezone_aware_dt = timezone.localize(combined_datetime)
    utc_dt = timezone_aware_dt.astimezone(pytz.utc)
    formatted_datetime = utc_dt.isoformat(timespec='seconds').replace('+00:00', 'Z')
    return formatted_datetime

# This function helps us set up where our event is going to be.
def create_venue(name:str, address:str, capacity:int = 25 ):
    if name and address:
        payload =   {
            "venue": {
              "name": name,
              "capacity": capacity,
              "address": {
                          "address_1": address
                          }
            }
        }
          
        response = requests.post(create_venue_url, json=payload, headers=headers)
        if response.status_code == 200:
            # If the internet letter gets a thumbs up, we know where our event will be.
            data = response.json()
            venue_id = data['id']
            return venue_id
        else:
            # If something goes wrong, we tell the user with a message.
            st.error(f'Error: {response.status_code}, {response.text}')
            return None

# This function helps us make tickets for our event.
def create_ticket_class(event_id, name):
    if event_id:
        create_ticketclass_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/ticket_classes/"
        payload =   {
                "ticket_class": {
                  "name": name,
                  "free": True,
                  "quantity_total": 25
                }
              }
        response = requests.post(create_ticketclass_url, json=payload, headers=headers)
        if response.status_code == 200:
            # If we get a thumbs up, the tickets are ready!
            return True
        else :
            # If something goes wrong, we don't make tickets.
            return False

# Here, we're setting up our webpage so it looks nice and people know what it's for.
st.set_page_config(page_title="Plan an event")

# This is where we start making our event page look nice and ask the user for details about their event.
st.markdown("# Plan an event \n")
st.markdown("""
**Plan an Event and find out which UN Sustainable Development Goals your event supports!**  
**We are so excited that you want to plan an event that supports the UNSDG.**

**Fill in the details below and click “Submit” to find out which UNSDG your event supports!**  
**You might be surprised and learn something new!**

""")
with st.sidebar:
    st.image("./assets/pippy.jpg", width=200)  # Show a picture on the side.
    st.write(
        "<h1>Hi, I'm <font color='#ffcdc2'>WorldHelper</font> - your personal UNSDG Helper</h1>",
        unsafe_allow_html=True,
    )
    st.sidebar.header("Plan an Event")

# We're making a list of all the time zones so the user can pick the right one for their event.
all_timezones = pytz.all_timezones

# We're making a special list of time zones for places in Canada.
canadian_cities = ['Toronto', 'Vancouver', 'Edmonton', 'Winnipeg', 'Montreal', 'Halifax', 'St_Johns','Regina', 'Yellowknife']
canada_timezones = [tz for tz in all_timezones if any(city in tz for city in canadian_cities)]

# This is where the user fills out the details about their event, like when it is and where.
with st.form("event_form", clear_on_submit=True):
    event_name = st.text_input('Name', help='Enter the name of the event')
    event_description = st.text_area('Description', help='What event do you want to plan that will support a UNSDG?')
    event_location = st.text_input('Event Location',  help='Enter the address where the event will be held')
    event_venue_details = st.text_input('Additional venue details',  help='Specify any additional information about the venue')
    event_date = st.date_input("When's your event", value=None)
    event_time_zone = st.selectbox('Timezone', canada_timezones, index=canada_timezones.index('America/Montreal'))
    event_start_time = st.time_input('What time will the event start', datetime.time(9, 0))
    event_end_time = st.time_input('What time will the event end', datetime.time(15, 0))

    # When the user is done filling out the form and presses the submit button, we start making their event happen.
    submit_button = st.form_submit_button("Submit")
    
    # If the user has filled everything out, we start putting their event together.
    if submit_button and event_name and event_description and event_location and event_date and event_time_zone and event_start_time and event_end_time:
        
        event_url = None
        event_venue_id = None
        
        # We start by setting up the venue.
        if eventbrite_org_id:
            event_venue_id = create_venue(name=event_name,address=event_location)
        
        # If we have a place for our event, we put all the details together.
        if event_venue_id:   
            payload = {
                    "event": {
                        "name": {
                            "html": event_name
                        },
                        "venue_id": event_venue_id ,
                        "start": {
                            "timezone": event_time_zone,
                            "utc": get_date_time(event_date, event_start_time, event_time_zone)
                        },
                        "end": {
                            "timezone": event_time_zone,
                            "utc": get_date_time(event_date, event_end_time, event_time_zone)
                        },
                        "description": {
                            "html": event_description
                        },
                        "currency": "CAD"
                    }
                }
            response = requests.post(create_event_url, json=payload, headers=headers)
        
            # If we successfully create the event, we get a webpage for it.
            if response.status_code == 200:
                data = response.json()
                event_url = data['url']
                event_id = data['id']

                # We make tickets for the event.
                if event_venue_id:
                    if create_ticket_class(event_id, f"{event_name}"):
                        with st.spinner('Creating event...'):
                            # We let everyone know the event is ready to go!
                            response = requests.post(f"https://www.eventbriteapi.com/v3/events/{event_id}/publish/", headers=headers)
                            if response.status_code == 200:    
                                st.write(f'Your event has been created; please go to {event_url} to check and share the event!')
                                st.warning("Please copy the link, it will not be available again and don't hesitate to contact us for any assistance", icon="⚠️")
                                # If our event supports world goals, we share that too!
                                if event_description:
                                    goals_met = get_unsdg_goals_met(event_description)
                                    if goals_met:
                                        st.write(goals_met.replace("{", "").replace("}", "").replace("\"","").replace("[","").replace("]",""))
            else:
                # If something goes wrong with creating the event, we let the user know.
                st.error(f'Error: {response.status_code}, {response.text}')
    elif submit_button:
        # If the user didn't fill everything out, we remind them to do so.
        st.error("Please fill in all required fields correctly.")
