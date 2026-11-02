"""Word and Excel files written and read back with the standard library only (office.py)."""
import io
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import office  # noqa: E402


class WordTest(unittest.TestCase):
    def test_markdown_to_word_and_back(self):
        doc = office.markdown_to_docx("# Launch plan\n\nOpen in **March**.\n\n- Hire a barista\n- Sign the lease\n\n"
                                      "| Month | Cost |\n| --- | --- |\n| March | £4,000 |")
        text = office.docx_text(doc)
        for part in ("Launch plan", "Open in March.", "Hire a barista", "Sign the lease", "March | £4,000"):
            self.assertIn(part, text)

    def test_odd_characters_survive(self):
        text = office.docx_text(office.markdown_to_docx("Tom & Jerry <script> \"quotes\" café"))
        self.assertIn('Tom & Jerry <script> "quotes" café', text)


class ExcelTest(unittest.TestCase):
    def sheet(self, csv_text):
        with zipfile.ZipFile(io.BytesIO(office.csv_to_xlsx(csv_text))) as zf:
            return zf.read("xl/worksheets/sheet1.xml").decode("utf-8")

    def test_numbers_money_percentages_and_formulas(self):
        xml = self.sheet("Item,Cost,Share\nRent,\"£1,200\",40%\nStock,800,25%\nTotal,=SUM(B2:B3),")
        self.assertIn("<v>1200</v>", xml)          # £1,200 is stored as a number...
        self.assertIn("<v>0.4</v>", xml)           # ...and 40% as 0.4, each with its format
        self.assertIn("<f>SUM(B2:B3)</f>", xml)    # a live formula, not text

    def test_ids_with_leading_zeros_stay_text(self):
        self.assertIn("07700900123", self.sheet("Name,Phone\nAna,07700900123"))
        self.assertNotIn("<v>7700900123</v>", self.sheet("Name,Phone\nAna,07700900123"))

    def test_excel_read_back(self):
        text = office.xlsx_text(office.csv_to_xlsx("Item,Cost\nRent,1200\nStock,800"))
        self.assertIn("Rent", text)
        self.assertIn("1200", text)


if __name__ == "__main__":
    unittest.main()
