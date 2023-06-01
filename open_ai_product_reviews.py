import openai
import mysql.connector

# Step 3: Connect to your MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='username',
    password='password',
    database='reviews'
)

# Step 4: Query the database to retrieve the product reviews
db_cursor = db_connection.cursor()
db_cursor.execute("SELECT * FROM product_reviews")
reviews = db_cursor.fetchall()

# Step 5: Set up your OpenAI API credentials
openai.api_key = 'API KEY'


# Step 6: Define a function to send the user query to ChatGPT and get the response
def get_chatgpt_response(query):
    response = openai.Completion.create(
        engine="davinci",
        prompt=query,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()


# Step 7: Interactive loop
print("Welcome! Ask your questions about the app reviews!")
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # Analyze each review using ChatGPT
    for review in reviews:
        review_text = review[0]
        print("Review:", review_text)
        query = user_input + " " + review_text
        response = get_chatgpt_response(query)
        print("ChatGPT Analysis:", response)
        print()

# Close the database connection
db_cursor.close()
db_connection.close()
