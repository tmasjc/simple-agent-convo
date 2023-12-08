## Simple Chat w/ Wizard Bob 

First, edit `config.ini.sample` and rename to `config.ini` (configuration file).

Then, setup development environment as shown below.

```bash
## setup Chroma vector database
docker pull chromadb/chroma
docker run -p 8000:8000 chromadb/chroma

## on separate window
redis-server

## on separate window
## activate virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

chmod +x run.sh # make sure script is executable
./run.sh # run command
```

