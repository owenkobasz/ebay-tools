from pathlib import Path

def generate_index():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>My Python Site</title></head>
    <body>
        <h1>Welcome to My Python-Generated Site!</h1>
        <p>This page was built with Python.</p>
    </body>
    </html>
    """
    Path("build").mkdir(exist_ok=True)
    with open("build/index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    generate_index()
