import unittest
import time
import Promwadserial


def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)

        return callHelper

    return repeatHelper

class Elne_Test(unittest.TestCase):

    def setUp(self):
        Promwadserial.try_connect_to_board(9600, 5)

    #@unittest.skip("skipping")
    def test_ON_RELAY(self):
        """ON_RELAY operation test"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.ON_RELAY)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.ON_RELAY), ['0xaa', '0x39', '0x0', '0x3'])

    #@unittest.skip("skipping")
    def test_OFF_RELAY(self):
        """OFF_RELAY operation test"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.OFF_RELAY)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.OFF_RELAY), ['0xaa', '0x3a', '0x0', '0x56'])

    #@unittest.skip("skipping")
    def test_REQ_CAPACITY(self):
        """REQ_CAPACITY operation test"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.REQ_CAPACITY)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.REQ_CAPACITY), ['0xaa', '0x37', '0x5', '0xff', '0x0', '0x0', '0x0', '0x0', '0x13'])

    #@unittest.skip("skipping")
    def test_SETUP_CAPACITY(self):
        """SETUP_CAPACITY operation test"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.SETUP_CAPACITY)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.SETUP_CAPACITY), ['0xaa', '0x38', '0x0', '0xc7'])

    #@unittest.skip("skipping")
    @unittest.expectedFailure
    def test_SAVE_LOG(self):
        """SAVE_LOG operation test- Request is not good fail after operation"""
        print("id: " + self.id())
        time.sleep(0.5)
        Promwadserial.Linda('send', Promwadserial.SAVE_LOG)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.SAVE_LOG), ['0xaa', '0x35', '0x0', '0x4e'])

    #@unittest.skip("skipping")
    @unittest.expectedFailure
    def test_RESTORE_LOG(self):
        """RESTORE_LOG operation test"""
        print("id: " + self.id())
        time.sleep(0.5)
        Promwadserial.Linda('send', Promwadserial.RESTORE_LOG)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.RESTORE_LOG), ['0xaa', '0x36', '0x2d', '0x0', '0x18', '0x13', '0x8', '0x3', '0x10', '0x25', '0x13', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0xa', '0x1a', '0xcd', '0xcc', '0xcc', '0x40', '0x0', '0x0', '0x60', '0x40', '0x25', '0x28', '0xb8', '0xb', '0x0', '0x0'])

    #@unittest.skip("skipping")
    def test_REQ_SERIAL(self):
        """REQ_SERIAL operation test - Request is not good 3 byte 0x0 - 0x6"""
        print("id: " + self.id())
        time.sleep(5)
        Promwadserial.Linda('send', Promwadserial.REQ_SERIAL)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.REQ_SERIAL), ['0xaa', '0x34', '0x6', '0xd9', '0xff', '0xff', '0xff', '0xff', '0xff'])

    #@unittest.skip("skipping")
    def test_REQ_UID(self):
        """REQ_UID operation test- Request is not good device going down"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.REQ_UID)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.REQ_UID), ['0xaa', '0x31', '0x8', '0x1', '0x0', '0x0', '0x0', '0x1', '0x0', '0x0', '0x0'])

    #@unittest.skip("develop skipping")
    def test_CLEAR_UID(self):
        """On relay operation test"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.CLEAR_UID)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.CLEAR_UID), ['0xaa', '0x33', '0x0', '0xe4'])

    #@unittest.skip("develop skipping")
    def test_SETUP_UID(self):
        """On relay operation test"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.SETUP_UID)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.SETUP_UID), ['0xaa', '0x32', '0x0', '0x20'])

    #@unittest.skip("skipping")
    def test_REQ_UUID(self):
        """REQ_UUID operation test-  Request is not good 3 byte 0x0 - 0x17"""
        print("id: " + self.id())
        time.sleep(3)
        Promwadserial.Linda('send', Promwadserial.REQ_UUID)
        self.assertEqual(Promwadserial.Linda('read', Promwadserial.REQ_UUID), ['0xaa', '0x30', '0x17', '0xd9', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff'])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(Elne_Test('test_SETUP_UID'))
    suite.addTest(Elne_Test('test_ON_RELAY'))
    suite.addTest(Elne_Test('test_OFF_RELAY'))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
    Promwadserial.Close_serial_board()