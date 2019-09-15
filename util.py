import random
import lyrics
import keys
import requests

subscription_key = keys.SUB_KEY
endpoint = keys.ENDPOINT
sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"
keyphrase_url = endpoint + "/text/analytics/v2.1/keyphrases"
headers = {"Ocp-Apim-Subscription-Key": subscription_key}

class MessageHandler():
    """Processes the messages sent by the user."""

    def __init__(self, message):
        """Inits a new MessageHandler"""
        self.message = message
        self.sentiment = self.get_sentiment()
        print(self.sentiment)
        self.key_phrases = self.get_key_phrases()
        print(self.key_phrases)

    def get_sentiment(self):
        """Get the sentiment of the message."""
        documents = {'documents': [{'id':1, 'language':'en', 'text': self.message}]}
        response = requests.post(sentiment_url, headers=headers, json=documents)
        sentiments = response.json()
        return sentiments['documents'][0]['score']

    def get_key_phrases(self):
        """Get the key phrases of the message."""
        documents = {'documents': [{'id':1, 'language':'en', 'text': self.message}]}
        response = requests.post(keyphrase_url, headers=headers, json=documents)
        key_phrases = response.json()
        return [s.lower() for s in key_phrases['documents'][0]['keyPhrases']]

    def yes_or_no_q(self):
        """Returns whether or not the message posed was a yes or not question that was personal."""
        content = self.message.lower().split()[0]
        try:
            return content in ['should','will','can','is','would']
        except IndexError:
            print('index error in yes_or_no_q')
            return False

    def sad(self):
        """Returns whether or not the given sentence has a sad sentiment."""
        return self.get_sentiment() < 0.3

    def waterloo(self):
        """Returns whether or not waterloo is related to the given sentence."""
        words = ['waterloo', 'hackathon', 'north', 'hacker']
        return any([word in self.key_phrases for word in words])
    
    def why_what(self):
        """Returns whether or not the question is a why or what statement."""
        content = self.message.lower().split()[0]
        try:
            return content in ['what','why','how']
        except IndexError:
            print('index error in why_what')
            return False

    def love_related(self):
        """Returns whether or not the question is related to romance."""
        words = ['love','lover','affection','sexy','loving','romance','romantic']
        return any([word in self.key_phrases for word in words])

    def money_related(self):
        """Returns whether or not the question is related to money."""
        words = ['money','wealth','cash','rich','salary','income','tax','taxes','taxation','richer']
        return any([word in self.key_phrases for word in words])       

    def return_output(self):
        """Returns the output of abba bot!"""
        phrases = set({})
        if self.yes_or_no_q():
            phrases = set.union(phrases, lyrics.yes_or_no_personal)
            print('yes_or_no_q')
        if self.why_what():
            phrases = set.union(phrases, lyrics.why_what)  
            print('why_what')
        if self.waterloo():
            phrases = set.union(phrases, lyrics.waterloo)
            print('waterloo')
        if self.love_related():
            phrases = set.union(phrases, lyrics.love)
            print('love_related')
        if self.money_related():
            phrases = set.union(phrases, lyrics.money)
            print('money_related')

        if self.sad() and phrases==set({}):
            phrases = set.union(phrases, lyrics.sad)
            print('sad')

        if phrases==set({}):
            phrases = lyrics.default

        li = list(phrases)
        random.shuffle(li)
        return li[0]