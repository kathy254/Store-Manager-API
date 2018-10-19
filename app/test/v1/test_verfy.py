import unittest


from app.api.v1.model.verify import Verify


class TestVerify(unittest.TestCase):
	def setUp(self):
		self.obj = Verify()
	
	
	def tearDown(self):
		self.obj = None
		
		
	def test_is_empty(self):
		test = self.obj.is_empty(['', 'dress'])
		self.assertTrue(test)
		def test_is_not_empty(self):
			test = self.obj.is_empty(['suit', 'suit'])
			self.assertFalse(test)
			
	
	def test_whitespace(self):
		test = self.obj.is_whitespace([' ', 'm'])
		self.assertTrue(test)
		
	
	def test_no_whitespace(self):
		test = self.obj.is_whitespace(['k', 'lm'])
		self.assertFalse(test)
		
		
	def test_not_payload(self):
		payload = {'name':'Gucci dress','moq':3,'quantity':0,'qwr':0}
		payload_2 = {'name':'Gucci dress','moq':3}
		payload_3 = {'name':'Gucci dress','moq':3,'quantity':0,'category':0,'we':0}
		test = self.obj.is_product_payload(payload)
		test_2 = self.obj.is_product_payload(payload_2)
		test_3 = self.obj.is_product_payload(payload_3)
		self.assertFalse(test)
		self.assertFalse(test_2)
		self.assertFalse(test_3)


if __name__ == '__main__':
    unittest.main()  
