#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


import numpy as np
import scipy.stats
import sys
from colorama import init, Fore, Back, Style
from texttable import Texttable


# https://github.com/bufordtaylor/python-texttable



def test1():
	# -37, 26.5, 15 --> -2.86%
    # http://www.morningstar.es/es/news/31047/Para-novatos-Rentabilidad-anualizada.aspx
	pass


def porcentaje(value,percentage):
    return value * percentage / 100


def calculateGeoMeanPorcentaje(ppt):

	mediageom = scipy.stats.mstats.gmean(ppt)
	result = float(mediageom) - 1
	result = result * 100
	result = "{0:.2f}".format(result)

	return result

def print_header_script():
	print "\n\n"
	print (Fore.CYAN + "                        AFIT - Analityc Financial Index Tool")

def print_header():

	TEXT_COLUMN_1 = "Year"
	TEXT_COLUMN_2 = "MSCI Word"
	TEXT_COLUMN_3 = "Value"
	TEXT_COLUMN_4 = "Benef."
	TEXT_COLUMN_5 = "Infl."
	TEXT_COLUMN_6 = "Crisis"

	c1 = format_value_cell(TEXT_COLUMN_1,ROW_WITH_COLUMN_1) 
	c2 = format_value_cell(TEXT_COLUMN_2,ROW_WITH_COLUMN_2)
	c3 = format_value_cell(TEXT_COLUMN_3,ROW_WITH_COLUMN_3)
	c4 = format_value_cell(TEXT_COLUMN_4,ROW_WITH_COLUMN_4)
	c5 = format_value_cell(TEXT_COLUMN_5,ROW_WITH_COLUMN_5)
	c6 = format_value_cell(TEXT_COLUMN_6,ROW_WITH_COLUMN_6)

	print(Fore.WHITE + " " + SECTION_SEPARATOR)
	print(Fore.BLUE + " " + c1 + c2 + c3 + c4 + c5 + c6)
	print(Fore.WHITE + " " + SECTION_SEPARATOR)

def print_row(clave,valor,money_value,percentaje_money_value,inflaction,crisis):

	truncate_perc_value = "{0:.2f}".format(percentaje_money_value)
	truncate_perc_value = str(truncate_perc_value)
	truncate_value = str("{0:.2f}".format(money_value))

	# Format cell
	c1 = format_value_cell(clave,ROW_WITH_COLUMN_1)
	c2 = format_value_cell(valor,ROW_WITH_COLUMN_2)
	c3 = format_value_cell(truncate_value,ROW_WITH_COLUMN_3)
	c4 = format_value_cell(truncate_perc_value,ROW_WITH_COLUMN_4)
	c5 = format_value_cell(inflaction,ROW_WITH_COLUMN_5)
	c6 = format_value_cell(crisis,ROW_WITH_COLUMN_6)

	if float(valor) > 0:
		print(Fore.GREEN + " " + c1 + c2 + c3 + c4 + c5 + c6)
	else:
		print(Fore.RED + " " + c1 + c2 + c3 + c4 + c5 + c6)


def format_value_cell(value,row_with):

	diff = row_with - len(str(value))
	for x in range(diff):
		value = value + " "

	return value

def get_map_inflaction():

	d = {}

	file_inflaction = open(INFLACTION_FILE,'r')

	# Save items in dictionary
	for item in file_inflaction:
		(year,value) = item.split()
		d[year] = value[:-1]

	return d

def get_map_crisis():

	d = {}

	file_crisis = open(CRISIS_FILE,'r')

	# Save items in dictionary
	for item in file_crisis:
		(year,value) = item.split('|')
		d[year] = value[:-1]

	return d

def global_variable():

	global DEFAULT_INIT_MONEY_VALUE
	global MONEY
	global ROW_WITH_COLUMN_1
	global ROW_WITH_COLUMN_2
	global ROW_WITH_COLUMN_3
	global ROW_WITH_COLUMN_4
	global ROW_WITH_COLUMN_5
	global ROW_WITH_COLUMN_6
	global SECTION_SEPARATOR
	global CRISIS_FILE
	global INFLACTION_FILE
	global MSCI_WORD_FILE

	DEFAULT_INIT_MONEY_VALUE = 1000
	MONEY = '€'

	ROW_WITH_COLUMN_1 = 7
	ROW_WITH_COLUMN_2 = 15
	ROW_WITH_COLUMN_3 = 16
	ROW_WITH_COLUMN_4 = 15
	ROW_WITH_COLUMN_5 = 8
	ROW_WITH_COLUMN_6 = 20

	CRISIS_FILE = "/home/miguelgranadino/github/datascience/spain_crisis.txt"
	INFLACTION_FILE = "/home/miguelgranadino/github/datascience/spain_inflaction.txt"
	MSCI_WORD_FILE = "/home/miguelgranadino/github/datascience/msci_world_data.txt"

	SECTION_SEPARATOR = "-----------------------------------------------------------------------------"

# --------------------------------------------------------------------
#  MAIN
# --------------------------------------------------------------------
if __name__ == '__main__':

	global_variable()

	print_header_script()


	# Init diccionary
	datos = {}
	init_money_value = DEFAULT_INIT_MONEY_VALUE


	map_inflaction = get_map_inflaction()
	map_crisis = get_map_crisis()

	# Parameters
	if len(sys.argv)>1:
		if sys.argv[1]:
			init_money_value = float(sys.argv[1])


	money_value = init_money_value

	num_years_count = 0
	num_years_negative = 0
	num_years_positive = 0

	print_header()

	precipfile = open(MSCI_WORD_FILE,'r')

	for precipline in precipfile:

		(clave,valor) = precipline.split()

		inflaction = map_inflaction[clave]
		crisis = map_crisis[clave]

		percentaje_money_value = porcentaje(money_value,float(valor))
		money_value = money_value + percentaje_money_value
		print_row(clave,valor,money_value,percentaje_money_value,inflaction,crisis)

		if float(valor) > -1:
			num_years_positive += 1
		else:
			num_years_negative += 1

		valor = str(1 + float(valor)/100)
		datos[clave] = valor
		num_years_count += 1

	ppt = np.array([float(v) for k,v in datos.iteritems()])

	result = calculateGeoMeanPorcentaje(ppt)




	print (Fore.RESET + Back.RESET + Style.RESET_ALL)

	# Output result
	print (Fore.RESET + Back.RESET + Style.RESET_ALL)

	print(Fore.MAGENTA + " Years: " + Fore.WHITE + str(num_years_count))
	print(Fore.MAGENTA + " Init money value: " + Fore.WHITE + str(init_money_value))
	print(Fore.MAGENTA + " Years negative: " + Fore.WHITE + str(num_years_negative))
	print(Fore.MAGENTA + " Years positive: " + Fore.WHITE + str(num_years_positive))
	print(Fore.MAGENTA + " Geometric mean: " + Fore.WHITE + str(result) + "%")

	print (Fore.RESET + Back.RESET + Style.RESET_ALL)

