from flask import render_template
import re
import logging
import random
from datetime import datetime, timedelta
from flask import request

# In-memory storage for user interactions
user_interactions = {}

# Global variable to track the first message after server restart
first_message_received = False

synonym_map = {'bot buddy': 'BotBuddy'}

def preprocess_query(query):
    for word in synonym_map:
        query = query.replace(word, synonym_map[word])
    return query

def append_campaign(response):
    campaign_link = "https://botbuddy.gitbook.io/botbuddy-docs/affiliate-program-bot-airdrop"
    if 'affiliate program' in response  and campaign_link not in response:
        response += "\nLearn more about the BotBuddy Affiliate Program by visiting: " + campaign_link
    return response 

def append_how_to_buy_info(query, response):
    how_to_buy_link = "https://botbuddy.gitbook.io/botbuddy-docs/tokenomics-usdbot"
    buy_keywords = ["how can i buy bot", "where to purchase bot", "how can i buy $bot", "where can i buy bot", "where can i buy $bot", "where to purchase $bot"] # only kw in lower case

    additional_info = "\nVisit " + how_to_buy_link + " for all the details regarding the BOT token"

    if any(keyword in query.lower() for keyword in buy_keywords) and how_to_buy_link not in response:
        response += additional_info

    return response

def append_proposal_info(query, response):
    proposal_email = "proposal@botbuddy.co"
    proposal_keywords = ["marketing proposal", "listing proposal", "commercial proposal", "partnership proposal"]

    additional_info = "For proposals, please email: " + proposal_email

    if any(keyword in query.lower() for keyword in proposal_keywords) and proposal_email not in response:
        response += additional_info

    return response

def check_greeting(query):
    global first_message_received
    greetings = ['hi', 'hello', 'hey', 'greetings']
    if query.lower() in greetings and not first_message_received:
        first_message_received = True
        return '''Hi! 👋
I'm Leo, the BotBuddy's AI Assistant ready to answer to every your question regarding BotBuddy and the upcoming $BOT token!

Feel free to explore all my features and ask me anything!
I'm here to make your learning experience as enjoyable as possible! 😃

How may I assist you today?'''
    else:
        return None

def check_developer(query):
    ask_dev = ['do you need developer', 'looking for developer', 'do you need a developer']
    if query.lower() in ask_dev:
        return '''You are welcome to send your CV to cv@botbuddy.co. Our team will contact you if there's room for further discussion.'''
    else:
        return None

def check_for_airdrop_request(query):
    airdrop_phrases = ["Wen airdrop", "When airdrop", "wen IDO", "when IDO", "wen TGE", "when TGE"]
    if query.lower() in airdrop_phrases:
        return '''The TGE and related Airdrop of the $BOT token will happen on Q2. You can find more detailed information by visiting https://botbuddy.gitbook.io/botbuddy-docs/tokenomics-usdbot.'''
    else:
        return None

def filter_bot_response(response_text):
    # Define the phrases that trigger the replacement
    trigger_phrases = ["I am not able", "Upon further request", "The article does not", "Based on the information provided, it is not", "This information is not provided", "It is unclear", "Based on the given context, it can", "I do not know", "It is likely", "Unfortunately", "I don't know", "It is not explicitly", "I'm sorry"]

    for phrase in trigger_phrases:
        if phrase in response_text:
            # Replace the response with one of the predefined answers
            replacement_responses = [
                "I didn't get it very well. Could you rephrase the question?",
                "Please repeat the question with more details, so I can understand better!",
                "Sorry but I didn't understand what you mean at first attempt. Could you rephrase the question adding more details?"
            ]
            # Randomly select one of the replacement responses
            replacement = random.choice(replacement_responses)
            return replacement

    return response_text  # Return the original response if no trigger phrase is found

def check_user_message_limit():
    # Attempt to get the user's original IP address from the X-Forwarded-For header
    if 'X-Forwarded-For' in request.headers:
        user_ip = request.headers['X-Forwarded-For'].split(',')[0]  # Take the first IP from the list
    else:
        user_ip = request.remote_addr  # Fallback if the header is not present

    current_time = datetime.now()
    max_messages_reached_message = "You have reached the maximum number of messages allowed in 24 hours."

    if user_ip not in user_interactions:
        user_interactions[user_ip] = [current_time]
        return True, ""  # The user can proceed, no error message required

    valid_times = [time for time in user_interactions[user_ip] if current_time - time <= timedelta(hours=24)]
    user_interactions[user_ip] = valid_times  # Keep only the valid interactions

    if len(valid_times) >= 7:
        return False, max_messages_reached_message  # Limit reached, return false with a message
    else:
        user_interactions[user_ip].append(current_time)  # Record new interaction time
        return True, ""  # The user can proceed, no error message required
