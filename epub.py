from epubContainers import opf,container,toc
import os
import zipfile
from datetime import datetime
import shutil
from html import *



'''
Todo:
fix save where if directory exists it fails
check why not accepting dc:title
make sure that spine has at least one itemref?
look where book-id is made
include a nav
finish up toc
'''
def getMediaType(extension):
	if extension == 'xhtml':
		return 'application/xhtml+xml'
	elif extension == 'css':
		return 'text/css'
	elif extension == 'js':
		return 'text/javascript'
	elif extension == 'jpg':
		return 'image/jpeg'	
	return ''


class epub:
	
	def __init__(self,title='title',identifier='id',language='en'):
		#create opf
		self.opf = opf()
		self.opf.addMetaDC("title",'title',title)
		self.opf.addMetaDC("identifier",'bookid',identifier)
		self.opf.addMetaDC("language",'',language)
		self.opf.addMetaProperty("dcterms:modified",datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
		
		#create container xml
		self.container = container()
		self.container.addRootFile({"full-path":"OEBPS/content.opf","media-type":"application/oebps-package+xml"})
		
		#string for mimetype file
		self.mimetype = "application/epub+zip"
		
		#create toc.xhtml
		# self.toc = toc()
		# self.opf.addToc("toc.xhtml")
		
		#holds references to each object to put in the epub
		self.objects = []
		
	def setTitle(self,title):
		self.opf.setMeta("dc:title",{"id":"title"},title)
	
	def addFile(self,filePath,isNav = False):
		fileName = filePath.split('\\')[-1]
		extension = fileName.split('.')[-1]	
		properties = {}
		if isNav:
			properties["properties"] = "nav"
		properties["id"] = fileName.split('.')[0]
		properties["href"] = fileName
		properties["media-type"] = getMediaType(extension.strip())
		#adds metadata based off of file, if can't recognize, will do nothing
		#add to lists
		self.objects.append(filePath)
		self.opf.addManifestItem("item",properties)
		if properties["media-type"] == "application/xhtml+xml":
			self.opf.addSpineItem("itemref",{"idref":properties["id"]})

	
	#add folder and if toc exists in here define toc Name
	def addFolder(self,folderPath,tocName=''):
		try:
			if os.path.isfile(folderPath+"\\"+tocName):
				self.addFile(folderPath+"\\"+tocName,True)
			for f in os.listdir(folderPath):
				path = '\\'.join([folderPath,f])
				if os.path.isfile(path):
					if f != tocName:
						self.addFile(path)
		except FileNotFoundError:
			print(folderPath + "can not be found")

	def save(self,loc):
		if os.path.exists(loc+".epub"):
			print(loc+" already exists.  please choose another place to save")
		else:
			with zipfile.ZipFile(loc + '.epub','w') as zip:
				#write mimetype,container and opf files
				zip.writestr('mimetype',self.mimetype)
				zip.writestr('META-INF\\container.xml',self.container.toString())
				zip.writestr('OEBPS\\content.opf',self.opf.toString())
				#zip.writestr('OEBPS\\toc.xhtml',self.toc.toString())
				#write objects
				for o in self.objects:
					zip.write(o,"OEBPS\\"+o.split('\\')[-1])