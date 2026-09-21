import markdown2, re, glob, pathlib, os, json

def get_title(content: str) -> str:
    return re.search(r"<h1>(.*)</h1>", content, re.IGNORECASE | re.DOTALL).group(1)

def serialize_filename(filename: str, content: str) -> str:
    full_name = filename.split(".")
    name, _ = full_name[0], full_name[1]
    title = re.search(r"<h1>(.*)</h1>", content).group(1)
    return f"{name}_{title.replace(' ', '-')}.html"

def parse_filename(fname: str) -> dict:
    return {
        "title": fname.split("_")[1].replace(".html", "").replace("-", " "),
        "date": fname.split("_")[0],
        "path": fname,
    }

def clean_assets(assets_dest: str):
    for file in glob.glob(f"{assets_dest}/*"):
        if file == ".gitignore":
            continue
        os.remove(file)
    with open("assets/files.json", "w") as f:
        f.write(json.dumps([]))

def build_files_json(files):
    with open("assets/files.json", "w") as f:
        files_json = []
        for file in files:
            file = pathlib.Path(file)
            files_json.append(parse_filename(file.name))
        f.write(json.dumps(files_json))


def with_parts(html: str) -> str:
    with open("index.html", "r") as f:
        index = f.read()
    

    
    head = re.search(r"<head>(.*)</head>", index, re.IGNORECASE | re.DOTALL).group(1)
    footer = re.search(r"<footer>(.*)</footer>", index, re.IGNORECASE | re.DOTALL).group(1)
    head = re.sub(r"<title>(.*)</title>", lambda _: f"<title>{get_title(html)}</title>", head, flags=re.IGNORECASE | re.DOTALL)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
{head}
</head>
<body>
{html}
<footer>
{footer}
</footer>
</body>
</html>
"""

def build_blog(assets_dest: str):
    files = glob.glob("blog/*.md")

    for file in files:
        file = pathlib.Path(file)
        with open(file, "r") as f:
            markdown = f.read()
        html = markdown2.markdown(markdown)
        dest = pathlib.Path(assets_dest) / serialize_filename(file.name, html)
        with open(dest, "w") as f:
            f.write(with_parts(html))
    
    files = glob.glob(f"{assets_dest}/*.html")
    build_files_json(files)





if __name__ == "__main__":
    assets_dest = "posts" # relative to workdir
    clean_assets(assets_dest)
    build_blog(assets_dest)