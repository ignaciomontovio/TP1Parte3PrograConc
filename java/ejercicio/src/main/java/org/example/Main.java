package org.example;

import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.Scanner;
import java.util.concurrent.ArrayBlockingQueue;

public class Main
{

  public static Integer AMOUNT_OF_NUMBERS;
  public static final int LIMIT_NUMBER = 99;
  public static ArrayBlockingQueue<Integer> LIST_OF_NUMBERS;

  public static class ProducerThread implements Runnable
  {

    @Override
    public void run()
    {
      Random rand = new Random();
      for (int i = 0; i < AMOUNT_OF_NUMBERS; i++)
      {
        Integer randomValue = rand.nextInt(LIMIT_NUMBER + 1);
        System.out.println("Se ha producido el número " + randomValue);
        LIST_OF_NUMBERS.add(randomValue);
      }
    }
  }

  public static class ConsumerThread implements Runnable
  {

    @Override
    public void run()
    {
      int sum = 0,
          max = 0,
          min = 100,
          number;
      Map<Integer, Integer> numberFrecuencyMap = new HashMap<>();
      try
      {
        for (int i = 0; i < AMOUNT_OF_NUMBERS; i++)
        {
          number = LIST_OF_NUMBERS.take();
          sum += number;
          if (number > max)
          {
            max = number;
          }
          if (number < min)
          {
            min = number;
          }
          numberFrecuencyMap.put(number, numberFrecuencyMap.getOrDefault(number, 0) + 1);
        }
      } catch (Exception e)
      {
        throw new NoSuchElementException(
            "Error taking from queue LIST_OF_NUMBERS." + e.getMessage());
      }
      System.out.println("La suma de los valores es: " + sum);
      System.out.println("El valor máximo es: " + max);
      System.out.println("El valor mínimo es: " + min);
      System.out.println("El promedio de los valores es: " + (float)sum / AMOUNT_OF_NUMBERS);
      Integer maxFrecuency = numberFrecuencyMap.values().stream().max(Integer::compare).get();
      System.out.println("El/Los valor/es mas frecuente/s son: ");
      numberFrecuencyMap.forEach((key, value) ->
      {
        if (value.equals(maxFrecuency))
        {
          System.out.println(key);
        }
      });
      System.out.println("El/Los valor/es ha/n aparecido " + maxFrecuency + " veces.");
    }
  }

  public static void main(String[] args) throws InterruptedException
  {
    AMOUNT_OF_NUMBERS = Integer.parseInt(args[0]);
    LIST_OF_NUMBERS = new ArrayBlockingQueue<>(AMOUNT_OF_NUMBERS);
    Thread producer = new Thread(new ProducerThread());
    Thread consumer = new Thread(new ConsumerThread());
    producer.start();
    consumer.start();

    producer.join();
    consumer.join();
  }
}