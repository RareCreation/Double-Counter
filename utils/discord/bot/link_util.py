import os

GLOBAL_LINK_FILE = "link/link.txt"
SERVER_LINK_FILE = "link/links.txt"


def format_link(link: str) -> str:
    link = link.strip()
    if not link.startswith(("http://", "https://")):
        link = "https://" + link
    return link


def load_global_link() -> str:
    if not os.path.exists(GLOBAL_LINK_FILE):
        return "https://example.com"

    with open(GLOBAL_LINK_FILE, "r", encoding="utf-8") as f:
        return format_link(f.read())


def load_server_links() -> dict:
    links = {}
    if not os.path.exists(SERVER_LINK_FILE):
        return links

    with open(SERVER_LINK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue
            gid, link = line.strip().split("|", 1)
            links[int(gid)] = link
    return links


def save_server_links(links: dict):
    os.makedirs(os.path.dirname(SERVER_LINK_FILE), exist_ok=True)
    with open(SERVER_LINK_FILE, "w", encoding="utf-8") as f:
        for gid, link in links.items():
            f.write(f"{gid}|{link}\n")


def get_link_for_guild(guild_id: int) -> str:
    server_links = load_server_links()
    if guild_id in server_links:
        return server_links[guild_id]

    return load_global_link()
