from typing import Optional
import json
import os
import csv

import requests
from bs4 import BeautifulSoup


class Parser:
    domain = "https://ru.wikipedia.org/"
    main_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    from_url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&from="

    def run_parser(self):
        alph = self._get_alphabet()
        data = {}
        for l in alph:
            count = self._get_animals_by_alph(letter=l)
            data[l] = count
            print(f"Letter: '{l}' | Count: {count}")
        
        with open("task2/beasts.json", "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # with open("task2/beasts.csv", "w", newline="") as f:
        #     w = csv.DictWriter(f, data.keys())
        #     w.writeheader()
        #     w.writerow(data)

        with open("task2/beasts.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for key, value in data.items():
                writer.writerow([key, value])

    def _get_animals_by_alph(self, letter: str) -> int:
        url = f"{self.from_url}{letter}"
        count = 0
        while True:
            response = self._get(url=url)
            if not response:
                print(f"[ERROR] :: response: {response} | url: {url}")
                continue
            soup = BeautifulSoup(response.text, "lxml")

            mw_div = soup.find("div", attrs={"id": "mw-pages"})
            next_page_a = mw_div.find_all("a")
            if not next_page_a:
                print("[ERROR] :: not next_page_a")
                continue
            
            mw_category_columns = mw_div.find("div", attrs={"class": "mw-category mw-category-columns"})
            if not mw_category_columns:
                print("[ERROR] :: not mw_category_columns")
                continue
            
            mw_category_group = mw_category_columns.find("div", attrs={"class": "mw-category-group"})
            if not mw_category_group:
                print("[ERROR] :: not mw_category_group")
                continue
            
            h = mw_category_group.find("h3")
            if not h or h.text.strip() != letter:
                break

            lis = mw_category_group.find_all("li")

            count += len(lis)

            next_page_a = f"{self.domain}{next_page_a[-1].get('href')}"
            url = next_page_a
        return count
        

    def _get_alphabet(self) -> Optional[list]:
        if os.path.exists("task2/alphabet.json"):
            with open("task2/alphabet.json", "r") as f:
                alph = json.load(f)
                return alph

        response = self._get(self.main_url)
        if not response:
            return None
        soup = BeautifulSoup(response.text, "lxml")
        uls = soup.find_all("ul", attrs={"class": "ts-module-Индекс_категории-multi-items"})
        alph = [i.find("li").text for i in uls]

        with open("task2/alphabet.json", "w") as f:
            json.dump(alph, f, ensure_ascii=False, indent=2)
        return alph

    def _get(self, url: str) -> Optional[requests.Response]:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        response = requests.get(url=url, headers=headers)
        if response and response.status_code == 200:
            return response
        return None


def main():
    parser = Parser()
    parser.run_parser()


if __name__ == "__main__":
    main()