import markdown2, re, glob, pathlib, os


def serialize_filename(filename: str, content: str) -> str:
    full_name = filename.split(".")
    name, _ = full_name[0], full_name[1]
    title = re.search(r"<h1>(.*)</h1>", content).group(1)
    return f"{name}_{title.replace(' ', '-')}.html"


def clean_assets():
    for file in glob.glob("assets/blog/*"):
        if file == ".gitignore":
            continue
        os.remove(file)
    

def build_blog():
    files = glob.glob("blog/*.md")
    for file in files:
        file = pathlib.Path(file)
        with open(file, "r") as f:
            markdown = f.read()
        html = markdown2.markdown(markdown)
        dest = pathlib.Path("assets/blog") / serialize_filename(file.name, html)
        with open(dest, "w") as f:
            f.write(html)
    

if __name__ == "__main__":
    clean_assets()
    build_blog()