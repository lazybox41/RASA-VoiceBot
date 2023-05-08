# rasa modules
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from typing import Any, Text, Dict, List

# modules for supporting API calls
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser as web
import requests


# song actions


class ActionCheckSong(Action):
    def name(self) -> Text:
        return "action_check_song"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check song method")
        user_input = tracker.latest_message.get("text")
        return [SlotSet("song_name", user_input)]


class ActionConfirmSong(Action):
    def name(self) -> Text:

        return "action_confirm_song"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)
        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_spotify_api")]


class ActionCallSpotifyAPI(Action):
    def name(self) -> Text:
        return "action_call_spotify_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_input = tracker.get_slot("song_name")
        print(user_input)

        client_id = "b98db0c89cf143a7bba3370cf13b2b96"
        client_secret = "eef5b8588cee4e06b2166da5795e3b2f"
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Search for the song and artist on Spotify
        query = "track:{}".format(user_input)
        result = spotify.search(q=query)

        # Get the Spotify URI of the first track in the search results
        track_uri = result["tracks"]["items"][0]["uri"]
        web.open(track_uri)

        # Send a message to the user confirming that the song is playing
        message = "Playing {} on Spotify".format(user_input)
        dispatcher.utter_message(text=message)

        return []


# map actions


class ActionCheckLocation(Action):
    def name(self) -> Text:
        return "action_check_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check location method")
        user_input = tracker.latest_message.get("text")
        return [SlotSet("location_name", user_input)]


class ActionConfirmLocation(Action):
    def name(self) -> Text:
        return "action_confirm_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)

        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_maps_api")]


class ActionCallMapsAPI(Action):
    def name(self) -> Text:
        return "action_call_maps_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_choice = tracker.get_slot("location_name")
        print(f"Now calling the Maps API to find the location {user_choice}")
        dispatcher.utter_message(f"Here are the directions to {user_choice}")
        url = (
            "https://www.google.com/maps/dir/?api=1&origin=pune&destination="
            + user_choice
        )
        web.open(url)

        return []


# contacts


class ActionConfirmContact(Action):
    def name(self) -> Text:
        return "action_confirm_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)
        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_contacts_api")]


class ActionCheckContact(Action):
    def name(self) -> Text:
        return "action_check_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check contact method")
        user_input = tracker.latest_message.get("text")
        return [SlotSet("contact_name", user_input)]


class ActionCallContactsAPI(Action):
    def name(self) -> Text:
        return "action_call_contacts_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_choice = tracker.get_slot("contact_name")
        print(f"Now calling the Contacts API to call the person {user_choice}")
        dispatcher.utter_message(
            f"Now calling the Contacts API to call the person {user_choice}"
        )
        return []


# weather actions


class ActionCheckWeatherLocation(Action):
    def name(self) -> Text:
        return "action_check_weather_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check weather location method")
        user_input = tracker.latest_message.get("text")
        return [SlotSet("weather_location_name", user_input)]


class ActionConfirmWeatherLocation(Action):
    def name(self) -> Text:
        return "action_confirm_weather_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)

        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_weather_api")]
        else:
            print("API not called")


class ActionCallWeatherAPI(Action):
    def name(self) -> Text:
        return "action_call_weather_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        api_key = "da562f52746c4e6687e61904230705"
        location = tracker.get_slot("weather_location_name")
        # API endpoint for current weather
        current_url = (
            f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        )

        # Send a GET request to the API and get the response
        response = requests.get(current_url)

        # Check if the response was successful
        if response.status_code == 200:
            # Parse the JSON response to get the weather data
            data = response.json()

            # Extract the relevant weather information for current weather
            current_description = data["current"]["condition"]["text"]
            current_temperature = data["current"]["temp_c"]
            current_humidity = data["current"]["humidity"]
            current_wind_speed = data["current"]["wind_kph"]

            # Print the current weather information
            print(f"The current weather in {location} is {current_description}.")
            print(f"The temperature is {current_temperature} Celsius.")
            print(f"The humidity is {current_humidity}%.")
            print(f"The wind speed is {current_wind_speed} kph.")

        else:
            # Handle errors
            print(f"Error {response.status_code}: {response.text}")

        # API endpoint for weather forecast for next day
        forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=2"

        # Send a GET request to the API and get the response
        response = requests.get(forecast_url)

        # Check if the response was successful
        if response.status_code == 200:
            # Parse the JSON response to get the forecast data
            data = response.json()

            # Extract the relevant weather information for next day
            forecast_description = data["forecast"]["forecastday"][1]["day"][
                "condition"
            ]["text"]
            forecast_temperature = data["forecast"]["forecastday"][1]["day"][
                "avgtemp_c"
            ]
            forecast_humidity = data["forecast"]["forecastday"][1]["day"]["avghumidity"]
            forecast_wind_speed = data["forecast"]["forecastday"][1]["day"][
                "maxwind_kph"
            ]

            # Print the forecast weather information
            print(
                f"\nThe weather forecast for tomorrow in {location} is {forecast_description}."
            )
            print(f"The average temperature is {forecast_temperature} Celsius.")
            print(f"The average humidity is {forecast_humidity}%.")
            print(f"The maximum wind speed is {forecast_wind_speed} kph.")

        else:
            # Handle errors
            print(f"Error {response.status_code}: {response.text}")

        dispatcher.utter_message(
            text=f"The weather forecast for tomorrow in {location} is {forecast_description}. The average temperature is {forecast_temperature} Celsius. The average humidity is {forecast_humidity}%."
        )
        return []
