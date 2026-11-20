"""Notify IndexNow after verifying a Just Compress Pages deployment."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
HOST = "justcompress.online"
SITE = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"
LOC = ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout


def page_path(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.netloc != HOST or parts.query or parts.fragment:
        raise ValueError(f"All submitted URLs must be public HTTPS pages on {HOST}")
    path = unquote(parts.path or "/")
    return (path + "index.html" if path.endswith("/") else path).lstrip("/")


def sitemap_urls(sitemap):
    return {node.text.strip() for node in ElementTree.fromstring(sitemap).findall(LOC) if node.text}


def plan_urls(base, target, target_sitemap, url_file):
    previous = sitemap_urls(git("show", f"{base}:sitemap.xml"))
    current = sitemap_urls(target_sitemap)
    differences = git("diff", "--name-only", "--no-renames", "-z", base, target)
    changed_files = set(differences.decode().split("\0"))
    urls = (previous ^ current) | {url for url in previous | current if page_path(url) in changed_files}
    if url_file:
        backlog = {line.strip() for line in url_file.read_text().splitlines() if line.strip()}
        for url in backlog:
            page_path(url)
        urls |= backlog
    if len(urls) > 10_000:
        raise ValueError("IndexNow accepts up to 10,000 URLs in one batch")
    return sorted(urls)


def ownership_file(target):
    matches = []
    for name in git("ls-tree", "--name-only", "-z", target).decode().split("\0"):
        if re.fullmatch(r"[A-Za-z0-9-]{8,128}\.txt", name):
            content = git("show", f"{target}:{name}")
            if content.strip() == name[:-4].encode():
                matches.append((name, content))
    if len(matches) != 1:
        raise ValueError("Expected one published IndexNow verification file")
    return matches[0]


def submit(plan, sitemap, receipt_path):
    if receipt_path.exists():
        prior = json.loads(receipt_path.read_text())
        same_batch = all(prior.get(key) == value for key, value in plan.items())
        if same_batch and prior.get("http_status") in (200, 202):
            return prior
        raise ValueError("Review the existing receipt before retrying a previous submission")

    target = plan["target"]
    name, content = ownership_file(target)
    key_location = f"{SITE}/{name}"
    opener = build_opener(NoRedirect())
    try:
        with opener.open(f"{SITE}/sitemap.xml?revision={target}", timeout=20) as response:
            if response.read() != sitemap:
                raise ValueError("Public sitemap differs from the target commit")
        with opener.open(key_location, timeout=20) as response:
            if response.read().strip() != content.strip():
                raise ValueError("Public IndexNow verification file does not match")
    except (HTTPError, URLError, OSError) as error:
        status = f" (HTTP {error.code})" if isinstance(error, HTTPError) else ""
        raise ValueError(f"Could not verify the public sitemap and ownership file{status}") from None

    request = Request(
        ENDPOINT,
        data=json.dumps({"host": HOST, "key": content.strip().decode(),
                         "keyLocation": key_location, "urlList": plan["urls"]}).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    receipt = dict(plan, status="attempted", attempted_at=datetime.now(timezone.utc).isoformat())
    with receipt_path.open("x", encoding="utf-8") as output:
        json.dump(receipt, output, indent=2)

    try:
        with opener.open(request, timeout=20) as response:
            receipt["http_status"] = response.status
    except HTTPError as error:
        receipt["http_status"] = error.code
        error.close()
    except (URLError, OSError):
        pass

    status = receipt.get("http_status")
    failure = "outcome_unknown" if status is None or status >= 500 else "rejected"
    receipt["status"] = {200: "accepted", 202: "accepted_pending_key_validation"}.get(status, failure)
    temporary = receipt_path.with_suffix(receipt_path.suffix + ".tmp")
    temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    temporary.replace(receipt_path)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="previous live commit")
    parser.add_argument("--target", required=True, help="verified deployed commit")
    parser.add_argument("--urls-from", type=Path, help="additional audited URLs, one per line")
    parser.add_argument("--submit", action="store_true", help="submit the URL batch rather than only listing it")
    parser.add_argument("--receipt", type=Path, help="local submission receipt path outside the website")
    args = parser.parse_args()
    if args.submit and not args.receipt:
        parser.error("--submit requires --receipt")

    try:
        base, target = (git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()
                        for ref in (args.base, args.target))
        if git("show", f"{target}:CNAME").decode().strip() != HOST:
            raise ValueError("Target commit has an unexpected Pages hostname")
        sitemap = git("show", f"{target}:sitemap.xml")
        urls = plan_urls(base, target, sitemap, args.urls_from)
        plan = {"host": HOST, "base": base, "target": target, "url_count": len(urls), "urls": urls}
        result = submit(plan, sitemap, args.receipt) if urls and args.submit else dict(
            plan, status="dry_run" if urls else "no_url_changes"
        )
    except (ElementTree.ParseError, OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    except subprocess.CalledProcessError:
        parser.exit(1, "Could not read the requested commits and website files\n")
    print(json.dumps(result, indent=2))
    return 1 if result["status"] in ("rejected", "outcome_unknown") else 0


if __name__ == "__main__":
    sys.exit(main())
