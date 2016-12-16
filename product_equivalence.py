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

class ProdEqualError(Exception):
	"""base class for custom exception for ProdEqual related errors"""
	def __init__(self, message):
		self.message = __class__.__name__+': '+message
	
class ZincAPIError(ProdEqualError):
	"""custom exception for Zinc API related errors"""
	pass

class ProdEqualInternalError(ProdEqualError):
	"""custom exception for ProdEqual internal errors"""
	pass

class ProdEqualHttpRequestError(ProdEqualError):
	"""custom exception for http request errors"""
	pass

class product_equivalence:
	
	_AUTH_KEY = 'A2984FCCADEC3B7AE3159DCB'
	_API_STRING = 'https://api.zinc.io/v1/products/{prod_id}?retailer={market_place}'
	_ok_status = 200;


	def are_products_identical(self, market_p1, product_id1, market_p2, product_id2):
		""" main method which checks the equivalence of two products
			returns: boolean value
		"""
		#retrieve data from the Zinc Api
		prod1_obj = self.retrive_data(market_p1,product_id1)
		prod2_obj = self.retrive_data(market_p2,product_id2)

		prod1_index = {}
		prod2_index = {}

		if(prod1_obj and prod2_obj):

			#create indexes to compare values of each product
			prod1_index = self.create_product_index(prod1_obj)
			prod2_index = self.create_product_index(prod2_obj)

			standard_epids = ['ISBN','UPC','MPN']

		elif(prod1_obj == None or prod2_obj == None):
			return None

		#if both products have search indexes
		if(prod1_index and prod2_index):	
			for epid in standard_epids:
				if(epid in prod1_index.keys() and epid in prod2_index.keys()):
					if(prod1_index[epid] == prod2_index[epid]):
						return True

		return False


	def create_product_index(self,prod_obj):
		"""creates a searchable product details index -return dictionary of product details
			returns: product details indexed in a dictionary
		"""
		MPN_alias = 'Item model number'
		
		# key for the MPN_alias value in the search index
		MPN_second = 'MPN'

		#search index
		prod_index = {}

		# add the epids to the search index
		if('epids' in prod_obj):
			for item in prod_obj['epids']:
				prod_index[item['type']] = item['value'].strip()

		# add the product details to the search index
		if ('product_details' in prod_obj):
			prod1_details_list = prod_obj['product_details'];

			#extracting the items in product details which match the value in MPN_alias
			prod_MPN_value = [prod_item for prod_item in prod1_details_list if MPN_alias in prod_item]
			
			#if exists, format the first MPN_alias value and replace it for MPN
			if(prod_MPN_value and MPN_second not in prod_index.keys()):
				prod_index[MPN_second] = prod_MPN_value[0].split(":")[1].strip()

		return prod_index

 
	def retrive_data(self, market_p, product_id):
		""" retrives the product data from the Zinc API
			returns: dictionary with all the details of the product
		"""
		#creating the request url for product
		prod_request = self._API_STRING.replace('{prod_id}',product_id)
		prod_request = prod_request.replace('{market_place}',market_p)
		
		try:
			#api response for product name
			prod_response = requests.get(prod_request,auth = (self._AUTH_KEY,''))
		except KeyboardInterrupt:
			exit()
		except:
			raise ProdEqualHttpRequestError('bad request')

		#data object to be returned
		prod_obj = None

		if(prod_response.status_code == self._ok_status):
			
			#parse response to python object
			try:
				prod_obj = prod_response.json()

				if(prod_obj['status'] == 'failed'):
					raise ZincAPIError('Unable to fetch product data from the Zinc API.'+
										' Make sure the product_id and the market_place values are correct.')
			except ValueError:
				raise ProdEqualInternalError('Cannot load the product details due to an internal error (json issue)')
		
		return prod_obj
