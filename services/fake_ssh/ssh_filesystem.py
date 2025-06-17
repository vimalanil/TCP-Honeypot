# services/fake_ssh/ssh_filesystem.py

fake_fs = {
    "home": {
        "vimal": {
            "README.txt": "Welcome to your home directory.",
            "notes.txt": "To-do:\n- Monitor logs\n- Update firewall rules"
        }
    },
    "etc": {
        "passwd": "root:x:0:0:root:/root:/bin/bash\nvimal:x:1000:1000:vimal:/home/vimal:/bin/bash",
        "shadow": "root:$6$abc123$...:18295:0:99999:7:::"
    },
    "var": {
        "log": {
            "syslog": "System booted\nNew login from 192.168.1.10",
            "auth.log": "Failed login for root from 192.168.1.20"
        }
    }
}

def list_dir(path):
    parts = [p for p in path.strip("/").split("/") if p]
    node = fake_fs
    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return f"ls: cannot access '{path}': No such file or directory"
    if isinstance(node, dict):
        return "\n".join(node.keys())
    return f"ls: cannot access '{path}': Not a directory"

def cat_file(path):
    parts = [p for p in path.strip("/").split("/") if p]
    node = fake_fs
    for part in parts[:-1]:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return f"cat: {path}: No such file or directory"
    file = parts[-1]
    return node.get(file, f"cat: {path}: No such file")
