import random

running = True
rules = "Jotto is a game in which two players will each guess\n" \
        "each other's word by guessing 5-letter english words.\n" \
        "After guessing a word, you are told how many of your\n" \
        "letters were in the opponent's word.  These are not\n" \
        "necessarily in order.  It is possible to get 5 letters\n" \
        "right without getting the word itself, if your guess\n" \
        "was an anagram of their word.  (For example, great/grate)\n" \
        "You will start by entering your chosen 5-letter english word."
botList = []
botEliminatedLetters = []
botConfirmedLetters = []

def main():
    print(rules)
    running = True
    getBotWords()
    playerWord = parsePlayerWord("My word: ")
    # Botto picks a random word
    botWord = pickWord()
    while running:
        # Turn loop
        playerGuess = parsePlayerWord("My guess: ")
        botGuess = pickWord()
        print("You: " + playerGuess + " : " + str(compareWords(playerGuess,botWord)))
        print("Bot: " + botGuess + " : " + str(compareWords(botGuess,playerWord)))
        if playerGuess == botWord:
            print("JOTTO!  You guessed Botto's word!")
            running = False
        if botGuess == playerWord:
            print("JOTTO!  Botto guessed your word!")
            running = False
    input("Press [ENTER] to play again.")
    main()


def getBotWords():
    # text file reading brought to you by:
    # https://stackoverflow.com/questions/3925614/how-do-you-read-a-file-into-a-list-in-python
    with open('wordList') as wordList:
        inList = wordList.read().splitlines()
    for word in inList:
        botList.append(word)
    print("Botto loaded " + str(len(botList)) + " words into their dictionary.")


def compareWords(wordA,wordB, botTurn = False):
    wordBList = []
    score = 0
    for letter in wordB:
        wordBList.append(letter)
    for letter in wordA:
        if letter in wordBList:
            score += 1
            wordBList.remove(letter)
    if(botTurn):
        botLogic(wordA,score)
    return score


def botLogic(word, score):
    wordLetters = []
    for letter in word:
        wordLetters.append(letter)
    if(score == 0):
        for letter in wordLetters:
            botEliminatedLetters.append(letter)
    for letter in botEliminatedLetters:
        if letter in wordLetters:
            wordLetters.remove(letter)


def parsePlayerWord(message):
    playerInput = str(input(message))
    if len(playerInput) != 5:
        print("Word must be exactly 5 letters long!")
        return parsePlayerWord(message)
    if not playerInput.isalpha():
        print("You can only use letters!")
        return parsePlayerWord(message)
    if not isValidWord():
        print("Word is not a recognized english word.")
        return parsePlayerWord(message)
    return playerInput.lower()


def pickWord():
    # TODO: Give bot smarter way to pick a word.
    print(len(botList))
    word = botList[random.randint(0, len(botList) - 1)]
    botList.remove(word)
    return word


def isValidWord():
    return True

main()