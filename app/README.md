<h3>How to Build the App?</h3>
    <p>
        1. Download the source from app folder
    </p>
    <p>
        You may have to modify app.spec to be compatible with your OS
        <br/>
        (Open app.spec in a Text Editor and remove the <code>app = BUNDLE(...)</code> for non-Macs)
    </p>
    <p>
        2. Open Console/Terminal and change directory to the src folder<br/>
        <code>$ cd src</code>
    </p>
    <p>
        3a. Install pyinstaller if you haven't already:<br/>
        <code>$ pip install -U pyinstaller</code>
    </p>
    <p>
        3.b Assuming you have pyinstaller, type the following:<br/>
        <code>$ pyinstaller app.spec</code>
    </p>
