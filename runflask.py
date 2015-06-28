from app import app


def run():
    print("""
    +===================================+
    ¦   Parkwood Vale Harriers Webapp   ¦
    +===================================+
    ¦   Stop the application by either  ¦
    ¦   closing the console window, or  ¦
    ¦         pressing CTRL+C.          ¦
    +===================================+
    ¦    Made by Christopher Stevens    ¦
	¦      GITHUB/PUBLIC VERSION        ¦
    +===================================+
    """)
    app.run(debug=True, use_reloader=False)
if __name__ == "__main__":
    run()