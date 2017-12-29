# -*- coding: utf-8 -*-
import html5, re, json
from widgets.actionbar import ActionBar
from widgets.file import FileWidget

from event import EventDispatcher
from priorityqueue import actionDelegateSelector
from config import conf
from i18n import translate
from network import DeferredCall

from __pyjamas__ import JS

class BasicEditorAction(html5.ext.Button):
	cmd = None
	name = None
	value = True
	title = None

	isActiveTag = None

	def __init__(self, *args, **kwargs):
		super(BasicEditorAction, self).__init__(self.cmd, *args, **kwargs)

		self.removeClass("button") # dont use default button class here
		self.addClass("btn-vTextedit", self.cmd) #, "ql-%s" % self.name)

		if self.title:
			self["title"] = self.title
		else:
			self["title"] = self.cmd
		
		self.setText('<img src="/vi/s/icons/actions/text/' + self.cmd.lower() + '.svg" alt="' + self["title"] + '">')

	def getQuill(self):
		return self.parent().parent().parent().editor.quill

	def onClick(self, sender = None):
		q = self.getQuill()

		fmt = q.getFormat()

		value = getattr(fmt, self.name, not self.value)
		if value == self.value:
			value = not value
		else:
			value = self.value

		print("clicked on button %s[%s]" % (self.name, value))
		q.format(self.name, value)

	def onAttach(self):
		self.parent().parent().parent().editor.editorChangeEvent.register(self)

	def onDetach(self):
		self.parent().parent().parent().editor.editorChangeEvent.unregister(self)

	def onEditorChange(self):
		q = self.getQuill()
	
		try:
			fmt = q.getFormat()
		except:
			return
		
		self.removeClass("is-active")
		if getattr(fmt, self.name, None):
			value = getattr(fmt, self.name, None)
			if value == "True" or self.value == value and self.name != "indent":
				self.addClass("is-active")



class TextStyleBold(BasicEditorAction):
	name = cmd = "bold"
	title = translate("Bold")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.bold", TextStyleBold )

class TextStyleItalic(BasicEditorAction):
	name = cmd = "italic"
	title = translate("Italic")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.italic", TextStyleItalic )

class TextStyleSuper(BasicEditorAction):
	cmd = "Super"
	name = "subsuper"
	value = "Sup"
	title = translate("Super")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.super", TextStyleSuper )

class TextStyleSub(BasicEditorAction):
	cmd = "Sub"
	name = "subsuper"
	value = "Sub"
	title = translate("Sub")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.sub", TextStyleSub )

class TextStyleH1(BasicEditorAction):
	cmd = "H1"
	name = "header"
	value = 1
	title = translate("H1")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h1", TextStyleH1 )

class TextStyleH2(BasicEditorAction):
	cmd = "H2"
	name = "header"
	value = 2
	title = translate("H2")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h2", TextStyleH2 )

class TextStyleH3(BasicEditorAction):
	cmd = "H3"
	name = "header"
	value = 3
	title = translate("H3")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h3", TextStyleH3 )

class TextStyleH4(BasicEditorAction):
	cmd = "H4"
	name = "header"
	value = 4
	title = translate("H4")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.h4", TextStyleH4 )

class TextStyleBlockQuote(BasicEditorAction):
	name = cmd = "blockquote"
	title = translate("Blockqoute")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.blockquote", TextStyleBlockQuote )

class TextInsertDivider(BasicEditorAction):
	name = cmd = "divider"
	title = translate("Divider")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.divider", TextInsertDivider )

class TextStyleAlignCenter(BasicEditorAction):
	cmd = "alignCenter"
	name = "align"
	value = "Center"
	title = translate("Align Center")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.alignCenter", TextStyleAlignCenter )

class TextStyleAlignLeft(BasicEditorAction):
	cmd = "alignLeft"
	name = "align"
	value = "Left"
	title = translate("Align Left")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.alignLeft", TextStyleAlignLeft )

class TextStyleAlignRight(BasicEditorAction):
	cmd = "alignRight"
	name = "align"
	value = "Right"
	title = translate("Align Right")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.alignRight", TextStyleAlignRight )

