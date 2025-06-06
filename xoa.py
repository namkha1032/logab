path = "../../../lib/python3.10/site-packages/urllib3/connectionpool.py"

def check_site_packages(path):
    if "site-packages" in path:
        parts = path.split("site-packages", 1)
        new_path = "lib" + parts[1]
        # Remove any leading slash if necessary
        if new_path.startswith("/"):
            new_path = "lib" + parts[1][1:]
        return new_path
    else:
        return path

print(check_site_packages(path=path))