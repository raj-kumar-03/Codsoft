import streamlit as st

# Chatbot logic to respond based on name and age
def chatbot_response(user_name, user_age):
    if user_age < 18:
        return f"Hello, {user_name}! You're under 18. It's great to start learning early!"
    elif 18 <= user_age <= 25:
        return f"Hello, {user_name}! You're in the prime age group. Keep working hard and achieving your goals!"
    elif user_age > 25:
        return f"Hello, {user_name}! With more experience, you're likely making great strides in your journey!"

# Chatbot for general college-related queries
def college_queries(user_input):
    user_input = user_input.lower()
    if 'admission' in user_input:
        return "You can apply for admission through the official website."
    elif 'course' in user_input:
        return "We offer various courses. Check our academic department page."
    elif 'fees' in user_input:
        return "Visit our fee section for detailed information."
    elif 'campus' in user_input:
        return "The campus offers modern facilities like hostels and sports complexes."
    elif 'location' in user_input:
        return "We are located in Puducherry, India."
    else:
        return "I'm sorry, I didn't quite understand your question."

# Streamlit app layout
st.title("College Chatbot")
st.write("Hello! I'm your college assistant. Let's get to know you!")

# Ask for name and age
user_name = st.text_input("Enter your name:")
user_age = st.number_input("Enter your age:", min_value=0)

# If both inputs are provided, generate age-based response
if user_name and user_age:
    age_response = chatbot_response(user_name, user_age)
    st.write(age_response)

# Suggest input queries for the user
st.write("You can ask me about:")
st.write("- Admission process")
st.write("- Courses available")
st.write("- Fees information")
st.write("- Campus facilities")
st.write("- Location of the college")

# Handle general chatbot queries
user_input = st.text_input("Ask me anything about the college:")
if user_input:
    college_response = college_queries(user_input)
    st.write(f"Chatbot: {college_response}")
