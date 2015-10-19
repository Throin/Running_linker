class CustDate:
	## A class to record a date. Allow comparison operations
	
	default_year = 2000
	default_month = 1
	default_day = 1
	
	def __init__(self, year = default_year, month = default_month, day = default_day):
		self.year = year
		self.month = month
		self.day = day
		
	def __str__(self):
		return "year: " + str(self.year) + "\nmonth: " +  str(self.month) + "\nday: " + str(self.day)
		
	def __lt__(self, other):
		if isinstance(other, CustDate):
			if self.year < other.year:
				return True
			elif self.year == other.year:
				if self.month < other.month:
					return True
				elif self.month == other.month:
					if self.day < other.day:
						return True
					else:
						return False
				else:
					return False
			else:
				return False
		else:
			return NotImplemented
	
	## TODO: complete with other operators
	
	def __le__(self, other):
		return False
		
	def __eq__(self, other):
		return False
	
	def __ne__(self, other):
		return True
		
	def __gt__(self, other):
		return False
		
	def __ge__(self, other):
		return False