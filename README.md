autoCourseEval uses chrome browser as default. 
Currently supports chrome (v105, v106, v107), edge (v105, v106, v107) on Windows.

## *Disclaimer:*
autoCourseEval is a web scraping project. The university course evaluation is used to obtain genuine feedback from verified students on course activity each week. The outcome  might be taken into account when deciding whether to promote or increase the pay of a course lecturer. Although the autoCourseEval project has no negative effects on a lecturer's status, it provides the same feedback regardless of the events that occurs each week. Overall, autoCourseEval does not substitute manual filling; you are still responsible for completing your forms each week.

## Instructions
- Install the dependencies
```Shell
pip install -r requirements.txt
```
- Create a .env file inside the main autoCourseEval folder
- Let the .env file contain a username and a password 
![.env format](https://user-images.githubusercontent.com/97765765/200183996-776263b7-6f32-4895-9adb-66e6fb9cadbd.png)
- Open main.py
- Set the `submit` arguement to `True` to allow autoCourseEval submit the form
- Set the `Lecturer` arguement to `True` to fill in lecturer names for each week yourself
- Run main.py

**Note**: Run autoCourseEval in a virtual environment to prevent dependencies from conflicting.

## Documentation
call the `help()` function on a method to see its documentation.
```python
help(fill_eval)
```
```python
Help on function fill_eval in module __main__:

fill_eval(driver, url, elements, submit=False, lecturer=False)
    It takes a list of elements, and fills them into the evaluation form

    :param driver: The webdriver object
    :param url: The url of the evaluation page
    :param elements: A list of the answers to the questions
    :param submit: If True, the evaluation will be submitted, defaults to False (optional)
    :param lecturer: If you want to enter the lecturer for the week, set this to True, defaults to False
    (optional)
```


## Contributors
- [Miracle](https://www.github.com/Gamaliel51)
- [Daniel](https://www.github.com/ch1n3du)
- [King_Mikky](https://www.github.com/mikky-j)
- [John](https://www.github.com/daudujohn)

More contributions are welcome. Just create a pull request.

Tests for autoCourseEval were held under bandwidth speeds of **at least 1mb per second**.
**Above 750kb per second** is the recommended bandwidth speed.
### FOR EXTREME SLOW AUTOMATION CASES: 
1. chrome://settings -> Click Advanced at the bottom -> Check the Use hardware acceleration when available box
2. chrome://flags -> Search for WebGL in the search bar -> Enable / Activate WebGL

There are much better instructions [here](https://superuser.com/questions/836832/how-can-i-enable-webgl-in-my-browser)


*All drivers used in this project were gotten from the official [chrome](https://chromedriver.chromium.org/downloads) and [edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#installation) websites. They have only been renamed for the purpose of this project.*