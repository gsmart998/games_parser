# games_parser

## Installation
Clone the repository, then in the terminal, being in the folder with the project, use command to install packages:

```
pip install -r requirements.txt
```

Then in the terminal go to the `/src` folder and run the command:
```
python3 main.py
```

## Usage
Amount and catalog_name required params.
Example requests:
```
curl http://localhost:5000\?amount\=4\&catalog_name\=ps-game

curl http://localhost:5000\?amount\=2\&catalog_name\=xbox-game-addons
```