#include <atomic>
#include <cctype>
#include <cstring>
#include <iostream>
#include <thread>
#include <vector>

#define CHAR_OFFSET ('A' - 1)
#define NOT_MODIFIED 0

// -- Funciones utilizadas --
int Hash(const char c);
void Hashing(const std::string &str, size_t count,
             std::vector<std::atomic_int> &hashed_values);

// -- Main function --
int main(int argc, const char *argv[])
{
  size_t length;

  // -- Nos aseguramos que la cadena pasada como argumento sea valida --
  if (argc < 1 || argv[1] == nullptr || (length = strlen(argv[1])) <= 0)
  {
    std::cerr << "[Error] - Missing string parameter" << std::endl;
    return EXIT_FAILURE;
  }

  // -- Variables utilizadas --
  // -- Para mantener la sincronizacion entre hilos utilizamos enteros atomicos
  // --
  std::vector<std::atomic_int> hashed_values(length);
  std::string str(argv[1], length);
  size_t half = length / 2;
  std::thread t1, t2;

  // -- Si el tamaño de la cadena es par lo repartimos equitativamente --
  if (length % 2 == 0)
  {
    t1 = std::thread(Hashing, str, half, std::ref(hashed_values));
    t2 = std::thread(Hashing, str, half, std::ref(hashed_values));
  }
  // -- Sino le damos uno de mas al primer hilo --
  else
  {
    t1 = std::thread(Hashing, str, half + 1, std::ref(hashed_values));
    t2 = std::thread(Hashing, str, half, std::ref(hashed_values));
  }

  // -- Esperamos que terminen su ejecucion --
  t1.join();
  t2.join();

  // -- Imprimos todos los elementos menos el ultimo,
  //    para evitarnos dejar una coma de mas --
  std::cout << "Result: [";
  for (size_t i = 0; i < length - 1; i++)
  {
    std::cout << hashed_values[i] << ", ";
  }
  std::cout << hashed_values[length - 1] << "]" << std::endl;

  return EXIT_SUCCESS;
}

// -- La idea general para mantener la sincronizacion es utilizar un vector
//    con sus elementos protejidos (en este caso de manera atomica)
//    y solo modificar los que no estan siendo usados o no hayan sido
//    modificados --
void Hashing(const std::string &str, size_t count,
             std::vector<std::atomic_int> &hashed_values)
{
  // -- Iteramos hasta que se acabe la cadena o
  //    haya cumplido con su cantidad de elementos especificada --
  for (size_t i = 0; count > 0 && i < str.length(); i++)
  {
    // -- Antes de tratar de modificarlo nos fijamos si el elemento atomico
    //    esta siendo utilizado o si ya fue modificado --
    if (hashed_values[i].is_lock_free() && hashed_values[i] == NOT_MODIFIED)
    {
      hashed_values[i] = Hash(str[i]);
      count--;
    }
  }
}

// -- Con esta funcion nos aseguramos que el char 'c' este en mayuscula,
//    y luego le restamos un offset para que nos de un valor entre 1 y 27.
//    En caso de no ser un valor alfabetico nos devolvera un 0 --
int Hash(const char c) { return (isalpha(c)) ? toupper(c) - CHAR_OFFSET : 0; }