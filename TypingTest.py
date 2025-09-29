import time
import random

# List of sentences for the typing game
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Python programming is fun and educational.",
    "Practice makes perfect.",
    "Typing games improve your typing speed.",
    "Stay focused and keep typing.",
    "Coding challenges help you learn new skills.",
    "Consistency is key to improvement.",
    "Challenge yourself every day.",
    "Never give up on learning.",
    "The journey of a thousand miles begins with a single step.",
    "Success is not final, failure is not fatal.",
    "It is the courage to continue that counts.",
    "Keep pushing forward no matter what.",
    "Believe in yourself and all that you are.",
    "Know that there is something inside you that is greater than any obstacle.",
    "Start where you are. Use what you have. Do what you can.",
    "Act as if what you do makes a difference. It does.",
    "Your limitation—it’s only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Sometimes later becomes never. Do it now.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn’t just find you. You have to go out and get it.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don’t stop when you’re tired. Stop when you’re done."
]

def typing_game():
    sentence = random.choice(sentences)
    print("Type the following sentence as quickly and accurately as possible:")
    input("Press Enter to start...")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("\n" + sentence + "\n")
    
    start_time = time.time()
    user_input = input("Start typing: ")
    end_time = time.time()
    
    time_taken = end_time - start_time
    time_taken_minutes = time_taken / 60
    accuracy = len([i for i in range(len(sentence)) if i < len(user_input) and sentence[i] == user_input[i]]) / len(sentence) * 100
    
    word_count = len(sentence.split())
    wpm = word_count / time_taken_minutes
    
    print("\nTime taken: {:.2f} seconds".format(time_taken))
    print("Accuracy: {:.2f}%".format(accuracy))
    print("Words per minute (WPM): {:.2f}".format(wpm))
    input()

if __name__ == "__main__":
    typing_game()
