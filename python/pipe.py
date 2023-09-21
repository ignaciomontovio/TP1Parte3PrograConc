from multiprocessing import Process, Pipe

def prompt(pipe):
    text = ""
    while text != 'close':
        text = str(input())
        pipe.send(text.lower())

def childLabour(pipe):
    longest = ""
    shortest = ""
    shortFlag = False
    totalChar = 0
    letters = 0
    digits = 0

    while True:
        data = pipe.recv()
        if data == 'close':
            break
        else:
            dataLength = len(data)
            totalChar += dataLength
            if dataLength > len(longest):
                longest = data
            
            if dataLength < len(shortest) or not(shortFlag) :
                shortest = data
                shortFlag = True
            
            letters += sum(1 for l in data if l.isalpha())
            digits += sum(1 for n in data if n.isdigit())

    child.send(totalChar)
    child.send(letters)
    child.send(digits)
    child.send(longest)
    child.send(shortest)

def statistics(pipe):
    print("Total de caracteres: " + str(pipe.recv()))
    print("Total de letras: " + str(pipe.recv()))
    print("Total de digitos: " + str(pipe.recv()))
    print("Palabra mas larga: " + pipe.recv())
    print("Palabra mas corta: " + pipe.recv())

if __name__ == '__main__':
    parent, child = Pipe(duplex=True)

    child_process = Process(target=childLabour, args=(child,))
    child_process.start()
    prompt(parent)
    statistics(parent)
    child_process.join()

    