class TextStyleAlignJustify(BasicEditorAction):
	cmd = "alignJustify"
	name = "align"
	value = "Justify"
	title = translate("Align Justify")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="style.text.alignJustify", TextStyleAlignJustify )

class TextInsertOrderedList(BasicEditorAction):
	cmd = "orderedList"
	name = "list"
	value = "ordered"
	title = translate("Insert an ordered List")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.orderedList", TextInsertOrderedList )

class TextInsertUnorderedList(BasicEditorAction):
	cmd = "unorderedList"
	name = "list"
	value = "bullet"
	title = translate("Insert an unordered List")
actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.unorderedList", TextInsertUnorderedList )

class TextOutdent(BasicEditorAction):
	cmd = "outdent"
	name = "indent"
	value = "-1"
	title = translate("Indent less")

	def onClick(self, sender = None):
		q = self.getQuill()
		fmt = q.getFormat()
		value = getattr(fmt, self.name, "0")
		r = q.getSelection()

	   	q.formatLine(r.index, r.length, "indent", int(value) - 1)

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.outdent", TextOutdent )

class TextIndent(BasicEditorAction):
	name = cmd = "indent"
	value = "+1"
	title = translate("Indent more")


	def onClick(self, sender = None):
		q = self.getQuill()
		fmt = q.getFormat()
		value = getattr(fmt, self.name, "0")
		r = q.getSelection()

	   	q.formatLine(r.index, r.length, "indent", int(value) + 1)

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.indent", TextIndent )

class TextRemoveFormat(BasicEditorAction):
	cmd = "removeformat"
	name = "clean"
	title = translate("Remove all formatting")

	def onClick(self, sender = None):
		q = self.getQuill()

		r = q.getSelection()
		if r.length > 0:
		   	q.removeFormat(r.index, r.length, "user")

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.removeformat", TextRemoveFormat )

# --- Images -----------------------------------------------------------------------------------------------------------

'''
class FileSelectDialog(html5.ext.Popup):
	def __init__(self, notifier=None, title="", alt="", additionalClass="", *args, **kwargs):
		super(FileSelectDialog, self).__init__(*args, **kwargs)

		currentSelector = FileWidget( "file", isSelector=True )
		currentSelector.selectionActivatedEvent.register(self)

		self.appendChild(currentSelector)

		# Title
		lbl = html5.Label()
		lbl.appendChild(translate("Title"))
		
		self.titleInput = html5.Input()
		self.titleInput["value"] = title
		lbl.appendChild(self.titleInput)
		self.appendChild(lbl)
		
		# Class
		lbl = html5.Label()
		lbl.appendChild(translate("Class"))

		self.classSelect = html5.Select()
		for c in ["vitxt-image-left", "vitxt-image-right", "vitxt-image-block"]:
			opt = html5.Option()
			opt["value"] = c
			opt.appendChild(c)

			if c == additionalClass:
				opt["selected"] = True

			self.classSelect.appendChild(opt)

		lbl.appendChild(self.classSelect)
		self.appendChild(lbl)

		# Alt
		lbl = html5.Label()
		lbl.appendChild(translate("Alt"))
		
		self.altInput = html5.Input()
		self.altInput["value"] = alt
		lbl.appendChild(self.altInput)
		self.appendChild(lbl)

		# Buttons
		btnOk = html5.ext.Button(translate("OK"), callback=self.onOkBtnClicked)
		btnOk.addClass("btn_yes")
		self.appendChild(btnOk)

		btnCancel = html5.ext.Button(translate("Cancel"), callback=self.close)
		btnCancel.addClass("btn_no")
		self.appendChild(btnCancel)

	def selectionActivatedEvent(self, selectWdg, selection)
		self.select

	def onOkBtnClicked(self, sender = None):
		self.close()
'''
	
