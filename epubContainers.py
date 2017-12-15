import xml.etree.ElementTree as ET

#create an etree Element
def createElement(name,params={},text=''):
	element = ET.Element(name,params)
	element.text = text
	return element
		
#structure for content.opf file
class opf:
	#creates skeleton structure for opf.  Still need to add title,identifier,languge, and update date to fit minimum requirements
	def __init__(self):
		self.package = self.makePackage()
		self.meta = self.makeMetaData()
		self.manifest = ET.Element("manifest")
		self.spine = ET.Element("spine")
		self.package.extend([self.meta,self.manifest,self.spine])

	#create package element
	def makePackage(self):
		docType = {"xmlns":"http://www.idpf.org/2007/opf","version":"3.0","xml:lang":"en","unique-identifier":"bookid"}
		return ET.Element("package",docType)

	#create metadata element
	def makeMetaData(self):
		return ET.Element("metadata",{"xmlns:dc":"http://purl.org/dc/elements/1.1/"})
		
	def setMeta(self,tagName,params,text):
		oldElement = self.meta.find(tagName)
		oldElement.text = text
		oldElement.attrib = params
		
	#add <dc:dcType id:?>text</dc:dcType> to metadata element
	def addMetaDC(self,dcType,id,text):
		params = {}
		if id != '':
			params = {"id":id}
		self.meta.append(createElement("dc:"+dcType,params,text))
	
	# add <meta property=?>text</meta> to metadata element
	def addMetaProperty(self,property,text):
		self.meta.append(createElement("meta",{"property":property},text))

	def addManifestItem(self,name,properties,text=''):
		self.manifest.append(createElement(name,properties,text))
	
	
	## spine format is <itemref item=itemLoc/>
	#adds item to spine
	def addSpineItem(self,name,properties,text=''):
		self.spine.append(createElement(name,properties,text))
	
	#add item to front of spine
	def addSpineFront(self,name,properties,text=''):
		self.spine.insert(0,createElement(name,properties,text))

	#returns tree in string form
	def toString(self):
		return ET.tostring(self.package,encoding="UTF-8",method="xml")
		
#holds container.xml file
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
