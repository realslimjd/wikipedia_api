Prequisites: [Python 3](http://docs.python-guide.org/en/latest/), [Pip](https://pip.pypa.io/en/stable/installing/), [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/), [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

How to run this application:
0. Make sure you have all the prerequisites installed. If not, follow all the linked instructions above for how to install them.
1. Clone this directory into a new folder.
2. In the project directory, create a new virtualenv with the command `virtuaulenv -p python3 env`
3. Activate the virtualenv with `source env/bin/activate`
4. Install the dependencies by running `pip install -r requirements.txt`
5. Change directories to the `app` directory with `cd app`
6. Set the flask environment variable by typing `export FLASK_APP=site.py`
7. Run the app with `flask run`
8. Open your web browser and navigate to <http://127.0.0.1:5000/>
9. You can stop the Flask server by hitting `Ctrl+C`
10. Close the virtualenv with the command `deactivate`