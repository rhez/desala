<h3>How to Build the App?</h3>
    <p>
        1. Download the source from app folder
    </p>
    <p>
        2. Open Console/Terminal and change directory to the src folder
        <br/>
        <code>$ cd src</code>
    </p>
    <p>
        You may have to modify app.spec to be compatible with your OS
        <br/>
        (Open app.spec in a Text Editor and remove the "app = BUNDLE(...)" for non-Macs)
    </p>
    <p>
        3. Assuming you have pyinstaller, type the following:
        <br/>
        <code>$ pyinstaller app.spec</code>
    </p>
