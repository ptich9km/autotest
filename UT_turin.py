import unittest
import time
import Promwadserial


class Turin_Test(unittest.TestCase):

    def setUp(self):
        Promwadserial.try_connect_to_board(115200, 5)
        Promwadserial.sendCmd('root' + '\r\n')
        time.sleep(3)
        Promwadserial.sendCmd('root' + '\r\n')

    #@unittest.skip("skipping")
    def test_pwd(self):
        """pwd operation test"""
        print("id: " + self.id())
        time.sleep(3)
        self.assertEqual(Promwadserial.sendCmd('pwd' + '\r\n'), ['/root'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(Turin_Test('test_pwd'))


    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    Promwadserial.Close_serial_board()