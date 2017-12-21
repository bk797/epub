from epubContainers import opf,container
import os
import zipfile
from datetime import datetime
from html import *


class epub:
	
	def __init__(self,title='title',identifier='id',language='en',mimetype="MediaType\\mime.txt"):
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
		
		#holds references to each object to put in the epub
		self.objects = []
		
		#get set of mimetypes
		self.mimetypes = self.getMimeTypes(mimetype)
		
	#get map of extensions and mimetypes
	def getMimeTypes(self,fileName):
		mt = {}
		with open(fileName,'r') as file:
			for l in list(file):
				mimetype = l.strip().split('\t')
				mt[mimetype[0]] = mimetype[1]
		return mt
	
	#return associated mimetype from extension
	def getMediaType(self,extension):
		if extension in self.mimetypes:
			return self.mimetypes[extension]
		return ''
		
	#use if need to create custom meta data
	def addMeta(self,name,params,text):
		self.opf.setMeta(name,params,text)
	
	#update dc:identifier in opf
	def setID(self,id):
		self.opf.setMeta("dc:identifier",{"id":"bookid"},id)
	
	#update dc:title in opf 
	def setTitle(self,title):
		self.opf.setMeta("dc:title",{"id":"title"},title)
	
	#update dc:language in opf
	def setLan(sef,lan):
		sef.opf.setMeta("dc:language",{},lan)
	
	def addFile(self,filePath,isNav = False):
		fileName = filePath.split('\\')[-1]
		extension = fileName.split('.')[-1]	
		properties = {}
		if isNav:
			properties["properties"] = "nav"
		properties["id"] = fileName.split('.')[0]
		properties["href"] = fileName
		properties["media-type"] = self.getMediaType(extension.strip())
		#add necessary references
		self.objects.append(filePath)
		self.opf.addManifestItem("item",properties)
		if properties["media-type"] == "application/xhtml+xml":
			if isNav:
				#if toc make first item
				self.opf.addSpineFront("itemref",{"idref":properties["id"]})
			else:
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

	#save to location
	def save(self,loc):
		if os.path.exists(loc+".epub"):
			print(loc+" already exists.  please choose another place to save")
		else:
			with zipfile.ZipFile(loc + '.epub','w') as zip:
				#write mimetype,container and opf files
				zip.writestr('mimetype',self.mimetype)
				zip.writestr('META-INF\\container.xml',self.container.toString())
				zip.writestr('OEBPS\\content.opf',self.opf.toString())
				#write objects
				for o in self.objects:
					zip.write(o,"OEBPS\\"+o.split('\\')[-1])