#-*- coding: utf-8 -*-
import html5, json
from i18n import translate
from __pyjamas__ import JS

class LinkEditor(html5.Div):
	targets = ["", "_blank", "_self", "_parent", "_top"]

	def __init__(self, parent, *args, **kwargs):
		assert isinstance(parent, TextEditor)

		super(LinkEditor, self).__init__(*args, **kwargs)
		self.addClass("vi-editor-link-edit")

		self.parent = parent
		self.mode = "edit"

		# URL
		lbl = html5.Label(translate("URL"))
		self.appendChild(lbl)

		self.url = html5.Input()
		lbl.appendChild(self.url)

		# Target
		lbl = html5.Label(translate("Target"))
		self.appendChild(lbl)

		self.target = html5.Select()
		lbl.appendChild(self.target)

		for t in self.targets:
			opt = html5.Option(t)
			opt["value"] = t
			self.target.appendChild(opt)

		# Title
		lbl = html5.Label(translate("Title"))
		self.appendChild(lbl)

		self.title = html5.Input()
		lbl.appendChild(self.title)

		# Buttons
		btnSave = html5.ext.Button(translate("Save"), callback=self.save)
		btnSave.addClass("button", "save")
		self.appendChild(btnSave)

		btnDelete = html5.ext.Button(translate("Delete"), callback=self.delete)
		btnDelete.addClass("button", "delete")
		self.appendChild(btnDelete)

		self.hide()

	def show(self, href = None, title = None, target = None, **attr):
		if href is None:
			self.mode = "add"
		else:
			self.mode = "edit"

		self.url["value"] = href or ""
		self.title["value"] = title or ""

		if target in self.targets:
			self.target.children(self.targets.index(target))["selected"] = True
		else:
			self.target.children(0)["selected"] = True

		super(LinkEditor, self).show()

	def save(self, *args, **kwargs):
		url = self.url["value"]
		if url and not url.startswith("/file/") and not url.startswith("http"):
			url = "http://" + url

		if self.mode == "edit":
			fmt = self.parent.getFormat("link")
			if not fmt:
				self.hide()
				return

			range = self.parent.quill.getSelection()
			start = range.index
			length = 1

			while start > 0 and self.parent.getFormat("link", start) == fmt:
				start -= 1

			while length < self.parent.quill.getLength() and self.parent.getFormat("link", start, length + 1) == fmt:
				length += 1

			self.parent.quill.setSelection(start, length)

		self.parent.format("link", href=url, title=self.title["value"],
		                    target=self.targets[self.target["selectedIndex"]])

		self.hide()

	def delete(self, *args, **kwargs):
		self.parent.format("link")
		self.hide()

