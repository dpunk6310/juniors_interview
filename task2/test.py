import unittest
from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup

from solution import Parser


class TestParser(unittest.TestCase):

    @patch("solution.requests.get")
    def test_get_alphabet_from_network(self, mock_get):
        """Проверяем загрузку алфавита с сети."""
        mock_html = """
        <ul class="ts-module-Индекс_категории-multi-items">
            <li>А</li>
            <li>Б</li>
        </ul>
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        solution = Parser()
        alphabet = solution._get_alphabet()

        self.assertEqual(alphabet[0:2], ["А", "Б"])

    def test_run_parser(self):
        """Подсчёт животных по букве
        """

        parser = Parser()
        
        alph = parser._get_alphabet()
        for l in alph[:2]:
            url = f"{parser.from_url}{l}"
            count = 0
            while True:
                response = parser._get(url=url)
                if not response:
                    print(f"[ERROR] :: response: {response} | url: {url}")
                    continue
                self.assertEqual(response.status_code, 200)
                soup = BeautifulSoup(response.text, "lxml")

                mw_div = soup.find("div", attrs={"id": "mw-pages"})
                self.assertTrue(mw_div)

                next_page_a = mw_div.find_all("a")
                self.assertTrue(next_page_a)

                mw_category_columns = mw_div.find("div", attrs={"class": "mw-category mw-category-columns"})
                self.assertTrue(mw_category_columns)
                
                mw_category_group = mw_category_columns.find("div", attrs={"class": "mw-category-group"})
                self.assertTrue(mw_category_group)
                
                h = mw_category_group.find("h3")
                if not h or h.text.strip() != l:
                    self.assertNotEqual(h.text.strip(), l)
                    break

                lis = mw_category_group.find_all("li")
                self.assertTrue(lis)

                count += len(lis)

                next_page_a = f"{parser.domain}{next_page_a[-1].get('href')}"
                url = next_page_a



if __name__ == "__main__":
    unittest.main()
