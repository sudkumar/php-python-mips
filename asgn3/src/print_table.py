#!/usr/bin/python

# return the non terminal print str
import json
def nt(nt, colspan):
	if nt == "start":
		return "<tr><th colspan=\""+ str(colspan) +"\" class=\"start\">"+str(nt)+"</th></tr>"
	return "<tr><th colspan=\""+ str(colspan) +"\">"+str(nt)+"</th></tr>"


# is string
def is_string(item):
	try:
		assert isinstance(item, basestring)
	except AssertionError, e:
		# raise e
		return False
	else:
		return True

class ParseTree():
	"""A Parse Tree generator"""
	def __init__(self, input):
		ol = []
		self.print_table(input, ol)
		# ol.reverse()
		self.ol = ol

	# write the html content to the given file
	def create_html(self, fileName):
		topHTML =  '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Parse Tree</title><style>  tr, th, td, .token, table{position: relative; padding: 0; margin: 0;} td{vertical-align: top; text-align: center; color: dimgray; padding: 26px 5px 0; } th{color: black; font-weight: normal; font-style: italic } th:after, th:before, .token:before{content: ""; position:absolute; width: 2px; height: 15px; background: grey; left: calc(50% - 1px); bottom: 100%;} th:after{top: 100%; height: 13px} table{ border-collapse: collapse; margin: 0px auto;} .first, .last, .mid{display:block;  width:50%; height: 2px; background: gray; position: absolute; top: 11px; left: 50%} .mid{width: 100%; left: 0} .last{left: 0} .start:before{display: none;} table{font-size: 11px;}</style></head><body>'
		midHTML = ''.join(self.ol)		
		bottomHTML = "</body></html>"
		with open(fileName, "w+") as htmlFile:
			htmlFile.write(topHTML)
			htmlFile.write(midHTML)
			htmlFile.write(bottomHTML)	

	# print the parse table with a given arr  
	def print_table(self, item, ol):
		"""
			for each new item
			1. open a table for it
			
			2. create a tr for itsef and put it in a th

			create a tr for it's children
				for each child 
					open td
					if child is a string
						print child
					else print that children
					close td 

		"""
			
		if is_string(item):
			# item is a sting, it's a token/value
			ol.append('<span class="token">'+str(item)+"</span>") 

		else:
			ol.append("<table>") 
			
			# print the current key
			keys = item.keys()
			me = keys[0]
			value = item[me]
			isValueStr = is_string(value)
			if isValueStr:
				# print nt(me)
				# if it is the start				
				ol.append(nt(me, 1))

				ol.append("<tr><td>"+str(value)+"</td></tr>") 
				colspan = 1
			else:				 
				colspan = len(value)
				# print nt(me)
				# if it is the start				
				ol.append(nt(me, colspan)) 

				ol.append("<tr>")

				# value is an array
				i = 1
				for key in value:
					if colspan == 1:
						className = "single"
					elif i == 1:
						className = "first"
					elif i == colspan:
						className = "last"
					else:
						className = "mid"
					# print "<td>"
					ol.append("<td> <span class=\""+className+"\"></span>") 
					self.print_table(key, ol)
					# print "</td>"
					ol.append("</td>") 
					i += 1

				# print "</tr>"
				ol.append("</tr>") 

			# print "</table>"
			ol.append("</table>") 


if __name__ == '__main__':

	file = open('output.json', 'r')
	input = file.read()	 
		# create the parse table and print it to index.html file
	ParseTree(json.loads(input)).create_html("index.html")
		