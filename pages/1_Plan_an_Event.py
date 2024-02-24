import datetime
import requests
import pytz
import streamlit as st
import time
import json

from datetime import datetime as dt

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

event_id = None

eventbrite_org_id = st.secrets["eventbrite_org_id"]
eventbrite_auth_key = st.secrets["eventbrite_auth_key"]
create_event_url = f"https://www.eventbriteapi.com/v3/organizations/{eventbrite_org_id}/events/"
update_event_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
create_venue_url = f"https://www.eventbriteapi.com/v3/organizations/{eventbrite_org_id}/venues/"
publish_event_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/publish/"

headers = {
    'Authorization': f"Bearer {eventbrite_auth_key}", 
    'Accept': 'application/json',
    'Content-Type': 'application/json' 
    }


template = """Question: What UN SDG goals does the description in Event_Description meet

Event_Description : {event_description}

Answer: Let's think step by step and list at most 3 goals in decreasing order of relevance to the description in Event_Description. Don't list any goals if the results are not relevant.
Just list the  goal names and goal number in brackets as JSON. Do not provide and explanation"""

prompt = PromptTemplate.from_template(template)

llm = OpenAI(openai_api_key=st.secrets["openai_api_key"],
            model='gpt-3.5-turbo-instruct')

llm_chain = LLMChain(prompt=prompt, llm=llm)


def get_unsdg_goals_met(description:str):
    
    if description:    
        llm_output = llm_chain.run(description)
        final_message = None
        
        if llm_output: 

            # Extracting the JSON part of the string
            json_string = llm_output.split('\n\n', 1)[1]  # Get the JSON part after the first '\n\n'
            
            final_message = f"Your event meets the following goals:\n {json_string}"

        return final_message



def get_date_time(event_day, event_time, event_tz):
    combined_datetime = dt.combine(event_day, event_time)
    timezone = pytz.timezone(event_tz)
    timezone_aware_dt = timezone.localize(combined_datetime)
    utc_dt = timezone_aware_dt.astimezone(pytz.utc)
    formatted_datetime = utc_dt.isoformat(timespec='seconds').replace('+00:00', 'Z')
    return formatted_datetime

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
            # Process a successful response
            data = response.json()
            venue_id = data['id']
            return venue_id
        else:
            # Handle HTTP errors (e.g., client or server errors)
            st.error(f'Error: {response.status_code}, {response.text}')
            return None

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
            return True
        else :
            return False


st.set_page_config(page_title="Plan an event", page_icon="📈")

st.markdown("# Plan an event")
with st.sidebar:
    st.image("./assets/pippy.png", width=50)
    st.write(
        "<h1>Hi, I'm <font color='#ffcdc2'>WorldHelper</font> - your personal UNSDG Helper</h1>",
        unsafe_allow_html=True,
    )
    st.sidebar.header("Plan an Event")

all_timezones = pytz.all_timezones

# Filter for Canadian timezones
all_timezones = pytz.all_timezones

# Filter for Canadian time zones by major cities/regions
canadian_cities = ['Toronto', 'Vancouver', 'Edmonton', 'Winnipeg', 'Montreal', 'Halifax', 'St_Johns','Regina', 'Yellowknife']
canada_timezones = [tz for tz in all_timezones if any(city in tz for city in canadian_cities)]



with st.form("event_form", clear_on_submit=True):
    event_name = st.text_input('Name', help='Enter the name of the event')
    event_description = st.text_area('Description', help='What event do you want to plan that will support a UNSDG?')
    event_location = st.text_input('Event Location',  help='Enter the address where the event will be held')
    event_venue_details = st.text_input('Additional venue details',  help='Specify any additional information about the venue')
    event_date = st.date_input("When's your event", value=None)
    event_time_zone = st.selectbox('Timezone', canada_timezones, index=canada_timezones.index('America/Montreal'))
    event_start_time = st.time_input('What time will the event start', datetime.time(9, 0))
    event_end_time = st.time_input('What time will the event end', datetime.time(15, 0))

     
    submit_button = st.form_submit_button("Submit")
    

    if submit_button and event_name and event_description and event_location and event_date and event_time_zone and event_start_time and event_end_time :
        
        event_url = None
        event_venue_id = None
        
        if eventbrite_org_id:
            event_venue_id = create_venue(name=event_name,address=event_location)
        
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
        
            if response.status_code == 200:
                # Process a successful response
                data = response.json()
                event_url = data['url']
                event_id = data['id']

                if event_venue_id:
                    if create_ticket_class(event_id, f"venue_{event_name}"):
                        with st.spinner('Creating event...'):
                            response = requests.post(f"https://www.eventbriteapi.com/v3/events/{event_id}/publish/", headers=headers)
                            # publish the event
                            if response.status_code == 200:    
                                st.write(f'Your event has been created; please go to {event_url} to check and share the event!')
                                st.warning("Please copy the link, it will not be available again and don't hesitate to contact us for any assistance", icon="⚠️")
                                if event_description:
                                    goals_met = get_unsdg_goals_met(event_description)
                                    if goals_met:
                                        st.write(goals_met.replace("{", "").replace("}", "").replace("\"","").replace("[","").replace("]",""))
            else:
                # Handle HTTP errors (e.g., client or server errors)
                st.error(f'Error: {response.status_code}, {response.text}')
            

        
    elif submit_button:
        st.error("Please fill in all required fields correctly.")
