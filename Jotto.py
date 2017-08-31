import random

debug = False
rules = "Jotto is a game in which two players will each guess\n" \
        "each other's word by guessing 5-letter english words.\n" \
        "After guessing a word, you are told how many of your\n" \
        "letters were in the opponent's word.  These are not\n" \
        "necessarily in order.  It is possible to get 5 letters\n" \
        "right without getting the word itself, if your guess\n" \
        "was an anagram of their word.  (For example, great/grate)\n" \
        "You will start by entering your chosen 5-letter english word."
botList = []
wordBank = []
botEliminatedLetters = []
botConfirmedLetters = []
botGuesses = {}

def main():
    print(rules)
    global debug
    debug = False
    botEliminatedLetters.clear()
    botConfirmedLetters.clear()
    botGuesses.clear()
    running = True
    getBotWords()
    playerWord = parsePlayerWord("My word: ")
    # Botto picks a random word
    botWord = pickWord()
    while running:
        # Turn loop
        playerGuess = parsePlayerWord("My guess: ")
        botGuess = pickWord()
        print("You: " + playerGuess + " : " + str(compareWords(playerGuess, botWord)))
        print("Bot: " + botGuess + " : " + str(compareWords(botGuess, playerWord, True)))
        if playerGuess == botWord:
            print("JOTTO!  You guessed Botto's word!")
            running = False
        if botGuess == playerWord:
            print("JOTTO!  Botto guessed your word!  Botto's word was '" + botWord + "'.")
            running = False
    input("Press [ENTER] to play again.")
    main()


def getBotWords():
    wordBank.clear()
    botList.clear()
    # text file reading brought to you by:
    # https://stackoverflow.com/questions/3925614/how-do-you-read-a-file-into-a-list-in-python
    with open('wordList') as wordList:
        inList = wordList.read().splitlines()
    for word in inList:
        botList.append(word)
        wordBank.append(word)
        dprint("Botto loaded " + str(len(botList)) + " words into their dictionary.")


def compareWords(wordA, wordB, botTurn = False):
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
        tempList = botGuesses.copy()
        for guess in tempList.keys():
            botLogic(guess, tempList[guess])
        botEliminateWords()
        dprint("Confirmed letters: " + str(botConfirmedLetters))
        dprint("Eliminated letters: " + str(botEliminatedLetters))
    return score


def botLogic(word, score):
    wordLetters = []
    for letter in word:
        wordLetters.append(letter)
    if(score == 0):
        # Scored 0, so every letter here is dead.
        for letter in wordLetters:
            if letter not in botEliminatedLetters:
                dprint('Eliminating ' + letter)
                botEliminatedLetters.append(letter)
    for letter in botEliminatedLetters:
        if letter in wordLetters:
            wordLetters.remove(letter)
    if len(wordLetters) == score:
        # All letters remaining are confirmed.
        for letter in wordLetters:
            if letter not in botConfirmedLetters:
                dprint('Confirming ' + letter)
                botConfirmedLetters.append(letter)
    for guess in botGuesses.keys():
        matches = 0
        guessLetters = []
        for letter in guess:
            guessLetters.append(letter)
        guessLettersVolatile = guessLetters.copy()
        unmatchedLetters = []
        letterDifference = {}
        for letter in wordLetters:
            if letter in guessLettersVolatile:
                matches += 1
                guessLettersVolatile.remove(letter)
            else:
                unmatchedLetters.append(letter)
        difference = 5 - matches
        scoreDifference = abs(score - botGuesses[guess])
        if difference == scoreDifference:
            # Different letters are confirmed and eliminated
            if score > botGuesses[guess]:
                for letter in unmatchedLetters:
                    if letter not in botConfirmedLetters:
                        dprint('Confirming ' + letter)
                        botConfirmedLetters.append(letter)
            elif score < botGuesses[guess]:
                for letter in guessLettersVolatile:
                    if letter not in botConfirmedLetters:
                        dprint('Confirming ' + letter)
                        botConfirmedLetters.append(letter)
    processedWord = ''.join(wordLetters)
    if word != processedWord:
        if word in botGuesses.keys():
            del botGuesses[word]
    if processedWord not in botGuesses.keys():
        botGuesses[processedWord] = score


def botEliminateWords():
    eliminationList = []
    for word in botList:
        eliminate = False
        for letter in botConfirmedLetters:
            if letter not in word:
                eliminate = True
        if eliminate:
            eliminationList.append(word)
    for word in eliminationList:
        botList.remove(word)


def parsePlayerWord(message):
    playerInput = str(input(message))
    if playerInput == "!debug":
        global debug
        if not debug:
            print("Entering debug mode!")
            debug = True
        else:
            print("Exiting debug mode!")
            debug = False
        return parsePlayerWord(message)
    if len(playerInput) != 5:
        print("Word must be exactly 5 letters long!")
        return parsePlayerWord(message)
    if not playerInput.isalpha():
        print("You can only use letters!")
        return parsePlayerWord(message)
    if not isValidWord(playerInput):
        print("Word is not a recognized english word.")
        return parsePlayerWord(message)
    return playerInput.lower()


def pickWord():
    # TODO: Give bot smarter way to pick a word.
    dprint(len(botList))
    word = botList[random.randint(0, len(botList) - 1)]
    botList.remove(word)
    return word

def isValidWord(word):
    return word in wordBank


def dprint(message):
    if debug:
        print(message)


main()