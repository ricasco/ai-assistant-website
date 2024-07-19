from flask import Flask, render_template, request, jsonify
import os
import qdrant_client
from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import re
import logging
import random
from functions import preprocess_query, append_campaign, check_greeting, check_developer, check_for_airdrop_request, append_how_to_buy_info, append_proposal_info, filter_bot_response, check_user_message_limit

# Configure basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Flask(__name__)

# Global variable to track the first message after server restart
first_message_received = False

# Environment variables set in Repl's Secrets
QDRANT_HOST = os.environ['QDRANT_HOST']
QDRANT_API_KEY = os.environ['QDRANT_API_KEY']
QDRANT_COLLECTION = os.environ['QDRANT_COLLECTION']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Create Qdrant client and collection
client = qdrant_client.QdrantClient(os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))
collection_config = qdrant_client.http.models.VectorParams(size=1536, distance=qdrant_client.http.models.Distance.COSINE)
client.recreate_collection(collection_name=os.getenv("QDRANT_COLLECTION"), vectors_config=collection_config)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Qdrant(client=client, collection_name=os.getenv("QDRANT_COLLECTION"), embeddings=embeddings)

# Add documents to your vector database
def get_chunks(text):
    separator = "\n\n"
    qna_pairs = text.split(separator)
    chunks = [pair for pair in qna_pairs if pair]
    return chunks

with open("botbuddy.txt") as f:
    raw_text = f.read()
texts = get_chunks(raw_text)
vectorstore.add_texts(texts)

# Instantiate the ChatOpenAI object with the gpt-4-turbo-preview model
llm = ChatOpenAI(model="gpt-4-turbo-preview")

# Use this llm object when setting up the RetrievalQA
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

# Flask routes
@app.route('/')
def index():
    welcome_message = "Welcome 👋 <br>I'm Leo, the AI Web Assistant of BotBuddy!<br><br>Ask me anything you want about BotBuddy in the language you prefer 🇬🇧🇨🇳🇪🇸🇮🇳🇷🇺🇺🇦🇦🇪🇫🇷🇯🇵🇩🇪🇹🇷🇰🇷🇮🇱🌍"
    return render_template('index.html', welcome_message=welcome_message)

KEYWORDS = [
    "BotBuddy", "Bot Buddy", "Co-founder", "CEO", "CTO", "Solidity", "Developer", "Advisor", "Web3", "Community Assistant", "Website Widget", "Telegram", "Discord", "tokenomics", "TGE", "$BOT", "Control Panel", "Coingecko", "spam", "security", "multi-language", "bot points", "Airdrop", "Galxe", "cold emailing", "KOL", "campaign", "Centralized Exchanges", "CEX", "blockchain integrations", "AI Software House", "Trading Bot", "DAO", "DeFi", "dApp", "GameFi", "Web2", "SME", "docs", "Medium", "Announcements", "Twitter", "LinkedIn", "email", "roadmap", "DEX", "Affiliate Program", "affiliates", "AI", "Widget", "affiliate", "affiliate program"
]

def contains_keyword(text):
  return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

# Example usage within the Flask route:
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = preprocess_query(data['query'])

    # Log the received query
    logging.info(f"Received query: {query_text}")

    # Here, we check if the user has exceeded the message limit
    can_send_message, rate_limit_message = check_user_message_limit()
    if not can_send_message:
        logging.info(f"Rate limit exceeded for user")
        return jsonify({'message': rate_limit_message})

    # Check if the query is a greeting
    greeting_response = check_greeting(query_text)
    if greeting_response:
        # Log the greeting response
        logging.info(f"Greeting response: {greeting_response}")
        return jsonify({'message': greeting_response})  

    # Check if the query is for dev
    ask_dev_response = check_developer(query_text)
    if ask_dev_response:
        # Log the greeting response
        logging.info(f"AskDev response: {ask_dev_response}")
        return jsonify({'message': ask_dev_response})  

    # Check if the query is for airdrop
    airdrop_phrases_response = check_for_airdrop_request(query_text)
    if airdrop_phrases_response:
        # Log the greeting response
        logging.info(f"airdrop_phrases response: {airdrop_phrases_response}")
        return jsonify({'message': airdrop_phrases_response})  

    # Retrieve the functions' response
    response = qa.invoke(query_text)  
    response_text = response.get('result', '')

    # Call append_otc_info function with the response text
    response_text = append_campaign(response_text)

    # Call append_how_to_buy_info function
    response_text = append_how_to_buy_info(query_text, response_text)

    # Call append_how_to_buy_info function
    response_text = append_proposal_info(query_text, response_text)

    # Now use response_text for further processing
    bot_response = response_text

    # Check for special responses and replace if needed
    bot_response = filter_bot_response(bot_response)

    # Check for keywords in both the query and the response
    if not contains_keyword(query_text) and not contains_keyword(bot_response):
        # Select one of the preset messages randomly
        preset_messages = [
            "I'm trained to answer only questions related to BotBuddy and the upcoming $BOT token. So I would like to respond you but then my boss will fire me, and I can't lose this job",
            "Sorry, I can only discuss topics about BotBuddy and the upcoming $BOT token because I'm trained on them. So if you wanna talk with me, now you know my favourite topics :D",
            "Please ask me something related to BotBuddy and the upcoming $BOT token! I'm not your personal Wikipedia!"
        ]
        bot_response = random.choice(preset_messages)

    # Log the final response
    logging.info(f"Bot response: {response}")

    return jsonify({'message': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)