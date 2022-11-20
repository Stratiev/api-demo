# Demo API

## About
This is a demo API prepared for a coding assignment. It is a toy example with the goal of satisfying the following requirements:

- Respond to json requests
- Make a call to an external executable
- Approriately handle errors with the correct http status code
- Handle new requests while performing a blocking call
- Graceful shutdown
- Sample unit test(s)

This API supports two endpoints. 

The first one allows the client to browse through the file system of the server by exposing the `ls` binary.

The second API takes two soccer club names and returns which one is more likely to win along with the probability.

## Set up

### Prerequisites

First, clone the repository to your local computer

```
git clone git@github.com:Stratiev/api-demo.git
```

Then navigate to the project folder and set up your favourite virtual environment. Here we use `venv`:

```
cd /path/to/api-demo
python -m venv venv
source venv/bin/activate
```

Install the dependencies:
```
pip install --upgrade pip && pip install -r requirements.txt
```

### Set up external executable for /probability end point

Compile the python file into a binary.

```
./create_executable.sh
```

### Run tests and use code

You can check if the code works as expected by running the unit tests:

```
pytest test/unit_tests.py
```

Finally, run the live server:
```
uvicorn main:app --reload --app-dir app
```

Now you can manually inspect the endpoints on the [docs page](http://127.0.0.1:8000/docs).

For example

```
curl -X 'POST' \
  'http://127.0.0.1:8000/probability' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "team_1": "Djurgarden",
  "team_2": "Hammarby"
}'
```

should produce something like this

```
"Djurgarden has probability 0.563 of winning against Hammarby.\n"
```

## To-do

- Extract the output of `ls` and turn it into a list. For example, default `ls` can return a json
    `{'items': [list_returned_by_ls]}`,
whereas if `-l` is provided (`ls -l`) can format `list_returned_by_ls` as a dictionary with keys 'permissions', 'user', 'group', 'last_modified', 'filetype' etc.
For other options one may properly format information about inodes, file sizes and other.
- The output of /probability can be split into 'text', which is the original output of the binary and 'probability', which is the numerical value extracted.
- Override default validation errors from fastAPI in order to add logging for the automated validation error handling.
- Add authentication and a limit to the number of requests per user, etc...

