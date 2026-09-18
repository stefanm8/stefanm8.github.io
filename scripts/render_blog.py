import markdown2
import glob
import pathlib

if __name__ == "__main__":
    files = glob.glob("blog/*.md")
    for file in files:
        file = pathlib.Path(file)
        dest = pathlib.Path("assets/blog") / file.name.replace(".md", ".html")
        with open(file, "r") as f:
            markdown = f.read()
        html = markdown2.markdown(markdown)
        with open(dest, "w") as f:
            f.write(html)
    