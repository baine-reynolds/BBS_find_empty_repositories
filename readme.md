## Dependency
* Python 3.6+ (due to the use of f strings)
* [Requests Package](http://docs.python-requests.org/en/master/)

`
pip3 install requests --user
`
or
`
pip3 install -r requirements.txt
`

## Background
This tool is designed to use the Bitbucket Server REST API to locate any potentially empty repositories. This is commonly used as a diagnostic for a few different reasons.

## Usage
1. Install dependencies as mentioned above
2. Run the find_empty.py  `
python3 find_empty.py
`
3. Enter url of Bitbucket environment, followed by any admin username and it's respective password when prompted.
4. Review printed output for results
