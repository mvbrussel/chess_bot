# Chess AI (WIP)
This project provides an application in which you can play chess against a trained AI model. It comes with an interactive chess interface where you can make moves and a trained model on 10M+ observations which you play against.

<!-- placeholder for video -->

## Usage

<!-- Provide detailed instructions on how to set up the project on a local machine. This includes any necessary dependencies, software requirements, and installation steps. Make sure to include clear and concise instructions so that others can easily replicate your setup. -->
- Clone the repository to your local machine
- Create a pip environment and install the packages using `pip install -r requirements.txt`
- Run the `main.py` file to start the application


## Repository structure

- [chess_game](https://github.com/mvbrussel/chess_bot/tree/master/chess_game): Provides the code for building the interactive chess application. Includes board creation, definition of the AI player, definition of the Human player
- [move_prediction](https://github.com/mvbrussel/chess_bot/tree/master/move_prediction): Provides the code for training the chess AI model. Includes creation of the dataset, exploratory analysis and training of the predictive model
- [stockfish](https://github.com/mvbrussel/chess_bot/tree/master/stockfish): The downloaded Stockfish engine. Have the trained AI model play against the commonly used Stockfish engine to determine performance
- [utils](https://github.com/mvbrussel/chess_bot/tree/master/utils): utility functions that are used accross the project

## Data

Due to the file size, the source and cleaned data is not available in the repository. Please contact me to obtain the data if needed.

### Source data
A dataset is created from [Lichess](https://database.lichess.org/) data. PGN data of +1M chess games is downloaded from which the FEN position of the board is derived. With this, the move made for a specific board FEN can be derived

### Encoding the data
To make the data understandable for the neural network, it needs to be encoded. This is done in the same way that DeepMind did with AlphaZero - their chess engine. Details can be found in the paper ["Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm"](https://arxiv.org/abs/1712.01815v1).

It results in a board position represented with an (8,8,119) shaped array and the moves represented with an (4672) array. This is the input used for training the model

## Model

Several model structures were implemented with the optimal result obtained with a Neural Network consisting of five layers. Details can be found in the model_training notebook

<!-- Placeholder for screenshot of model -->

## Contact
If you have any questions or suggestions, feel free to reach out



