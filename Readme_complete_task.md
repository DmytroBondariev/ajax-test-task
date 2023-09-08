## Installing process

#### Run with Android Studio IDE
1. Clone the repository
2. Open the project in Android Studio
3. Run the project
4. Run the tests
5. Check the results in the terminal(Make sure you are running project directory)
6. If terminal command is not working, configure absolute imports in files due to your project root directory / try to run the tests with IDE pytest interface:
-right click on the tests folder
-choose Run pytest in the context menu
```
    git clone https://github.com/DmytroBondariev/ajax-test-task.git
    python -m venv venv
    sourse venv/bin/activate
    pip install -r requirements.txt
    pytest
```