import unittest
import main.fullfilelistpdf as list
import main.pullpagestrxns as pages

listfiles_0 = ['123.pdf','foo/bar/ready_for.pdf','foobartwo.pdf','123.df','111.f','practicepiecepd.f','']
listfiles_1 = ['123.xlsx','foo/bar/ready_for.csv','foobartwo.doc','123.docx','pdf.pdf', "pdf.xlsx"]
test_length_pdf_lines = ["12/01 NC 0.00","12/01 0.00", "123.12 10/01", "-13.12 10/01", "payment 1.00/01", "/123/2 wat /1.00"]
test_trxn_line_ends_5 = ["12/01 NC 0.00","12/01 0.0032", "123.12 10/01.00", "-13.12 10/01.23", "payment 123.1", "///alkwe/123/2 wat /1", "23423.12", "nyc transfer 124,234.122", "nyc transfer 124,234.2", "nyc transfer 124,234.12", "nyc transfer 124,234,12"]

class Testpdflist(unittest.TestCase):
    def test_listpdffiles(self):
        x = list.fulldirpdffiles(listfiles_0,dirPath="/users")
        print(x)
        self.assertEqual(len(x), 3)
        
    def test_trxn_line_length(self):
        x = pages.transactionList(test_length_pdf_lines, stmtyear="2022-01")
        self.assertFalse(len(x) < 0)

    def test_trxn_line_end(self):
        x = pages.transactionList(test_trxn_line_ends_5, stmtyear="2022-01")
        self.assertFalse(len(x) == 5)



if __name__ == "__main__":
    unittest.main()

