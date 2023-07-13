import unittest
from train_new import train

class TestTrain(unittest.TestCase):
    def test_train(self):
        result = train()
        self.assertGreater(result, 85)

if __name__ == "__main__":
    unittest.main()
