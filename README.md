### The kafka pokemon fight!  
<img src="https://pokemonletsgo.pokemon.com/assets/img/common/char-pikachu.png" width="120" height="150">

The aim of this project is just to get started with kafka.  

To start with, I used a public Docker image provided by [Confluent](https://developer.confluent.io/get-started/python/#kafka-setup)  

As a producer, I decided to go through the [PokeAPI](https://pokeapi.co/), and used a random selector for a pokemon and its main ability through a basic ending loop.  

The consumer will then print out the battle in real-time.

Let's fight!!!  

_P.D. Next steps on this project should include:_  
_*  Writing the events to a database_    
_*  Synching a dashboard with the data in the database_  
_*  Adding more features by using a new topic to categorize data and load into another table_  
