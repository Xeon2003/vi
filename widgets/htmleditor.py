import html5
import network
from __pyjamas__ import JS
from i18n import translate
from widgets.file import FileWidget
from config import conf
from utils import getImagePreview


class TextInsertImageAction(html5.ext.Button):
	def __init__(self, summernote=self, boneName="", *args, **kwargs):
		super(TextInsertImageAction, self).__init__(translate("Insert Image"), *args, **kwargs)
		self["class"] = "icon text image viur-insert-image-btn"
		self["title"] = translate("Insert Image")
		self["style"]["display"] = "none"
		self.element.setAttribute("data-bonename", boneName)
		self.summernote = summernote

	def onClick(self, sender=None):
		currentSelector = FileWidget("file", isSelector=True)
		currentSelector.selectionActivatedEvent.register(self)
		conf["mainWindow"].stackWidget(currentSelector)

	def onSelectionActivated(self, selectWdg, selection):
		print "onSelectionActivated"

		if not selection:
			return

		print selection

		for item in selection:
			if "mimetype" in item.data.keys() and item.data["mimetype"].startswith("image/"):
				dataUrl = getImagePreview(item.data)

				self.summernote.summernote("editor.insertImage", dataUrl, item.data["name"].replace("\"", ""))
				print "insert img %s" % dataUrl
			else:
				dataUrl = "/file/download/%s/%s" % (
					item.data["dlkey"], item.data["name"].replace("\"", ""))
				text = item.data["name"].replace("\"", "")

				self.summernote.summernote("editor.createLink",
										   JS("{url: @{{dataUrl}}, text: @{{text}}, isNewWindow: true}"))
				print "insert link %s<%s> " % (text, dataUrl)

	@staticmethod
	def isSuitableFor(modul, handler, actionName):
		return (actionName == "text.image")

	def resetLoadingState(self):
		pass


class HtmlEditor(html5.Textarea):
	def __init__(self, *args, **kwargs):
		super(HtmlEditor, self).__init__(*args, **kwargs)

		self.value = ""
		self.summernote = None
		self.enabled = True
		self.summernoteContainer = self
		self.boneName = ""

	def _attachSummernote(self, retry=0):
		elem = self.summernoteContainer.element

		try:
			self.summernote = JS("""window.top.createSummernote(@{{elem}})""")

		except:
			if retry >= 3:
				alert("Unable to connect summernote, please contact technical support...")
				return

			print("Summernote initialization failed, retry will start in 1sec")
			network.DeferredCall(self._attachSummernote, retry=retry + 1, _delay=1000)
			return

		self.summernote.on("summernote.change", self.onEditorChange)

		if self.value:
			self["value"] = self.value

	def onAttach(self):
		super(HtmlEditor, self).onAttach()

		if self.summernote:
			return

		self._attachSummernote()

		if not self.enabled:
			self.summernote.summernote("disable")

		self.element.setAttribute("data-bonename", self.boneName)

		imagebtn = TextInsertImageAction(summernote=self.summernote, boneName=self.boneName)
		self.parent().appendChild(imagebtn)

	def onDetach(self):
		super(HtmlEditor, self).onDetach()
		self.value = self["value"]
		self.summernote.summernote('destroy')
		self.summernote = None

	def onEditorChange(self, e, *args, **kwargs):
		if self.parent():
			e = JS("new Event('keyup')")
			self.parent().element.dispatchEvent(e)

	def _getValue(self):
		if not self.summernote:
			return self.value

		ret = self.summernote.summernote("code")
		return ret

	def _setValue(self, val):
		if not self.summernote:
			self.value = val
			return

		self.summernote.summernote("reset")  # reset history and content
		self.summernote.summernote("code", val)

	def enable(self):
		super(HtmlEditor, self).enable()

		self.enabled = True
		self.removeClass("is-disabled")

		if self.summernote:
			self.summernote.summernote("enable")

	def disable(self):
		super(HtmlEditor, self).disable()

		self.enabled = False
		self.addClass("is-disabled")

		if self.summernote:
			self.summernote.summernote("disable")