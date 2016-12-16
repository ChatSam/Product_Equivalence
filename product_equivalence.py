"""
This module accepts the product ids from two different marketplaces 
and returns a boolean indicating if the products are identical

Author: Chatura Samarasinghe

Invocation:
	Prod = product_equivalence()
	are_products_identical(market_place1, product_id1, market_place2, product_id2)
"""

import requests
import json
from collections import Counter 


class product_equivalence:
	""" main method which checks the equivalence of two products
		return - boolean
	"""
	
	_auth_key = 'A2984FCCADEC3B7AE3159DCB'
	_api_string = 'https://api.zinc.io/v1/products/{prod_id}?retailer={market_place}'
	_ok_status = 200;

	def are_products_identical(self, market_p1, product_id1, market_p2, product_id2):

		#retrieve data from the Zinc Api
		prod1_obj = self.retriveData(market_p1,product_id1)
		
		prod2_obj = self.retriveData(market_p2,product_id2)

		prod1_index = {}

		prod2_index = {}

		if(prod1_obj and prod2_obj):
			#create indexes to compare values of each product
			prod1_index = self.create_product_index(prod1_obj)

			prod2_index = self.create_product_index(prod2_obj)

			standard_epids = ['ISBN','UPC','MPN']

		#if both products have search indexes
		if(prod1_index and prod2_index):
			
			for epid in standard_epids:
				#print(prod1_epids.keys())
				#print(prod2_epids)

				if(epid in prod1_index.keys() and epid in prod2_index.keys()):
					if(prod1_index[epid] == prod2_index[epid]):
						#print ("prod1 {0} | prod2 {1}".format(prod1_epids[epid],prod2_epids[epid] ))
						return True

		return False


	def create_product_index(self,prod_obj):
		"""creates a searchable product details index -return dictionary of product details
			return - product details index dictionary
		"""

		MPN_alias = 'Item model number'

		# key for the MPN_alias value in the search index
		MPN_second = 'MPN_second'

		#search index
		prod_index = {}

		# add the product details to the search index
		if ('product_details' in prod_obj):

			prod1_details_list = prod_obj['product_details'];

			#extracting the items in product details which match the value in MPN_alias
			prod_MPN_value = [prod_item for prod_item in prod1_details_list if MPN_alias in prod_item]

			#if exists, format the first MPN_alias value and add it to the search index
			if(prod_MPN_value):
 
				prod_index[MPN_second] = prod_MPN_value[0].split(":")[1].strip()

		# add the epids to the search index
		if('epids' in prod_obj):

			for item in prod_obj['epids']:

				prod_index[item['type']] = item['value'].strip()

		return prod_index

 
	def retriveData(self, market_p, product_id):
		""" retrives the product data from the Zinc API
			return - dictionary with all the details of the product
		"""

		#creating the request url for product
		prod_request = self._api_string.replace('{prod_id}',product_id)
		prod_request = prod_request.replace('{market_place}',market_p)

		#response for prod1
		prod_response = requests.get(prod_request,auth = (self._auth_key,''))

		prod_obj = None

		if(prod_response.status_code == self._ok_status):
			#parse response to python object
			try:
				prod_obj = prod_response.json()
			except ValueError:
				print ('cannot load the product details due to json error')
		else:
			#todo: write a proper request
			print("Error in the request")
			exit()

		return prod_obj


Prod = product_equivalence()
#print(Prod.are_products_identical("bhphotovideo","1223091-REG","amazon","B007W5B7IK"))
print(Prod.are_products_identical("bhphotovideo","1148315-REG","amazon","B00PB1K3KA"));
#Prod.are_products_identical("bhphotovideo","1146603-REG","amazon","B007B5TMW4")