class TextEditor(html5.Div):
	def __init__(self):
		super(TextEditor, self).__init__()

		self.value = ""
		self.quill = None

		self.quillContainer = self
		self.actionContainer = self

		self.linkEditor = LinkEditor(self)

	def onAttach(self):
		super(TextEditor, self).onAttach()

		if self.quill:
			return

		imageHandler = self.imageHandler
		linkHandler = self.linkHandler

		elem = self.quillContainer.element
		self.quill = JS("""
			new window.top.quill(@{{elem}},
			{
				modules: {
					toolbar: {
						container: [
							[{header: [1, 2, false]}],
							["bold", "italic", "underline"],
							["image", "link"],
							[{"align": []}],
							[{"color": []}],
							["clean"]
						],
						handlers: {
							"image": @{{imageHandler}},
							"link": @{{linkHandler}}
						}
					}
		        },
	            theme: "viur"
            })
        """)

		self.quill.on("editor-change", self.eventQuillEditorChange)
		self.quill.on("selection-change", self.eventQuillSelectionChange)

		if self.value:
			self["value"] = self.value

		self.actionContainer.appendChild(self.linkEditor)

	def onDetach(self):
		super(TextEditor, self).onDetach()
		self.value = self["value"]

	def _getValue(self):
		if not self.quill:
			return self.value

		ret = self.quill.root.innerHTML
		if ret.strip() == "<p><br></p>":
			ret = ""

		return ret

	def _setValue(self, val):
		if not self.quill:
			self.value = val
			return

		self.quill.root.innerHTML = val

	# Quill-related function wrapping

	def eventQuillEditorChange(self, e):
		assert self.quill

		if self.parent():
			e = JS("new Event('keyup')")
			self.parent().element.dispatchEvent(e)

	def eventQuillSelectionChange(self, range, oldRange, source, *args, **kwargs):
		assert self.quill

		print("eventQuillSelectionChange", source)

		if range and source == "user" and range.length == 0:
			fmt = self.getFormat("link", range.index, 1)
			if fmt:
				self.linkEditor.show(**fmt)
			else:
				self.linkEditor.hide()

	def format(self, name, **attr):
		assert self.quill

		attr = json.dumps(attr)

		print("set:", attr)
		self.quill.format(name, JS("JSON.parse(@{{attr}})"))

	def getFormat(self, name, start = None, length = None):
		assert self.quill

		if start:
			if length is not None:
				fmt = self.quill.getFormat(start, length)
			else:
				fmt = self.quill.getFormat(start)
		else:
			fmt = self.quill.getFormat()

		#JS("console.log(fmt)")
		attr = JS("@{{fmt}}[@{{name}}]")
		#JS("console.log(attr)")
		#print(attr)
		attr = json.loads(JS("JSON.stringify(@{{attr}})"))

		print("get:", attr)
		return attr

	def imageHandler(self, *args, **kwargs):
		alert("Image!")

	def linkHandler(self, *args, **kwargs):
		assert self.quill
		self.linkEditor.show()

class HtmlEditor(TextEditor):
	def __init__(self, showHtml=False):
		super(HtmlEditor, self).__init__()
		self.sinkEvent("onChange")

		self.mode = "quill"

		self.fromHTML("""
			<div [name]="sourceQuill" class="vi-editor-quill">
				<div [name]="QUILL" />
			</div>
			<div [name]="sourceHtml" class="vi-editor-html" hidden>
				<textarea [name]="html"></textarea>
			</div>

			<div class="vi-editor-html-switch">
				<label><input type="checkbox" [name]="showHtml"> HTML</label>
			</div>
		""", )

		self.quillContainer = self.QUILL
		self.actionContainer = self.sourceQuill

		self.showHtml["checked"] = showHtml
		if self.showHtml["checked"]:
			self.switchMode()

	def onChange(self, event):
		if html5.utils.doesEventHitWidgetOrChildren(event, self.showHtml):
			self.switchMode()

	def switchMode(self):
		content = self["value"]

		if self.mode == "quill":
			self.mode = "html"
			self.sourceQuill.hide()
			self.sourceHtml.show()

			self.showHtml["checked"] = True
		else:
			self.mode = "quill"
			self.sourceHtml.hide()
			self.sourceQuill.show()

			self.showHtml["checked"] = False

		self["value"] = content

	def insertTemplate(self, code):
		if self.mode == "quill":
			assert self.quill
			sel = self.quill.getSelection()

			if sel is None:
				sel = object()
				sel.index = sel.length = 0

			if "..." in code and sel.length:
				txt = self.quill.getText(sel.index, sel.length)
				self.quill.deleteText(sel.index, sel.length)

				pos = code.index("...")

				self.quill.insertText(sel.index, code[pos + 3:])
				self.quill.insertText(sel.index, txt)
				self.quill.insertText(sel.index, code[:pos])
			else:
				self.quill.insertText(sel.index, code)

			self.quill.root.focus()

		else:
			start = self.html.element.selectionStart
			end = self.html.element.selectionEnd

			pre = self.html["value"][:start]
			sel = self.html["value"][start:end]
			post = self.html["value"][end:]

			if "..." in code:
				code = code.replace("...", sel, 1)

			self["value"] = pre + code + post

			end = start + len(code)

			self.html.element.selectionStart = start
			self.html.element.selectionEnd = end
			self.html.focus()

	def _getValue(self):
		if self.mode == "html":
			return self.html["value"]

		return super(HtmlEditor, self)._getValue()

	def _setValue(self, val):
		if self.mode == "html":
			self.html["value"] = val
			return

		super(HtmlEditor, self)._setValue(val)
