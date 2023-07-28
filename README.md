### The kafka pokemon fight!  
<img src="https://pokemonletsgo.pokemon.com/assets/img/common/char-pikachu.png" width="120" height="150">

The aim of this project is just to get started with kafka.  

To start with, I used a public Docker image provided by [Confluent](https://developer.confluent.io/get-started/python/#kafka-setup)  

As a producer, I decided to go through the [PokeAPI](https://pokeapi.co/), and used a random selector for a pokemon and its main ability through a basic ending loop.    

First, the producer will print the event sent to the appropriate topic in the terminal as follows:

![image](https://github.com/silviaherf/kafka-pokemon-fight/assets/65872238/dca8af2a-9de3-4635-af28-7139a8dfa491)


The consumer will then load each event to a table in Postgres 
![image](https://github.com/silviaherf/kafka-pokemon-fight/assets/65872238/676f6536-b46c-4708-a05c-2ff29a2ba21d)  

and will print out the battle in real-time in the terminal.

![image](https://github.com/silviaherf/kafka-pokemon-fight/assets/65872238/6c6b9bd4-a728-4805-8676-8d96808c6be8)   


Let's fight!!!

_P.D. Next steps on this project should include:_  
* _Synching a dashboard with the data in the database_  
* _Adding more features by using a new topic to categorize data and load into another table_  
