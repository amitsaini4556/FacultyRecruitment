# Faculty-Recruitment

## Prerequisite for project [for Windows]

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash

#start Command Prompt for windows
$ pip install virtualenv
$ virtualenv myenv
$ myenv\Scripts\activate

# open Git bash here and use below command.
# clone below repo or fork in personal account
$ git clone https://github.com/amitsaini4556/Faculty-Recruitment.git
$ cd Faculty-Recruitment

$ pip install -r requirements.txt

$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Rules
- Use camelcase naming convention for new file
- Use SOLID principles
## Contributing

I love contributions, so please feel free to fix bugs, improve things, provide documentation. Just send a pull request.
