// Informal source: https://quilljs.com/guides/cloning-medium-with-parchment/

// Global import
let Parchment = Quill.import("parchment");

// Default block
class Block extends Quill.import("blots/block")
{
	static create(value)
	{
		let node = super.create(value);
		node.setAttribute("class", "vitxt-paragraph");
		return node;
	}
}

Quill.register(Block, true);

// Bold
class BoldBlot extends Quill.import("formats/bold")
{
	static create(value)
	{
		let node = super.create(value);
		node.setAttribute("class", "vitxt-fBold");
		return node;
	}
}

BoldBlot.blotName = "bold";
BoldBlot.tagName = ["strong"];

Quill.register(BoldBlot, true);

// Italic
class ItalicBlot extends Quill.import("formats/italic")
{
	static create(value)
	{
		let node = super.create(value);
		node.setAttribute("class", "vitxt-fItalic");
		return node;
	}
}

ItalicBlot.blotName = "italic";
ItalicBlot.tagName = ["em"];

Quill.register(ItalicBlot, true);



// Super & Sub
class SuperSubBlot extends Quill.import("blots/inline")
{
	static create(value)
	{
		let node = super.create(value);
		node.setAttribute("class", "vitxt-f" + value);
		
		return node;
	}
	static formats(domNode) {
		return domNode.tagName.charAt(0).toUpperCase() +
		domNode.tagName.slice(1).toLowerCase();
	}
}

SuperSubBlot.tagName = ["sub", "sup"];
SuperSubBlot.blotName = "subsuper";

Quill.register(SuperSubBlot, true);

// Blockquote
class BlockquoteBlot extends Quill.import("formats/blockquote")
{
	static create(value)
	{
		let node = super.create(value);
		node.setAttribute("class", "vitxt-tQuote");
		return node;
	}
}

Quill.register(BlockquoteBlot, true);

// Header
class HeaderBlot extends Quill.import("formats/header")
{
	static create(value)
	{
		let cl = {
			1: "title",
			2: "large",
			3: "medium",
			4: "small",
		};

		let node = super.create(value);
		node.setAttribute("class", "vitxt-tHeading vitxt-tHeading-" + cl[value]);
		return node;
	}
}

HeaderBlot.blotName = "header";
HeaderBlot.tagName = ["h1", "h2", "h3", "h4"];
Quill.register(HeaderBlot, true);

// Align
let alignOptions = { scope: Parchment.Scope.BLOCK, whitelist: ["Left", "Right", "Center", "Justify"] };
let AlignClass = new Parchment.Attributor.Class("align", "vitxt-a", alignOptions);
Quill.register({"attributors/class/align": AlignClass,
	"formats/align": AlignClass}, true);


// List
class ListBlot extends Quill.import("formats/list")
{
	static create(value)
	{
		let node = super.create(value);
		if (value == "ordered")
		{
			node.setAttribute("class", "vitxt-list vitxt-listOrder");
		}
		else if (value == "bullet")
		{
			node.setAttribute("class", "vitxt-list vitxt-listUnorder");
		}

		return node;
	}
}

Quill.register(ListBlot, true);

// List Item
class ListItemBlot extends Quill.import("formats/list/item")
{
	static create(value)
	{
		let node = super.create(value);
		node.setAttribute("class", "vitxt-listItem");

		return node;
	}
}

Quill.register(ListItemBlot, true);


let indentAttributor = new Parchment.Attributor.Attribute('indent', 'data-indent', { 
	scope: Parchment.Scope.BLOCK
});
Quill.register(indentAttributor);

// Link
class LinkBlot extends Quill.import("formats/link")
{
	static create(value)  {
		console.log(value);

		let node = super.create(value.href);

		node.setAttribute('href', value.href);
		if (value.target) {
			node.setAttribute('target', value.target);
		} else {
			node.removeAttribute('target');
		}

		if (value.title) {
			node.setAttribute('title', value.title);
		} else {
			node.removeAttribute('title');
		}

		if (value.isDownload || (" " + node.className + " ").replace(/[\n\t]/g, " ").indexOf(" vitxt-download ") > -1 ) {
			node.setAttribute('class', "vitxt-download");
		} else {
			node.setAttribute('class', "vitxt-link");
		}
		return node;
	}

	static format(name, value)
	{
		if( !value )
			return;

		super.format(name, value.href); // use value.href here because the super class doesnt support objects

		this.domNode.setAttribute('href', value.href);
		if (value.target) {
			this.domNode.setAttribute('target', value.target);
		} else {
			this.domNode.removeAttribute('target');
		}

		if (value.title) {
			this.domNode.setAttribute('title', value.title);
		} else {
			this.domNode.removeAttribute('title');
		}
	}

	static formats(node)
	{
		return {
			href: node.getAttribute('href'),
			target: node.getAttribute('target'),
			title: node.getAttribute('title'),
		}
	}

}
LinkBlot.blotName = 'link';
LinkBlot.tagName = 'A';

Quill.register(LinkBlot, true);

// Image
class ImageBlot extends Quill.import('blots/embed') {
	static create(value)
	{
		console.log(value);
		let node = super.create();
		node.setAttribute('class', "vitxt-image");
		node.setAttribute('alt', value.alt);
		node.setAttribute('src', value.url);
		return node;
	}

	static value(node) {
		return {
			alt: node.getAttribute('alt'),
			url: node.getAttribute('src')
		};
	}
}
ImageBlot.blotName = 'image';
ImageBlot.tagName = 'img';

Quill.register(ImageBlot, true);

// Hr
class DividerBlot extends Quill.import('blots/embed') {
	static create(value)
	{
		let node = super.create();
		node.setAttribute('class', "vitxt-rule");
		return node;
	}
}
DividerBlot.blotName = 'divider';
DividerBlot.tagName = 'hr';
Quill.register(DividerBlot, true);