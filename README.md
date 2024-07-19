# AI Assistant for Website

## Overview
The AI Assistant for Website is a Flask-based application integrated with OpenAI APIs, providing an interactive chatbot experience. This project demonstrates the ability to create a full-stack application, including a backend developed with Python and Flask, and a dynamic frontend using HTML, CSS, and JavaScript. The chatbot leverages advanced AI functionalities to engage users with intelligent responses based on their queries.

## Technical Features

### Backend
- **Flask Application**: Utilized Flask, a lightweight WSGI web application framework, to handle HTTP requests and serve dynamic content. 
- **OpenAI API Integration**: Integrated OpenAI’s powerful language models to generate responses, ensuring the chatbot can handle complex queries with contextually appropriate answers.
- **Vector Search with Qdrant**: Implemented a vector search mechanism using Qdrant, which optimizes the retrieval of relevant information from a corpus of text, enhancing the chatbot's ability to provide accurate answers.
- **Custom Middleware Functions**: Developed middleware to preprocess user queries and manage response content, demonstrating capabilities in crafting efficient data processing pipelines.
- **Rate Limiting and User Session Management**: Applied rate limiting to manage request frequency and used in-memory storage to track user interactions, showcasing skills in developing robust and scalable applications.

### Frontend
- **Interactive Chat Interface**: Built an interactive user interface with HTML, CSS, and JavaScript, providing users with a seamless and engaging interaction experience.
- **JavaScript Enhancements**: Implemented AJAX calls for dynamic data fetching without reloading the webpage, improving user experience with asynchronous JavaScript.
- **CSS for Responsive Design**: Crafted a responsive design using CSS, ensuring the application is accessible and visually appealing across different devices and screen sizes.

### Deployment
- **Replit Hosting**: Deployed the application on Replit, demonstrating familiarity with cloud-based hosting environments and continuous deployment practices.

## Skills Demonstrated
- **Python Programming**: Proficient in Python, with a focus on backend development using Flask.
- **Frontend Development**: Skills in HTML, CSS, and JavaScript, capable of building and styling interactive web interfaces.
- **API Integration**: Experienced in integrating and utilizing third-party APIs, specifically OpenAI, to enhance application functionalities.
- **Data Handling**: Ability to handle and process data efficiently, evident from the implementation of custom middleware and integration with vector databases.
- **Problem Solving**: Strong problem-solving skills, capable of designing solutions to complex software requirements.

## Setup and Installation
To set up and run the BotBuddy AI Assistant locally, follow these steps:

### Prerequisites
- Python 3.8 or higher
- pip for Python package installation
- An active internet connection for accessing external APIs

### Installation Steps
1. **Clone the Repository:**
   ```
   git clone https://github.com/yourusername/botbuddy.git
   cd botbuddy
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   You'll need to set up the following environment variables:
   - `QDRANT_HOST`
   - `QDRANT_API_KEY`
   - `QDRANT_COLLECTION`
   - `OPENAI_API_KEY`
   
   These can be set in your shell or through a `.env` file using a library like `python-dotenv`.

4. **Initialize the Database:**
   Run the Python script provided in the repository to set up your Qdrant vector database with the necessary configuration.

5. **Run the Application:**
   ```
   python main.py
   ```
   This will start the Flask server on `http://localhost:8080`.

6. **Accessing the Web Interface:**
   Open your browser and navigate to `http://localhost:8080` to interact with the AI assistant.

## Author
- [Ricasco](https://github.com/ricasco) - Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/your-linkedin)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
