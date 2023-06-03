from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted
from rasa_sdk.events import ActionExecutionRejected
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from rasa_sdk.events import SlotSet

df = pd.read_csv("tmdb_5000_movies.csv")
valid_genres = ["action","comedy" ,"thriller" ,"family" , "adventure", "drama","horror","romance","animation","children","fantasy","crime","mystery","sci fi","scifi","sci-fi","western","documentary","war", "musical"]


class DisplayGenres(Action):

    def name(self) -> Text:
        return "action_display_genres"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Union[Text, Dict[Text, Any]]]]:

        init_genres = tracker.get_slot('genres')
        genres = []

        for i in range(len(init_genres)):
            if init_genres[i].lower() in valid_genres:
                genres.append(init_genres[i].lower())
                
        if genres:
            dispatcher.utter_message(f"The genres you selected are: {', '.join([genre.title() for genre in genres])}")
        else:
            dispatcher.utter_message("You have not selected any genres yet.")
        return []


class SearchMovie(Action):

    def name(self) -> Text:
        return "action_search_movie"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Union[Text, Dict[Text, Any]]]]:


        init_genres = tracker.get_slot('genres')
        genres = []

        for i in range(len(init_genres)):
            if init_genres[i].lower() in valid_genres:
                genres.append(init_genres[i].lower())



        if len(genres) == 1:
            mask = df['genres'].str.contains(genres[0].title())
        elif len(genres) == 2:
            mask = df['genres'].str.contains(genres[0].title()) & df['genres'].str.contains(genres[1].title()) 
        elif len(genres) == 3:
            mask = df['genres'].str.contains(genres[0].title()) & df['genres'].str.contains(genres[1].title()) & df['genres'].str.contains(genres[2].title())
        elif len(genres) == 4:
            mask = df['genres'].str.contains(genres[0].title()) & df['genres'].str.contains(genres[1].title()) & df['genres'].str.contains(genres[2].title()) & df['genres'].str.contains(genres[3].title())
        elif len(genres) == 5:
            mask = df['genres'].str.contains(genres[0].title()) & df['genres'].str.contains(genres[1].title()) & df['genres'].str.contains(genres[2].title()) & df['genres'].str.contains(genres[3].title()) & df['genres'].str.contains(genres[4].title())
        elif len(genres) > 5:
            dispatcher.utter_message("More than 5 genres selected!")
        else:
            dispatcher.utter_message("NO genre specified")



        # Finding the best movie
        try:
            search_result1 = df[mask].sort_values(by='popularity', ascending=False).iloc[0]
            dispatcher.utter_message("There you go")
            dispatcher.utter_message(  f"Name: {search_result1['original_title']}\n"
                    f"Overview: {search_result1['overview']}\n"
                    )

        except:
            dispatcher.utter_message("Could not find the best movie with current selection of genres. Please try again. \n")


            
        return []




class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Conversation restarted")


        # Reset the conversation tracker to its initial state
        return [Restarted()]
    

class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="I am having difficulty understanding you. Can you please rephrase your message?")



