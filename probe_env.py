import os, subprocess

base = "C:/AI_산출물/개발/tax-labor-manager"
print("prototype size:", os.path.getsize(os.path.join(base, "prototype_20261013/index.html")))
for cmd in [["git", "--version"], ["node", "--version"], ["python3", "--version"]]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(" ".join(cmd), "→", (r.stdout or r.stderr).strip()[:80])
