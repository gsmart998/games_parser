# games_parser

## Installation
### Local
Clone the repository,then use command to install packages:

```
pip install -r requirements.txt
```

Then run the command:
```
python3 ./src/main.py
```

### Docker
Clone the repository, use the docker command to start service: 
```
docker-compose up -d
```

## Usage
Amount and catalog_name required params.
amount: int and > 0
catalog_name: str
Example requests:
```
curl http://localhost:5000\?amount\=4\&catalog_name\=ps-game

curl http://localhost:5000\?amount\=2\&catalog_name\=xbox-game-addons
```