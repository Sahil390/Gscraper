import json
import os
from scraper.crowler import get_links
from scraper.parser import parse_course

def main():
    print("start...\n")

    links = get_links()
    print(f"got {len(links)} links\n")

    out = []

    for i, u in enumerate(links, 1):
        print(f"[{i}/{len(links)}] {u}")

        try:
            d = parse_course(u)
            out.append(d)
        except Exception as e:
            print("err:", e)

    os.makedirs("output", exist_ok=True)

    with open("output/data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)

    print("\ndone -> output/data.json")


if __name__ == "__main__":
    main()