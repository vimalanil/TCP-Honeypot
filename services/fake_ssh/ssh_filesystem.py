# services/fake_ssh/ssh_filesystem.py

fake_fs = {
    "home": {
        "vimal": {
            "README.txt": "Welcome to your home directory.",
            "notes.txt": "To-do:\n- Monitor logs\n- Update firewall rules",
            ".ssh": {
                "id_rsa": "-----BEGIN RSA PRIVATE KEY-----\nFAKEKEY1234567890\n-----END RSA PRIVATE KEY-----"
            },
            "secrets.txt": "FLAG{fake_ctf_flag_here}"
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
    },
    "tmp": {
        "backup.zip": "[Binary ZIP file contents here]"
    }
}

def _resolve_path(path):
    parts = [p for p in path.strip("/").split("/") if p]
    node = fake_fs
    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return None
    return node

def list_dir(path):
    node = _resolve_path(path)
    if isinstance(node, dict):
        return "\n".join(node.keys())
    return f"ls: cannot access '{path}': Not a directory"

def cat_file(path):
    parts = [p for p in path.strip("/").split("/") if p]
    node = fake_fs
    for part in parts[:-1]:
        node = node.get(part)
        if node is None or not isinstance(node, dict):
            return f"cat: {path}: No such file or directory"
    file = parts[-1]
    content = node.get(file)
    if isinstance(content, dict):
        return f"cat: {path}: Is a directory"
    return content or f"cat: {path}: No such file"

