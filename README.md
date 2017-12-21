# Epub
This program will create a program that follows the Epub3 convention.  It can be given the content files of the epub either by directory or by file.  When given a file, it will look for the corresponding mediatype and add the file information to the appropriate metafile containers to allow epub3 readers to recognize each file.  

# Installation
To use download the files in docs and put them in a directory that has code that will use this program.

# Basic Usage
To create a simple epub from a directory

```python
from epub import epub
sampleEbook = epub()
sampleEbook.addFolder("pathToDirectory")
sampleEbook.save("pathToFile\\sampleName")
#will save as "sampleName.epub" at pathToFile
```
This will create an epub with all of the contents in the folder pathToDirectory as an epub.  

# More Options

**Set Title**
```python
sampleEbook = epub(title="sampleTitle")
```
or
```python
sampleEbook = epub()
sampleEbook.setTitle("sampleTitle")
```

**Set Unique Identifier**
```python
sampleEbook = epub(title="sampleTitle",identifier="sampleID")
```
or
```python
sampleEbook = epub()
sampleEbook.setID("sampleID")
```

**Add any other MetaData**
```python
sampleEbook.addMeta("dc:tagName",{"id":"identifier"},"tagText")
# add entry <dc:tagName id=identifier>tagText</dc:tagName> into metadata element of content.opf
```

**Add Table of Contents**
```python
sampleEbook.addFolder(tocName="tocFile")
```
or
```python
sampleEbook.addFile("pathToToC",nav=True)
```

# Possible features to add in the future
**Auto-generate Table of Contents:** if no table of contents is provided, generate one  
**Support for epub2:** add necessary files to allow epub2 readers to read epubs created by this script  
**XHTML format checking:** make sure that any xhtml formats are validated and therefore readable  

# Additional Information
I got my list of common mimetypes from [here](http://hul.harvard.edu/ois/////systems/wax/wax-public-help/mimetypes.htm).  It was missing the mimetype for xhtml, so if there are any more crucial mimetypes missing, let me know.
