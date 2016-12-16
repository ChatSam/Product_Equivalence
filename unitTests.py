"""
Test file for product_equivalence module
Author: Chatura Samarasinghe

"""

import product_equivalence

filename = "bhphotovideo_to_asin_examples.txt "
#filename ="test3.txt"

def initializeForTest():

	file = open(filename)

	testList = list(file)

	count = 0;

	passed = 0

	failed = 0

	for item in testList:
		
		test = item.strip()

		if(test):
			count += 1

			testUnit =test.split()


			prodEq = product_equivalence.product_equivalence()

			#invoke function
			prod_test_run = prodEq.are_products_identical(testUnit[0],testUnit[1],testUnit[2],testUnit[3])

			if(prod_test_run):
				print("test case: {0} | output {1}".format(count,prod_test_run))
				passed += 1		

			else:
				print ("test case: {0} | output {1} -> bhphotovideo {2} amazon {3}".format(count, prod_test_run, testUnit[1], testUnit[3]))
				failed += 1

	accuracy = float((passed/count) * 100)

	print ("passed: {0} | failed: {1} | est accuracy: {2}%".format(passed, failed, accuracy))

	file.close()



initializeForTest()