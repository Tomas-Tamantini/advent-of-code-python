import http.client


def fetch_problem_name(year: int, day: int) -> str:
    conn = http.client.HTTPSConnection("adventofcode.com")
    conn.request("GET", f"/{year}/day/{day}")
    response = conn.getresponse()
    html = response.read().decode("utf-8")
    conn.close()
    start = html.find("<h2>")
    end = html.find("</h2>")
    header = html[start + 4 : end]
    return header.split(":")[1].replace("---", "").strip()
