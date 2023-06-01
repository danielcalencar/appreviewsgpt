import mysql.connector
import openai

openai.api_key = 'API KEY'

# Establish MySQL connection
cnx = mysql.connector.connect(
    host='localhost',
    user='username',
    password='password',
    database='reviews'
)

# Function to retrieve reviews from the MySQL table based on user query
def retrieve_reviews_from_database(query):
    cursor = cnx.cursor()
    # Modify the SQL query based on your table structure
    sql_query = "SELECT * FROM product_reviews WHERE product_reviews LIKE '%{}%'".format(query)
    cursor.execute(sql_query)
    reviews = cursor.fetchall()
    cursor.close()
    return reviews

# Initialize chat messages
messages = [
    {"role": "system", "content": "You are an intelligent assistant."},
    {"role": "system", "content": "The following are some relevant product reviews:"},
    {"role": "assistant", "content": "Review 1: ..."},
    {"role": "assistant", "content": "Review 2: ..."},
    {"role": "assistant", "content": "Review 3: ..."},
]

Flag = True
# Conversation loop
while Flag:
    user_input = input("User: ")

    if user_input:
        # Append user query to messages
        messages.append({"role": "user", "content": user_input})

        # Retrieve reviews from the database based on user query
        reviews = retrieve_reviews_from_database(user_input)

        # Append review information to messages
        for review in reviews:
            messages.append({"role": "assistant", "content": review[0]})

        # Generate assistant reply using ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract assistant reply from response
        assistant_reply = response.choices[0].message.content

        # Display assistant reply
        print("ChatGPT: " + assistant_reply)

        # Append assistant reply to messages
        messages.append({"role": "assistant", "content": assistant_reply})
        Flag = False

# Close the MySQL connection
cnx.close()
