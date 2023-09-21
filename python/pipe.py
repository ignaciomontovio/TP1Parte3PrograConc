from multiprocessing import Process, Pipe

def prompt(pipe):
    text = ""
    while text != 'close':
        text = str(input())
        pipe.send(text.lower())

def child_labour(pipe):
    longest = ""
    shortest = ""
    short_flag = False
    total_char = 0
    letters = 0
    digits = 0

    while True:
        data = pipe.recv()
        if data == 'close':
            break

        data_length = len(data)
        total_char += data_length
        if data_length > len(longest):
            longest = data

        if data_length < len(shortest) or not short_flag:
            shortest = data
            short_flag = True

        letters += sum(1 for l in data if l.isalpha())
        digits += sum(1 for n in data if n.isdigit())

    pipe.send(total_char)
    pipe.send(letters)
    pipe.send(digits)
    pipe.send(longest)
    pipe.send(shortest)

def statistics(pipe):
    print("Total de caracteres: " + str(pipe.recv()))
    print("Total de letras: " + str(pipe.recv()))
    print("Total de digitos: " + str(pipe.recv()))
    print("Palabra mas larga: " + pipe.recv())
    print("Palabra mas corta: " + pipe.recv())

if __name__ == '__main__':
    PARENT, CHILD = Pipe(duplex=True)

    child_process = Process(target=child_labour, args=(CHILD,))
    child_process.start()
    prompt(PARENT)
    statistics(PARENT)
    child_process.join()
