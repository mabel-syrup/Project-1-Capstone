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
    # Python is kinda weird and you have to do this so it doesn't create a local variable with the same name
    global debug
    debug = False
    # Only relevant when you play a second time, but it doesn't hurt to do it on game 1.
    botEliminatedLetters.clear()
    botConfirmedLetters.clear()
    botGuesses.clear()
    running = True
    # Loads the acceptable words into the list.
    getBotWords()
    # Player specifies their word for Botto to guess.
    playerWord = parsePlayerWord("My word: ")
    # Botto picks a random word
    botWord = pickWord()
    while running:
        # Turn loop
        playerGuess = parsePlayerWord("My guess: ")
        # Bot chooses a word to guess
        botGuess = pickWord()
        # User interface.
        print("You: " + playerGuess + " : " + str(compareWords(playerGuess, botWord)))
        print("Bot: " + botGuess + " : " + str(compareWords(botGuess, playerWord, True)))
        if playerGuess == botWord:
            print("JOTTO!  You guessed Botto's word!")
            running = False
        if botGuess == playerWord:
            print("JOTTO!  Botto guessed your word!  Botto's word was '" + botWord + "'.")
            running = False
    # Ready to play again.
    input("Press [ENTER] to play again.")
    main()


def getBotWords():
    # Clears anything left over from last game.
    wordBank.clear()
    botList.clear()
    # text file reading brought to you by:
    # https://stackoverflow.com/questions/3925614/how-do-you-read-a-file-into-a-list-in-python
    with open('wordList') as wordList:
        inList = wordList.read().splitlines()
    # Throw each word into the lists.
    for word in inList:
        botList.append(word)
        wordBank.append(word)
        # dprint is a method that checks if we're in debug mode before printing.
        dprint("Botto loaded " + str(len(botList)) + " words into their dictionary.")


def compareWords(wordA, wordB, botTurn = False):
    wordBList = []
    score = 0
    for letter in wordB:
        wordBList.append(letter)
    for letter in wordA:
        # Check letter by letter for matches
        if letter in wordBList:
            # Matching letter found
            score += 1
            # Remove the matched letter for any repeated letters (like queue)
            wordBList.remove(letter)
    if(botTurn):
        # Bot has some extra stuff going on
        botLogic(wordA,score)
        # We modify the dictionary during this next part, so we are going to make a copy first
        tempList = botGuesses.copy()
        # Iterate through the copy.  Don't want any mismatches.
        for guess in tempList.keys():
            botLogic(guess, tempList[guess])
        # Bot eliminates words that aren't possible to narrow their guesses.
        botEliminateWords()
        # Debug output
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
            # Make sure we don't put duplicates in.
            if letter not in botEliminatedLetters:
                dprint('Eliminating ' + letter)
                botEliminatedLetters.append(letter)
    for letter in botEliminatedLetters:
        # Remove each eliminated letter from a guessed word.
        # We don't need to worry about them anymore.
        if letter in wordLetters:
            wordLetters.remove(letter)
    if len(wordLetters) == score:
        # All letters remaining are confirmed.
        for letter in wordLetters:
            if letter not in botConfirmedLetters:
                dprint('Confirming ' + letter)
                botConfirmedLetters.append(letter)
    # Look through all previous guesses.
    for guess in botGuesses.keys():
        matches = 0
        guessLetters = []
        for letter in guess:
            guessLetters.append(letter)
        guessLettersVolatile = guessLetters.copy()
        unmatchedLetters = []
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
    # Word might have been changed by eliminating letters.
    processedWord = ''.join(wordLetters)
    # If it changed, we need to update the dictionary to remove the old entry.
    if word != processedWord:
        if word in botGuesses.keys():
            del botGuesses[word]
    # If the word isn't in the dictionary, (yet OR any more,) we need to add it.
    if processedWord not in botGuesses.keys():
        botGuesses[processedWord] = score


def botEliminateWords():
    # Make a list of words to eliminate.
    # We iterate through the word list, so we can't eliminate as we go.
    eliminationList = []
    for word in botList:
        eliminate = False
        for letter in botConfirmedLetters:
            if letter not in word:
                eliminate = True
        if eliminate:
            eliminationList.append(word)
    # Eliminate the words.
    for word in eliminationList:
        botList.remove(word)


def parsePlayerWord(message):
    # This handles player input.
    playerInput = str(input(message))
    # Special case: !debug will enter or exit debug mode
    if playerInput == "!debug":
        global debug
        if not debug:
            print("Entering debug mode!")
            debug = True
        else:
            print("Exiting debug mode!")
            debug = False
        return parsePlayerWord(message)
    # If the word isn't 5 letters long, it can't be used.
    if len(playerInput) != 5:
        print("Word must be exactly 5 letters long!")
        return parsePlayerWord(message)
    # You can't use numbers or punctuation.
    if not playerInput.isalpha():
        print("You can only use letters!")
        return parsePlayerWord(message)
    # Word was correct length, but it's not within the accepted words.
    # No proper nouns can be used; and some words are banned.
    if not isValidWord(playerInput):
        print("Word is not a recognized or allowed english word. Make sure you are not using proper nouns.")
        return parsePlayerWord(message)
    return playerInput.lower()


def pickWord():
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