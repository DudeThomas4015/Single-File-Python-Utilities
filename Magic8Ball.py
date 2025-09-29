import random

def magic_8_ball():
    responses = [
        "Yes, definitely.",
        "It is certain.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]

    question = input("Ask the Magic 8 Ball a question: ")
    print("Shaking the Magic 8 Ball...\n")
    answer = random.choice(responses)
    print(f"Magic 8 Ball says: {answer}")
    input()

if __name__ == "__main__":
    magic_8_ball()