class TextInsertImageAction(BasicEditorAction):
	name = cmd = "image"
	title = translate("Insert Image")

	def onClick(self, sender=None):
		#FileSelectDialog(successHandler=self.onFileSelectionAvailable)

		self.currentSelector = FileWidget( "file", isSelector=True )
		self.currentSelector.selectionActivatedEvent.register(self)
		conf["mainWindow"].stackWidget(self.currentSelector)

	def onSelectionActivated(self, widget, selection):
			conf["mainWindow"].removeWidget(self.currentSelector)

			if not selection:
				return

			for item in selection:
				dataUrl = "/file/download/%s/%s" % (item.data["dlkey"], item.data["name"].replace("\"",""))
				if "mimetype" in item.data.keys() and item.data["mimetype"].startswith("image/"):	
					data = json.dumps({"url": dataUrl, "alt": item.data["name"]})
					self.getQuill().format("image", JS("JSON.parse(@{{data}})"))
				else:
					data = json.dumps({"href": dataUrl + "?download=1", "title": item.data["name"], "isDownload": "True"})
					self.getQuill().format("link", JS("JSON.parse(@{{data}})"))

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.image" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TextInsertImageAction.isSuitableFor, TextInsertImageAction )


# --- Links ------------------------------------------------------------------------------------------------------------

class LinkEditDialog(html5.ext.Popup):
	def __init__(self, href="", target="", title="", successHandler=None, quill=None, *args, **kwargs):
		super(LinkEditDialog, self).__init__(*args, **kwargs)

		self.successHandler = successHandler
		self.quill = quill
		self.addClass("linkDialog")

		# URL
		lbl = html5.Label()
		lbl.appendChild(translate("URL"))
		
		self.urlInput = html5.Input()
		self.urlInput["value"] = href
		lbl.appendChild(self.urlInput)
		self.appendChild(lbl)

		# Target
		lbl = html5.Label()
		lbl.appendChild(translate("Target"))

		self.targetSelect = html5.Select()
		for t in ["", "_blank", "_self", "_parent", "_top"]:
			opt = html5.Option()
			opt["value"] = t
			opt.appendChild(t)

			if t == target:
				opt["selected"] = True

			self.targetSelect.appendChild(opt)

		lbl.appendChild(self.targetSelect)
		self.appendChild(lbl)

		# Title
		lbl = html5.Label()
		lbl.appendChild(translate("Title"))
		
		self.titleInput = html5.Input()
		self.titleInput["value"] = title
		lbl.appendChild(self.titleInput)
		self.appendChild(lbl)

		# Buttons
		btnOk = html5.ext.Button(translate("OK"), callback=self.onOkBtnClicked)
		btnOk.addClass("btn_yes")
		self.appendChild(btnOk)

		btnCancel = html5.ext.Button(translate("Cancel"), callback=self.close)
		btnCancel.addClass("btn_no")
		self.appendChild(btnCancel)

	def onOkBtnClicked(self, sender = None):
		if self.successHandler:
			url = self.urlInput["value"]
			if url and not url.startswith('/file/') and not url.startswith('http'):
				url = 'http://' + url

			self.successHandler(
				href=url, 
				target=self.targetSelect.children(self.targetSelect["selectedIndex"])["value"],
				title=self.titleInput["value"])
			self.close()


class TextInsertLinkAction(BasicEditorAction):
	name = cmd = "link"
	title = translate("Insert Link")

	def onClick(self, sender=None):
		q = self.getQuill()
		r = q.getSelection()
		if r.length > 0:
			data = getattr(self.getQuill().getFormat(), self.name, "")
			data = json.loads(JS("JSON.stringify(@{{data}})"))

			LinkEditDialog(successHandler=self.onLinkAvailable, **data)

	def onLinkAvailable(self, **data):
		data = json.dumps(data)
		self.getQuill().format("link", JS("JSON.parse(@{{data}})"))

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return actionName=="text.link"

	def resetLoadingState(self):
		pass

