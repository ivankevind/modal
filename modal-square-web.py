"""Draft only — not deployed, not pushed.

Same square example as ~/workspace/modal-example/example.py, but exposed
over plain HTTPS so Muse (and a phone browser) can call it with a normal
web request, which works from this VM, instead of the Modal gRPC client,
which does not.

Deploy path that avoids this VM's network block:
  GitHub Actions runs on a GitHub runner with direct internet, so it can
  run `modal deploy` with MODAL_TOKEN_ID / MODAL_TOKEN_SECRET set from
  GitHub secrets (Modal docs pattern). No laptop, no Termux needed.

After deploy, Modal prints a URL like:
  https://<workspace>--example-get-started-web-square.modal.run
Then, from this VM / a phone browser:
  curl "https://<workspace>--example-get-started-web-square.modal.run?x=42"
  -> {"x": 42, "square": 1764, "note": "This code is running on a remote worker!"}

Security note: this draft leaves the endpoint public for the first test,
exactly like Modal's basic web tutorial. Before any real use, add
requires_proxy_auth=True (Modal proxy token) or a Bearer-token check
via a Modal Secret — do NOT put any token in this file or in git.
"""

import modal

image = modal.Image.debian_slim().pip_install("fastapi")

app = modal.App("example-get-started-web")


@app.function(image=image)
@modal.fastapi_endpoint(method="GET")
def square(x: int):
    print("This code is running on a remote worker!")
    return {"x": x, "square": x**2, "note": "This code is running on a remote worker!"}
