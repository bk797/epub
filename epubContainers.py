import xml.etree.ElementTree as ET
import datetime

def createElement(name,params={},text=''):
	element = ET.Element(name,params)
	element.text = text
	return element
		
class opf:

	def __init__(self):
		self.package = self.makePackage()
		self.meta = self.makeMetaData()
		self.manifest = ET.Element("manifest")
		self.spine = ET.Element("spine")
		self.package.extend([self.meta,self.manifest,self.spine])

	def makePackage(self):
		docType = {"xmlns":"http://www.idpf.org/2007/opf","version":"3.0","xml:lang":"en","unique-identifier":"bookid"}
		return ET.Element("package",docType)

	def makeMetaData(self):
		return ET.Element("metadata",{"xmlns:dc":"http://purl.org/dc/elements/1.1/"})
		# return ET.Element("metadata")
		
	def setMeta(self,tagName,params,text):
		oldElement = self.meta.find(tagName)
		oldElement.text = text
		oldElement.attrib = params
		
	def addMetaDC(self,dcType,id,text):
		params = {}
		if id != '':
			params = {"id":id}
		self.meta.append(createElement("dc:"+dcType,params,text))

	def addMetaProperty(self,property,text):
		self.meta.append(createElement("meta",{"property":property},text))

	def addManifestItem(self,name,properties,text=''):
		self.manifest.append(createElement(name,properties,text))
	
	def addSpineItem(self,name,properties,text=''):
		self.spine.append(createElement(name,properties,text))

	def toString(self):
		return ET.tostring(self.package,encoding="UTF-8",method="xml")
		
class container:
	
	def __init__(self):
		self.root = ET.Element('container')
		self.root.set('version','1.0')
		self.root.set('xmlns','urn:oasis:names:tc:opendocument:xmlns:container')
		self.rootfiles = ET.Element('rootfiles')
		self.root.append(self.rootfiles)
		
	def addRootFile(self,params={}):
		self.rootfiles.append(ET.Element('rootfile',params))
		
	def toString(self):
		return ET.tostring(self.root,encoding="UTF-8",method="xml")

#create table of contents xhtml
class toc:

	def __init__(self):
		self.table = ET.Element("nav",{"id":"toc"})
		self.list = ET.Element("ol")
		self.table.append(self.list)
		
	def addItem(self,href,title):
		listEntry = ET.Element("li")
		link = ET.Element("a",{"href":href})
		link.text = title
		listEntry.append(link)
		self.list.append(listEntry)
		
	def toString(self):
		return ET.tostring(self.table)	