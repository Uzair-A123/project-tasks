import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import tkinter as tk
from tkinter import ttk, messagebox

# FAQs dictionary with numbers
faqs = {
    1: ("What is the return policy?", "At ShopEase, our return policy allows for returns within 30 days of purchase, provided the item is in its original condition. To initiate a return, please contact ShopEase customer support or visit our returns page."),
    2: ("How do I track my order?", "You can track your order using the tracking link provided in the confirmation email. If you haven't received it, make sure to check your spam folder or visit ShopEase's 'Track Order' page with your order number."),
    3: ("What payment methods do you accept?", "ShopEase accepts multiple payment methods, including Visa, MasterCard, American Express, debit cards, PayPal, and Apple Pay. You can also use ShopEase gift cards and promotional codes at checkout."),
    4: ("Do you ship internationally?", "Yes, ShopEase ships to over 50 countries worldwide! International shipping times and rates vary depending on the destination. Please check ShopEase's shipping page for detailed information regarding your country."),
    5: ("Can I change my shipping address after placing an order?", "If your order hasn't shipped yet, you can change the shipping address by contacting ShopEase's customer service team. However, once the order is dispatched, no changes can be made."),
    6: ("Do you offer expedited shipping?", "Yes, ShopEase offers several shipping options, including standard, expedited, and next-day shipping. You can select your preferred option at checkout, and rates will be calculated based on your location."),
    7: ("What is your customer service contact?", "ShopEase's customer service team is available via phone at 1-800-123-4567 or email at support@shopease.com. You can also reach us through live chat on ShopEase's website for quick inquiries."),
    # Add more FAQs as needed
}

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Preprocess FAQ questions
def preprocess(text):
    doc = nlp(text.lower())  # Convert to lowercase and tokenize
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

processed_faqs = {num: preprocess(faq[0]) for num, faq in faqs.items()}

# Find the most similar FAQ question based on user input
def find_most_similar_question(user_input):
    user_input_preprocessed = preprocess(user_input)
    
    # Vectorize both user input and FAQ questions
    vectorizer = CountVectorizer().fit_transform(
        [user_input_preprocessed] + list(processed_faqs.values())
    )
    vectors = vectorizer.toarray()

    # Compute cosine similarity
    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])
    most_similar_index = cosine_similarities.argmax()

    return list(faqs.keys())[most_similar_index + 1], cosine_similarities[0][most_similar_index]

# Get chatbot response by FAQ number
def get_chatbot_response_by_number(question_number):
    if question_number in faqs:
        question, answer = faqs[question_number]
        return f"Q: {question}\nA: {answer}"
    else:
        return "Sorry, I didn't understand your choice. Please choose a number from the list."

# Get response for custom question input
def get_chatbot_response(user_input):
    question_number, similarity_score = find_most_similar_question(user_input)
    return get_chatbot_response_by_number(question_number)

# Create tkinter window
root = tk.Tk()
root.title("ShopEase FAQ Assistant")
root.geometry("600x400")

# Welcome message label
welcome_label = tk.Label(root, text="Welcome to ShopEase FAQ Assistant!", font=("Helvetica", 16))
welcome_label.pack(pady=10)

# Frame for the listbox and scrollbar
frame = tk.Frame(root)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Listbox with scrollbar
listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=80, height=10)
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

# Populate the Listbox with FAQ options
for num, (question, _) in faqs.items():
    listbox.insert(tk.END, f"{num}. {question}")

listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Custom question entry box
custom_question_label = tk.Label(root, text="Or, ask your own question:")
custom_question_label.pack(pady=5)
custom_question_entry = tk.Entry(root, width=60)
custom_question_entry.pack(pady=5)

# Function to handle user input
def handle_input():
    selected_index = listbox.curselection()
    if selected_index:
        question_number = int(listbox.get(selected_index).split('.')[0])
        response = get_chatbot_response_by_number(question_number)
        messagebox.showinfo("Response", response)
    
    elif custom_question_entry.get():
        user_input = custom_question_entry.get()
        response = get_chatbot_response(user_input)
        messagebox.showinfo("Response", response)
    
    else:
        messagebox.showwarning("Input Error", "Please select a question or ask your own.")

# Submit button
submit_button = tk.Button(root, text="Ask", command=handle_input)
submit_button.pack(pady=20)

# Run the tkinter event loop
root.mainloop()
