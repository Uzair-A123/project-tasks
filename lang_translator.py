from googletrans import Translator, LANGUAGES
import sys

# Initialize the Translator
translator = Translator()

# Function to detect the language of the input text
def detect_language(text):
    try:
        detected = translator.detect(text)
        lang_code = detected.lang
        lang_name = LANGUAGES.get(lang_code, 'Unknown')
        return lang_code, lang_name
    except Exception as e:
        return None, str(e)

# Function to translate text from detected language to target language
def translate_text(text, target_language):
    try:
        # Detect the input language
        lang_code, lang_name = detect_language(text)
        if lang_code is None:
            return f"Error detecting language: {lang_name}"
        
        # Translate the text
        translation = translator.translate(text, src=lang_code, dest=target_language)
        translated_text = translation.text
        return translated_text, lang_name
    except Exception as e:
        return str(e), None

# Function to display available languages
def display_languages():
    print("Available languages and their codes:\n")
    for lang_code, lang_name in LANGUAGES.items():
        print(f"{lang_name.capitalize()} ({lang_code})")
    print("\n")

# Main function to handle user input and output
def main():
    # Display available languages
    display_languages()

    # Get the target language from the user
    target_language = input("Enter the target language code: ").strip().lower()
    if target_language not in LANGUAGES:
        print(f"Error: Unsupported language code '{target_language}'. Exiting.")
        sys.exit(1)

    # Loop to translate multiple inputs
    while True:
        text = input("\nEnter text to translate (or type 'exit' to quit): ").strip()
        if text.lower() == 'exit':
            print("Exiting the program.")
            break

        # Translate the text
        translated_text, detected_language = translate_text(text, target_language)
        
        if detected_language is None:
            print(f"Error: {translated_text}")
        else:
            print(f"Detected language: {detected_language}")
            print(f"Translated text: {translated_text}")

# Entry point of the script
if __name__ == "__main__":
    main()
