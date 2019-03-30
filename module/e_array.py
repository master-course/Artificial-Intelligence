
from e_object import e_object

class e_array(list):

	def __init__(self):
		super().__init__()
		self.e_array=[]

	def size(self):
		return len(self)
		

	def test(self):
		return "Hello world"	
