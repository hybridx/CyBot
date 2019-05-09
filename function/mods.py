import pkgutil
import os
import string

class mods():
	def __init__(self):
		print("mods class init")
		self.modules = self.getmodules()
		print(self.modules)

	def getmodules(cls):
		locations = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")]
		modules = []
		for finder, name, ispkg in pkgutil.walk_packages(locations):
			loader = finder.find_module(name)
			mod = loader.load_module(name)
			modules.append(mod)
		#modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
		return modules

	def getkeywords(self, text):
		words = []
		text = text.lower()
		words = text.split()
		return words

	def query(self, txt, ai):
		texts = self.getkeywords(txt)
		res = None
		rescount = mres = -1
		for module in self.modules:
			rescount = module.isValid(texts)
			if mres < rescount:
				mres = rescount
				res = module
		if mres > 0:
			res.handle(txt, ai)