class LinkEditor(html5.ext.Popup):
	def __init__(self, value=None, quill=None, left=500, top=200, *args, **kwargs):
		super( LinkEditor, self ).__init__(*args, **kwargs)

		self.value = value
		self.addClass("linkEditor")
		self.parent().removeClass("popup")
		self.element.setAttribute("style", "left:" + str(left) + "px;top:" + str(top) + "px;")

		# hint
		hint = html5.Span()
		hint.appendChild(value.href)
		self.appendChild(hint)
		
		# Buttons
		btnEdit = html5.ext.Button(translate("edit"), callback=self.onEditBtnClicked)
		btnEdit.addClass("icon edit")
		hint.appendChild(btnEdit)

	def onEditBtnClicked(self, sender = None):
		value = self.value
		data = json.loads(JS("JSON.stringify(@{{value}})"))

		LinkEditDialog(successHandler=self.onLinkAvailable, **data)
		self.close()

	def onLinkAvailable(self, **data):
		q = JS("parent.myQuill")
		data = json.dumps(data)
		q.format("link", JS("JSON.parse(@{{data}})"))
		eval("parent.lastSelection.index = parent.lastSelection.length = 0;")

actionDelegateSelector.insert(1, TextInsertLinkAction.isSuitableFor, TextInsertLinkAction )


