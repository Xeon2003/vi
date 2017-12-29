# -*- coding: utf-8 -*-
import html5, utils
from priorityqueue import editBoneSelector
from __pyjamas__ import JS

class HtmlEditor(html5.Div):

	def __init__(self, moduleName, boneName, skelStructure, *args, **kwargs):
		super(HtmlEditor, self).__init__(*args, **kwargs)
		self.sinkEvent("onChange")

		self.moduleName = moduleName
		self.boneName = boneName
		self.skelStructure = skelStructure

		self.richView = html5.Div()
		self.appendChild(self.richView)

		self.htmlView = html5.Textarea()
		self.appendChild(self.htmlView)

		self.value = ""
		self.quill = None

	def onAttach(self):
		super(HtmlEditor, self).onAttach()

		if self.quill:
			return

		elem = self.richView.element
		self.quill = JS("""

			new window.top.quill(
				@{{elem}},  // The element
				
				{
				  // Theme
		          theme: 'snow',    
		          
		          // Toolbar
				  toolbar: [
		               [{ header: [false] }],
		               ["bold", "italic", "underline"], //, "image"
		               [{ 'list': 'bullet' }],
		               [{ "align": [] }],
		               ["clean"]
		          ],
		          
		          // Improved Line Break
		          modules: {        
		            clipboard: {
		              matchers: [
		                ['BR', window.top.lineBreakMatcher]
		              ]
		            },
		            keyboard: {
		              bindings: {
		                linebreak: {
		                  key: 13,
		                  shiftKey: true,
		                  handler: window.top.lineBreakHandler
		                }
		              }
		            }
		          }
		        })
        """)

		self.quill.on("editor-change", self.onEditorChange)

		if self.value:
			self["value"] = self.value

	def onDetach(self):
		super(HtmlEditor, self).onDetach()
		self.value = self["value"]

	def onEditorChange(self, *args, **kwargs):
		self.updateHtmlView()

	def updateHtmlView(self):
		self.htmlView["value"] = self["value"]

	def updateRichView(self):
		self["value"] = self.htmlView["value"]

	def onChange(self, event):
		if html5.utils.doesEventHitWidgetOrChildren(event, self.htmlView):
			self.updateRichView()

	def _getValue(self):
		if not self.quill:
			return self.value

		return self.quill.root.innerHTML

	def _setValue(self, val):
		if not self.quill:
			self.value = val
			return

		self.quill.root.innerHTML = val

	@classmethod
	def fromSkelStructure(cls, moduleName, boneName, skelStructure, *args, **kwargs):
		return cls(moduleName, boneName, skelStructure)

	@staticmethod
	def checkFor(moduleName, boneName, skelStructure, *args, **kwargs):
		if boneName in skelStructure.keys():
			if skelStructure[boneName].get("type") == "html":
				return True

			if "params" in skelStructure[boneName] and skelStructure[boneName]["params"]:
				return skelStructure[boneName]["params"].get("style") == "html"

		return False

	def unserialize(self, data, extendedErrorInformation = None):
		self["value"] = data.get(self.boneName)

	def serializeForPost(self):
		return {
			self.boneName: self["value"]
		}

	def serializeForDocument(self):
		return self.serializeForPost()

	def setExtendedErrorInformation(self, errorInfo):
		pass

editBoneSelector.insert(20, HtmlEditor.checkFor, HtmlEditor)
