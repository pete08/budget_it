import unittest
import main.fullfilelistpdf as list

listfiles_0 = ['123.pdf','foo/bar/ready_for.pdf','foobartwo.pdf','123.df','111.f','practicepiecepd.f','']
listfiles_1 = ['123.xlsx','foo/bar/ready_for.csv','foobartwo.doc','123.docx','pdf.pdf', "pdf.xlsx"]

class Testpdflist(unittest.TestCase):
    def test_listpdffiles(self):
        # x = cpc.Graphit("/Users/peter/Desktop/Programming/budget_it","spendcsv_.csv")
        x = list.fulldirpdffiles(listfiles_0,dirPath="/users")
        print(x)
        self.assertEqual(len(x), 3)
        # for i in filesearch:
        #     self.assertIn(i, '.pdf')


if __name__ == "__main__":
    unittest.main()