'''
class CreateTablePopup( html5.ext.Popup ):
	def __init__(self, targetNode, *args, **kwargs ):
		super( CreateTablePopup, self ).__init__( *args, **kwargs )
		assert targetNode

		while not "innerHTML" in dir(targetNode):
			targetNode = targetNode.parentNode

		self.targetNode = targetNode
		self["class"].append("createtable")
		self.rowInput = html5.Input()
		self.rowInput["type"] = "number"
		self.rowInput["value"] = 3
		self.appendChild( self.rowInput )
		l = html5.Label(translate("Rows"), forElem=self.rowInput)
		l["class"].append("rowlbl")
		self.appendChild( l )
		self.colInput = html5.Input()
		self.colInput["type"] = "number"
		self.colInput["value"] = 4
		self.appendChild( self.colInput )
		l = html5.Label(translate("Cols"), forElem=self.colInput)
		l["class"].append("collbl")
		self.appendChild( l )
		self.insertHeader = html5.Input()
		self.insertHeader["type"] = "checkbox"
		self.appendChild( self.insertHeader )
		l = html5.Label(translate("Insert Table Header"), forElem=self.insertHeader)
		l["class"].append("headerlbl")
		self.appendChild( l )
		self.appendChild( html5.ext.Button( "Cancel", callback=self.doClose ) )
		self.appendChild( html5.ext.Button( "Create", callback=self.createTable ) )

	def doClose(self, *args, **kwargs):
		self.targetNode = None
		self.close()

	def createTable(self, *args, **kwargs):
		rows = int(self.rowInput["value"])
		cols = int(self.colInput["value"])
		insertHeader = self.insertHeader["checked"]
		innerHtml = "<table>"
		if insertHeader:
			innerHtml += "<thead>"
			for c in range(0,cols):
				innerHtml += "<th>&nbsp;</th>"
			innerHtml += "</thead>"
		for x in range(0,rows):
			innerHtml += "<tr>"
			for y in range(0,cols):
				innerHtml += "<td>%s - %s</td>" % (x,y)
			innerHtml += "</tr>"
		innerHtml += "</table>"
		self.targetNode.innerHTML = self.targetNode.innerHTML+innerHtml
		self.doClose()

class TextInsertTableAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TextInsertTableAction, self ).__init__( translate("Insert Table"), *args, **kwargs )
		self["class"] = "icon text table"
		self["title"] = translate("Insert Table")

	def onClick(self, sender=None):
		self.parent().parent().editor.focus()
		node = eval("window.top.getSelection().anchorNode")

		if node:
			CreateTablePopup( node )

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TextInsertTableAction.isSuitableFor, TextInsertTableAction )

class TableInsertRowBeforeAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertRowBeforeAction, self ).__init__( translate("Insert Table Row before"), *args, **kwargs )
		self["class"] = "icon text table newrow before"
		self["title"] = translate("Insert Table Row before")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		i = 10
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TR":
				tr = html5.document.createElement("tr")
				for c in range(0,node.children.length):
					td = html5.document.createElement("td")
					tr.appendChild( td )
				node.parentNode.insertBefore( tr, node )
				return
			node = node.parentNode

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newrow.before" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertRowBeforeAction.isSuitableFor, TableInsertRowBeforeAction )

class TableInsertRowAfterAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertRowAfterAction, self ).__init__( translate("Insert Table Row after"), *args, **kwargs )
		self["class"] = "icon text table newrow after"
		self["title"] = translate("Insert Table Row after")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		i = 10
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TR":
				tr = html5.document.createElement("tr")
				for c in range(0,node.children.length):
					td = html5.document.createElement("td")
					tr.appendChild( td )
				if node.nextSibling:
					node.parentNode.insertBefore( tr, node.nextSibling )
				else:
					node.parentNode.appendChild( tr )
				return
			node = node.parentNode

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newrow.after" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertRowAfterAction.isSuitableFor, TableInsertRowAfterAction )

class TableInsertColBeforeAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertColBeforeAction, self ).__init__( translate("Insert Table Col before"), *args, **kwargs )
		self["class"] = "icon text table newcol before"
		self["title"] = translate("Insert Table Col before")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		td = None
		tr = None
		table = None
		i = 10
		#Try to extract the relevat nodes from the dom
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TD":
				td = node
			elif node.tagName=="TR":
				tr = node
			elif node.tagName=="TABLE":
				table = node
				break
			node = node.parentNode
		if td and tr and table:
			cellIdx = 0 # Before which column shall we insert a new col?
			for x in range(0, tr.children.length):
				if td==tr.children.item(x):
					break
				cellIdx += 1
			for trChildIdx in range(0,table.children.length):
				trChild = table.children.item(trChildIdx)
				if not "tagName" in dir( trChild ):
					continue
				if trChild.tagName=="THEAD":
					#Fix the table head
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("th")
							child.insertBefore( newTd, child.children.item(cellIdx) )
				elif trChild.tagName=="TBODY":
					#Fix all rows in the body
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("td")
							child.insertBefore( newTd, child.children.item(cellIdx) )

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newcol.before" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertColBeforeAction.isSuitableFor, TableInsertColBeforeAction )

class TableInsertColAfterAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableInsertColAfterAction, self ).__init__( translate("Insert Table Col after"), *args, **kwargs )
		self["class"] = "icon text table newcol after"
		self["title"] = translate("Insert Table Col after")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		td = None
		tr = None
		table = None
		i = 10
		#Try to extract the relevat nodes from the dom
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TD":
				td = node
			elif node.tagName=="TR":
				tr = node
			elif node.tagName=="TABLE":
				table = node
				break
			node = node.parentNode
		if td and tr and table:
			cellIdx = 0 # Before which column shall we insert a new col?
			for x in range(0, tr.children.length):
				if td==tr.children.item(x):
					break
				cellIdx += 1
			for trChildIdx in range(0,table.children.length):
				trChild = table.children.item(trChildIdx)
				if not "tagName" in dir( trChild ):
					continue
				if trChild.tagName=="THEAD":
					#Fix the table head
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("th")
							if cellIdx+1<child.children.length:
								child.insertBefore( newTd, child.children.item(cellIdx+1) )
							else:
								child.appendChild( newTd )
				elif trChild.tagName=="TBODY":
					#Fix all rows in the body
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							newTd = html5.document.createElement("td")
							if cellIdx+1<child.children.length:
								child.insertBefore( newTd, child.children.item(cellIdx+1) )
							else:
								child.appendChild( newTd )

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.newcol.after" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableInsertColAfterAction.isSuitableFor, TableInsertColAfterAction )

class TableRemoveRowAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableRemoveRowAction, self ).__init__( translate("Remove Table Row"), *args, **kwargs )
		self["class"] = "icon text table remove row"
		self["title"] = translate("Remove Table Row")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		i = 10
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TR":
				node.parentNode.removeChild(node)
				return
			node = node.parentNode

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.remove.row" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableRemoveRowAction.isSuitableFor, TableRemoveRowAction )

class TableRemoveColAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TableRemoveColAction, self ).__init__( translate("Remove Table Col"), *args, **kwargs )
		self["class"] = "icon text table remove col"
		self["title"] = translate("Remove Table Col")

	def onClick(self, sender=None):
		node = eval("window.top.getSelection().anchorNode")
		td = None
		tr = None
		table = None
		i = 10
		#Try to extract the relevat nodes from the dom
		while i>0 and node and node != self.parent().parent().editor.element:
			i -= 1
			if not "tagName" in dir( node ):
				node = node.parentNode
				continue
			if node.tagName=="TD":
				td = node
			elif node.tagName=="TR":
				tr = node
			elif node.tagName=="TABLE":
				table = node
				break
			node = node.parentNode
		if td and tr and table:
			cellIdx = 0 # Which column shall we delete?
			for x in range(0, tr.children.length):
				if td==tr.children.item(x):
					break
				cellIdx += 1
			for trChildIdx in range(0,table.children.length):
				trChild = table.children.item(trChildIdx)
				if not "tagName" in dir( trChild ):
					continue
				if trChild.tagName=="THEAD":
					#Fix the table head
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							child.removeChild(child.children.item(cellIdx))
				elif trChild.tagName=="TBODY":
					#Fix all rows in the body
					for childIdx in range(0,trChild.children.length):
						child = trChild.children.item(childIdx)
						if not "tagName" in dir( child ):
							continue
						if child.tagName=="TR":
							child.removeChild(child.children.item(cellIdx))

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.table.remove.col" )

	def resetLoadingState(self):
		pass

actionDelegateSelector.insert(1, TableRemoveColAction.isSuitableFor, TableRemoveColAction )
'''

class TextSaveAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TextSaveAction, self ).__init__( translate("Save"), *args, **kwargs )
		self["class"] = "btn-vTextedit save f-right"
		self["title"] = translate("Save")
		self.setText('<img src="/vi/s/icons/actions/text/save.svg">')

	def onClick(self, event):
		self.parent().parent().parent().saveText()

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.save" )

actionDelegateSelector.insert(1, TextSaveAction.isSuitableFor, TextSaveAction )

class TextAbortAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( TextAbortAction, self ).__init__( translate("Abort"), *args, **kwargs )
		self["class"] = "btn-vTextedit abort f-right"
		self["title"] = translate("Abort")
		self.setText('<img src="/vi/s/icons/actions/text/cancel.svg">')

	def onClick(self, event):
		if self.parent().parent().parent().editor.changed():
			html5.ext.popup.YesNoDialog(translate("Any changes will be lost. Do you really want to abort?"),
			                            yesCallback=self.doAbort)
		else:
			self.doAbort()

	def doAbort(self, *args, **kwargs):
		self.parent().parent().parent().abortText()

	@staticmethod
	def isSuitableFor( module, handler, actionName ):
		return( actionName=="text.abort" )

actionDelegateSelector.insert(1, TextAbortAction.isSuitableFor, TextAbortAction )


class TextUndoAction(BasicEditorAction):
	cmd = "undo"
	title = translate("Undo the last action")

	def onClick(self, sender = None):
		self.getQuill().history.undo()

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.undo", TextUndoAction )

class TextRedoAction( BasicEditorAction ):
	cmd = "redo"
	title = translate("Redo the last undone action")

	def onClick(self, sender=None):
		self.getQuill().history.redo()

actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.redo", TextRedoAction )


class FlipViewAction( html5.ext.Button ):
	def __init__(self, *args, **kwargs):
		super( FlipViewAction, self ).__init__( translate("Flip View"), *args, **kwargs )
		self["class"] = "btn-vTextedit flipview"
		self["title"] = translate("Flip View")
		self.setText('<img src="/vi/s/icons/actions/text/code.svg">')

	def onAttach(self):
		super( FlipViewAction, self ).onAttach()
		if self.parent().parent().parent().isWysiwygMode:
			self["class"].append("is_wysiwyg")
		else:
			self["class"].append("is_htmlview")

	def onClick(self, sender=None):
		if "is_wysiwyg" in self["class"]:
			self["class"].remove("is_wysiwyg")
		if "is_htmlview" in self["class"]:
			self["class"].remove("is_htmlview")

		if self.parent().parent().parent().flipView():
			self["class"].append("is_wysiwyg")
		else:
			self["class"].append("is_htmlview")

	def resetLoadingState(self):
		pass
actionDelegateSelector.insert(1, lambda module, handler, actionName: actionName=="text.flipView", FlipViewAction )


