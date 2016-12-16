"""
Test file for product_equivalence module
Author: Chatura Samarasinghe

"""
import product_equivalence as pro
import unittest

class TestProductEquivalence(unittest.TestCase):

	prod_eql = pro.product_equivalence()

	#runs the test cases from the primary test file
	def test_run_primary(self):		
		passed = 0
		failed = 0
		#filename = "bhphotovideo_to_asin_examples.txt"
		filename = "test2.txt"
		testCases = self.initialize_for_test(filename)

		print("running main test - {0} testcases ...".format(len(testCases)))

		for testUnit in testCases:

			try:
				prod_test_run = self.prod_eql.are_products_identical(testUnit[0],testUnit[1],testUnit[2],testUnit[3])
				test_no = testCases.index(testUnit) + 1

				self.assertTrue(prod_test_run)

			except AssertionError as err:
				print ("test case: {0} | output {1} -> bhphotovideo {2} amazon {3}"
					.format(test_no, prod_test_run, testUnit[1], testUnit[3]))
				failed += 1
			
			except pro.ProdEqualError as err:
				print(err.message)

			else:
				print("test case: {0} | output {1}".format(test_no,prod_test_run))
				passed += 1

		print ("passed: {0} | failed: {1}".format(passed, failed))

	#tests for custom exception
	def test_run_excep(self):

		testUnit = ["bhphotovideo","AAAAA114835-REG","amazon","B00PB1K3KA"]

		try:
			prod_test_run = self.prod_eql.are_products_identical(testUnit[0],testUnit[1],testUnit[2],testUnit[3])
		except pro.ProdEqualError:
			self.assertTrue(True)
			pass
		else:
			self.assertTrue(False)
			pass

	#loads the testcase from file
	def initialize_for_test(self,filename):
		testCases = []
		file = open(filename)
		testList = list(file)

		for item in testList:		
			test = item.strip()

			if(test):
				testUnit =test.split()

				testCases.append(testUnit)		

		file.close()

		return testCases

if __name__ == '__main__':
    unittest.main()
