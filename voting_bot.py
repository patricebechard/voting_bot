#!/usr/bin/python
# -*- coding: utf-8 _*_

import os, sys
import getopt
from selenium import webdriver
from urllib.request import urlopen
from urllib.error import URLError
from html.parser import HTMLParser

"""
This code let's you vote a certain number of times for a given target on a survey
given a starting url. The code finds the survey and votes for the target, then
reloads the page NVOTES times.
"""

NVOTES = 10000

default_url = 'http://ici.radio-canada.ca/premiere/emissions/plus-on-est-de-fous-plus-on-lit'
#default_target = 'Misa'
default_target = '41473'

class SurveyParser(HTMLParser):
	"""We modify and add some methods for the HTMLParser class"""
    
	def handle_starttag(self, tag, attrs):
		"""
		This is a function that HTMLParser normally has but we are adding some 
		functionality to it.
		"""

		if tag == 'iframe':
			# We are looking for the link to the survey box to vote
			for (key, value) in attrs:
				if key == 'src':
					self.links = self.links + [value]

	def find_survey_url(self, url):
		"""New function to find the survey url on the initial webpage"""
		self.links = []
		self.survey_url = ''
		response = urlopen(url)

		try:
			htmlBytes = response.read()
			htmlString = htmlBytes.decode('utf-8')
			self.feed(htmlString)

			if len(self.links) != 0:
				self.survey_url = self.links[0]		#we only keep the first link
			return self.survey_url

		except:
			print('error')
			return ''

	#new function to vote for option
	def vote_for_option(self, driver, url, target):
		"""New function to choose option to vote for and repeat NVOTES times"""

		driver.get(url)

		select = driver.find_elements_by_css_selector\
								("input[type='radio'][value='%s']"%target)
		select[0].click()
		submit = driver.find_element_by_name("btnSubmit")
		submit.click()

		for i in range(NVOTES):
			driver.refresh()

def handle_arguments():
	"""Function to handle arguments given in command line"""

	fullCmdArguments = sys.argv			#read command line arguments first
	argumentList = fullCmdArguments[1:]
	user_inputs = True

	unixOptions = 'd'
	gnuOptions = ['default']

	try:
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
	except getopt.error as err:
		#output error, and return with an error code
		print(str(err))
		sys.exit(2)

	for currentArgument, currentValue in arguments:
		if currentArgument in ('-d', '--default'):
			user_inputs = False

	return user_inputs

def vote(url,target):
	"""high level function to vote for option"""

	driver = webdriver.Chrome()

	try :
		parser = SurveyParser()
		survey_url = parser.find_survey_url(url)
		parser.vote_for_option(driver,survey_url,target)

	except:
		raise URLError ('URL is not valid')

	driver = close()


if __name__ == '__main__':

	user_inputs = handle_arguments()

	if user_inputs:
		url = input('Enter URL of page :')
		target = input('Entrer la cible du vote :')	
	else:
		url = default_url
		target = default_target		

	vote(url,target)