def dumpNode(obj):
	try:
		print("obj", obj)
		print("type", obj.nodeType)
		print("child", obj.childElementCount)

		div = html5.Div()
		div.element.appendChild(obj.cloneNode(True))
		print("html", div.element.innerHTML)
		print("children", div.element.childNodes.length)
		print("children[1]", obj.childNodes.length)
	except:
		print("ERROR DUMPING %s" % obj)


class Editor(html5.Div):
	__editorCount__ = 0

	def __init__(self, parent, html, *args, **kwargs ):
		super(Editor, self).__init__(*args, **kwargs)
		self.addClass("contentdiv")

		self["id"] = "wysiwyg%d" % Editor.__editorCount__
		Editor.__editorCount__ += 1

		self.initial_txt = self.element.innerHTML = html
		self.sinkEvent("onBlur", "onFocus")
		parent.appendChild(self)
		self.quill = None

		self.editorChangeEvent = EventDispatcher("editorChange")
		DeferredCall(self.init)

	def init(self):
		self.quill = eval("""
					new window.top.quill("#%s",{}) // quill works without toolbar as well
					""" % (self["id"]))
		q = self.quill
		eval("parent.lastSelection = {}; parent.lastSelection.index = parent.lastSelection.length = 0;")
		JS("parent.myQuill = @{{q}}")

		self.quill.on("editor-change", self.updateActionBar)
		self.quill.on("selection-change", self.updateSelection)

	def changed(self):
		return self.initial_txt != self.element.innerHTML

	def updateActionBar(self, *args, **kwargs):
		self.editorChangeEvent.fire()

	def updateSelection(self, *args, **kwargs):
		if args[2] == "user":
			JS("""
				if(parent.document.getElementsByClassName('linkEditor')) {
					if(parent.document.getElementsByClassName('linkEditor')[0]) {
						if(parent.document.getElementsByClassName('linkEditor')[0].parentNode) {
							if(parent.document.getElementsByClassName('linkEditor')[0].parentNode.parentNode) {
								parent.document.getElementsByClassName('linkEditor')[0].parentNode.parentNode.removeChild(parent.document.getElementsByClassName('linkEditor')[0].parentNode)
							}
						}
					}
				}
			""")
			try:
				fmt = self.quill.getFormat()
			except:
				return

			
			if getattr(fmt, "link", None):
				value = getattr(fmt, "link", None)
				lastSelection =(JS("parent.lastSelection"))

				jsonSel = json.dumps(self.quill.getFormat())
				start = self.quill.getSelection().index - 1
				length = 0

				while json.dumps(self.quill.getFormat(start)) == jsonSel:
					start = start - 1

				while json.dumps(self.quill.getFormat(start + 1, length)) == jsonSel:
					length = length + 1

				if lastSelection.index == start and lastSelection.length == length:
					return
				
				self.quill.setSelection(start, length)

				top = self.quill.getBounds(start, length).top + self.quill.getBounds(start, length).height + eval("parent.document.getElementById('%s').getBoundingClientRect().top" % self["id"])
				left = self.quill.getBounds(start, length).left + eval("parent.document.getElementById('%s').getBoundingClientRect().left" % self["id"])

				LinkEditor(value=value, quill=self.quill, left=left, top=top)

			eval("parent.lastSelection.index = '%s'; parent.lastSelection.length = '%s';" % (self.quill.getSelection().index, self.quill.getSelection().length))

	def execCommand(self, commandName, valueArgument=None):
		"""
		Wraps the document.execCommand() function for easier usage.
		"""

		if valueArgument is None:
			valueArgument = "null"
		else:
			valueArgument = "\"%s\"" % str(valueArgument)

		print("execCommand(\"%s\", false, %s)" % (commandName, valueArgument))
		return bool(eval("window.top.document.execCommand(\"%s\", false, %s)" % (commandName, valueArgument)))


