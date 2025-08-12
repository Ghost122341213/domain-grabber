import re
import time
import random
import string
import requests
from datetime import datetime
from pathlib import Path
from typing import Iterable, Set, Dict, List, Tuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.text import Text

CDX_URL = "https://web.archive.org/cdx/search/cdx"

console = Console()

ASCII_ART = r"""
    ____                                _                   ______                    __      __
   / __ \  ____    ____ ___   ____ _   (_)   ____          / ____/   _____  ____ _   / /_    / /_   ___    _____
  / / / / / __ \  / __ `__ \ / __ `/  / /   / __ \        / / __    / ___/ / __ `/  / __ \  / __ \ / _ \  / ___/
 / /_/ / / /_/ / / / / / / // /_/ /  / /   / / / /       / /_/ /   / /    / /_/ /  / /_/ / / /_/ //  __/ / /
/_____/  \____/ /_/ /_/ /_/ \__,_/  /_/   /_/ /_/        \____/   /_/     \__,_/  /_.___/ /_.___/ \___/ /_/
"""

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]

def make_session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=6,
        connect=3,
        read=3,
        backoff_factor=1.2,
        status_forcelist=(403, 429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({
        "User-Agent": random.choice(UA_POOL),
        "Accept": "text/plain, */*;q=0.1",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    })
    return s

def color_banner():
    banner_text = Text(ASCII_ART, justify="left")
    banner_text.stylize("bold yellow", 1, 120)
    footer = Text("by github.com/bimantaraz", style="bold cyan")
    panel = Panel.fit(
        Text.assemble(banner_text, "\n", footer),
        title="Domain Grabber",
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(panel)

def sanitize_ext_list(raw: str) -> List[str]:
    exts = []
    for token in raw.split(","):
        t = token.strip().lower()
        if not t:
            continue
        t = t.lstrip(".")
        if any(ch for ch in t if ch not in string.ascii_lowercase + ".-"):
            continue
        parts = [p for p in t.split(".") if p]
        if not parts:
            continue
        exts.append(".".join(parts))
    seen = set()
    ordered = []
    for e in exts:
        if e not in seen:
            ordered.append(e)
            seen.add(e)
    return ordered

def host_to_root(host: str, ext: str) -> str:
    ext_dot = f".{ext}"
    if not host.endswith(ext_dot):
        return ""
    parts = host.split(".")
    ext_len = len(ext.split("."))
    if len(parts) < ext_len + 1:
        return ""
    root = ".".join(parts[-(ext_len + 1):])
    return root

def build_params(ext: str, limit_hint: int = None) -> Dict[str, str]:
    params = {
        "url": f"*.{ext}/*",
        "output": "txt",
        "collapse": "urlkey",
        "fl": "original",
    }
    if limit_hint and limit_hint > 0:
        params["limit"] = str(max(1000, limit_hint * 50))
    return params

def rotate_user_agent(session: requests.Session):
    session.headers["User-Agent"] = random.choice(UA_POOL)

def get_roots_for_ext(ext: str, target_count: int, session: requests.Session, progress) -> Tuple[Set[str], int]:
    roots: Set[str] = set()
    attempts = 0
    max_attempts = 4
    backoff = 1.5
    task_id = progress.add_task(f"[cyan]Fetching .{ext}", total=target_count)
    while attempts < max_attempts and len(roots) < target_count:
        params = build_params(ext, limit_hint=target_count)
        try:
            resp = session.get(CDX_URL, params=params, stream=True, timeout=40)
            status = resp.status_code
            if status in (403, 429):
                attempts += 1
                wait = backoff ** attempts + random.uniform(0, 0.7)
                rotate_user_agent(session)
                progress.console.log(f"[bold yellow]Rate limited ({status}) on .{ext} — retry {attempts}/{max_attempts} after {wait:.1f}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                m = re.search(r'https?://([^/\s]+)', line)
                if not m:
                    continue
                host = m.group(1).lower()
                root = host_to_root(host, ext)
                if not root:
                    continue
                if root not in roots:
                    roots.add(root)
                    progress.update(task_id, completed=min(len(roots), target_count))
                    if len(roots) >= target_count:
                        break
            if len(roots) < target_count:
                attempts += 1
                wait = backoff ** attempts + random.uniform(0, 0.5)
                progress.console.log(f"[bold yellow]Got {len(roots)} of {target_count} for .{ext}. Retrying to reach target after {wait:.1f}s")
                time.sleep(wait)
                rotate_user_agent(session)
                continue
        except requests.RequestException as e:
            attempts += 1
            wait = backoff ** attempts + random.uniform(0, 0.7)
            progress.console.log(f"[bold red]Error on .{ext}: {e}. Retry {attempts}/{max_attempts} after {wait:.1f}s")
            time.sleep(wait)
            rotate_user_agent(session)
            continue
        break
    progress.update(task_id, completed=target_count)
    return roots, attempts

def save_results(ext: str, roots: Iterable[str]) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(f"grab_{ext}_{ts}.txt")
    lines = sorted(set(roots))
    out.write_text("\n".join(lines), encoding="utf-8")
    return out

def show_summary(results: Dict[str, Tuple[Path, int, int]]):
    table = Table(title="Summary", show_lines=False, header_style="bold magenta")
    table.add_column("Extension", style="cyan", justify="left")
    table.add_column("Saved file", style="green", justify="left")
    table.add_column("Found", style="yellow", justify="right")
    table.add_column("Retries", style="red", justify="right")
    for ext, (path, found, retries) in results.items():
        table.add_row(f".{ext}", str(path), str(found), str(retries))
    console.print(table)

def main():
    color_banner()
    console.print(Panel.fit(
        "Enter extensions (comma-separated). Example: [bold]id, co.id, ac.id, go.id[/bold]\n"
        "Target count is per extension.",
        title="Input",
        border_style="blue",
    ))
    raw_exts = Prompt.ask("Extensions", default="id, co.id, ac.id")
    exts = sanitize_ext_list(raw_exts)
    if not exts:
        console.print("[bold red]No valid extensions. Exiting.[/bold red]")
        return
    try:
        target = int(Prompt.ask("Number of root domains per extension", default="50"))
        if target <= 0:
            raise ValueError
    except ValueError:
        console.print("[bold red]Count must be a positive integer.[/bold red]")
        return
    cautious = Confirm.ask("Cautious mode (extra small delay)?", default=True)
    with Progress(
        SpinnerColumn(style="magenta"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        session = make_session()
        results: Dict[str, Tuple[Path, int, int]] = {}
        for ext in exts:
            if cautious:
                time.sleep(0.5 + random.uniform(0, 0.5))
            roots, retries = get_roots_for_ext(ext, target, session, progress)
            time.sleep(0.2 + random.uniform(0, 0.3))
            out_path = save_results(ext, roots)
            results[ext] = (out_path, len(roots), retries)
            console.print(Panel.fit(
                f".{ext}: Saved [bold green]{len(roots)}[/bold green] root-domains to\n[bold]{out_path}[/bold]",
                title=f".{ext} complete",
                border_style="green" if len(roots) >= max(5, target // 2) else "yellow",
            ))
    show_summary(results)
    console.print(Panel.fit(
        "Tips:\n"
        "- Use more specific extensions (e.g., co.id, ac.id, go.id) if .id often gets 403/429.\n"
        "- Increase the number gradually to avoid rate limiting.\n"
        "- Run again at a different time if limited.",
        title="Suggestions",
        border_style="cyan",
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Cancelled by user.[/bold red]")
