from multiprocessing import Pipe
import os
import sys

CHILD = 0
ERROR = -1
INIT = 1
CHARS = 0
LETTERS = 1
DIGITS = 2
MAX = 3
MIN = 4
FIRST_MSG = True
SECOND_MSG = False
FIRST = 0

def son(son_tx, son_rx):
    first = FIRST_MSG
    digits = 0
    chars = 0
    letters = 0
    msg = son_rx.recv()
    
    while msg != "close":
        if first:
            max_word, min_word = msg, msg
            first = SECOND_MSG
        else:
            max_word = max_word_length(max_word, msg)
            min_word = min_word_length(min_word, msg)
            
        chars += len(msg)
        digits = count_digits(digits, msg)
        letters = count_letters(letters, msg)
        msg = son_rx.recv()
    
    son_rx.close()
    son_tx.send((chars, letters, digits, max_word, min_word))
    os._exit(0)

def father(father_tx, father_rx, son_tx, son_rx):
    pid = os.fork()
    
    if pid == ERROR:
        sys.exit("Error al crear el proceso")
    
    if pid == CHILD:
        father_tx.close()
        father_rx.close()
        son(son_tx, son_rx)
    else:
        son_tx.close()
        son_rx.close()
        msg = input("Ingrese un mensaje: ")
        father_tx.send(msg)
        
        while msg != "close":
            msg = input("Ingrese un mensaje: ")
            father_tx.send(msg)
        
        father_tx.close()
        statistics(father_rx.recv())
        os.wait()

def count_digits(digits, msg):
    for i in range(10):
        digits += msg.count(str(i))
    return digits

def count_letters(letters, msg):
    for letter in msg:
        if letter.isalpha():
            letters += 1
    return letters

def max_word_length(max_word, msg):
    words = msg.split()
    
    for word in words:
        if not word.isdigit():
            if len(word) > len(max_word.split(",")[FIRST]):
                max_word = word
            elif len(word) == len(max_word.split(",")[FIRST]):
                max_word += ", " + word
    
    return max_word

def min_word_length(min_word, msg):
    words = msg.split()
    
    for word in words:
        if not word.isdigit():
            if len(min_word.split(",")[FIRST]) > len(word):
                min_word = word
            elif len(word) == len(min_word.split(",")[FIRST]):
                min_word += ", " + word
    
    return min_word

def statistics(msg):
    print("#########################")
    print("Cantidad de caracteres: ", msg[CHARS])
    print("Cantidad de letras: ", msg[LETTERS])
    print("Cantidad de dígitos: ", msg[DIGITS])
    print("Palabra más larga: ", msg[MAX])
    print("Palabra más corta: ", msg[MIN])
    print("#########################")

def main():
    father_tx, son_rx = Pipe()
    son_tx, father_rx = Pipe()
    father(father_tx, father_rx, son_tx, son_rx)

if __name__ == '__main__':
    main()