class Wysiwyg( html5.Div ):
	def __init__(self, editHtml, actionBarHint=translate("Text Editor"), *args, **kwargs ):
		super( Wysiwyg, self ).__init__(*args, **kwargs)
		self.cursorMovedEvent = EventDispatcher("cursorMoved")
		self.saveTextEvent = EventDispatcher("saveText")
		self.abortTextEvent = EventDispatcher("abortText")

		self.primaryActions = ActionBar(None, None, actionBarHint)
		self.primaryActions.removeClass("actionbar")
		self.primaryActions.setActions([
			"style.text.bold",
			"style.text.italic",
			"style.text.super",
			"style.text.sub",
		    "style.text.h1",
			"style.text.h2",
			"style.text.h3",
			"style.text.h4",
			"|",
			"text.removeformat",
			"|",
			"text.undo",
			"text.redo",
			"|",
			"text.flipView",
			"|",
			"text.abort",
			"text.save"])

		self.secondaryActions = ActionBar(None, None, None)
		self.secondaryActions.removeClass("actionbar")
		self.secondaryActions.setActions([
			"style.text.alignLeft",
			"style.text.alignCenter",
			"style.text.alignRight",
			"style.text.alignJustify",
			"|",
			"text.outdent",
			"text.indent",
			"|",
			"style.text.blockquote",
			"text.orderedList",
			"text.unorderedList",
			"|",
			"text.divider",
			"text.image",
			"text.link",
		])

		self.rawCodeActions = ActionBar(None, None, actionBarHint)
		self.rawCodeActions.hide()
		self.rawCodeActions.removeClass("actionbar")
		self.rawCodeActions.setActions(["text.flipView"])

		self.actionbarWrap = html5.Div()
		self.actionbarWrap.addClass("actionbar")
		self.actionbarWrap.appendChild(self.primaryActions)
		self.actionbarWrap.appendChild(self.secondaryActions)
		self.actionbarWrap.appendChild(self.rawCodeActions)
		self.appendChild(self.actionbarWrap)
		
		self.source = html5.form.Textarea()
		self.source.addClass("sourceCode")
		self.source.hide()
		self.appendChild(self.source)
		
		self.isWysiwygMode = True
		self.discardNextClickEvent = False
		self.editor = Editor(self, editHtml)

		self.currentImage = None
		self.cursorImage = None
		self.lastMousePos = None
		self.sinkEvent("onMouseDown", "onMouseUp", "onMouseMove", "onClick")

	def flipView(self, *args, **kwargs ):
		htmlStr = self.editor.quill.root.innerHTML

		if self.isWysiwygMode:
			outStr = ""
			indent = 0
			indestStr = "    "
			inStr = htmlStr
			while inStr:
				if inStr.startswith("<div"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</div>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				if inStr.startswith("<p"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</p>"):
					indent -=1
					outStr += indestStr*indent
				elif inStr.startswith("<br"):
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<table"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</table"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<tr"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</tr"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<td"):
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<th>"):
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<thead"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</thead>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				elif inStr.startswith("<tbody"):
					outStr += "\n"
					outStr += indestStr*indent
					indent +=1
				elif inStr.startswith("</tbody>"):
					indent -=1
					outStr += "\n"
					outStr += indestStr*indent
				outStr += inStr[0]
				inStr = inStr[ 1: ]
	
			self.editor.hide()
			self.source.show()

			self.primaryActions.hide()
			self.secondaryActions.hide()
			self.rawCodeActions.show()

			self.source.element.value = outStr.strip()

			#self.actionbar1.setActions(["text.flipView"])
			#self.actionbar2.setActions([])
		else:
			htmlStr = self.source.element.value
			#htmlStr = re.sub("\n", '', htmlStr)
			#htmlStr = re.sub("&nbsp;", '', htmlStr).strip()

			self.editor.quill.root.innerHTML = htmlStr
			#self.editor.quill.setText(self.source.element.value)

			self.editor.show()
			self.source.hide()

			self.primaryActions.show()
			self.secondaryActions.show()
			self.rawCodeActions.hide()

		#self.actionbar1.setActions(self.textActions1)
			#self.actionbar2.setActions(self.textActions2)

		self.isWysiwygMode = not self.isWysiwygMode
		return self.isWysiwygMode


	def saveText(self, *args, **kwargs):
		htmlStr = self.editor.quill.root.innerHTML
		self.saveTextEvent.fire(self, htmlStr)

	def abortText(self, *args, **kwargs):
		self.abortTextEvent.fire(self)
