"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// Informal source: https://quilljs.com/guides/cloning-medium-with-parchment/

// Global import
var Parchment = Quill.import("parchment");

// Default block

var Block = function (_Quill$import) {
	_inherits(Block, _Quill$import);

	function Block() {
		_classCallCheck(this, Block);

		return _possibleConstructorReturn(this, (Block.__proto__ || Object.getPrototypeOf(Block)).apply(this, arguments));
	}

	_createClass(Block, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(Block.__proto__ || Object.getPrototypeOf(Block), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-paragraph");
			return node;
		}
	}]);

	return Block;
}(Quill.import("blots/block"));

Quill.register(Block, true);

// Bold

var BoldBlot = function (_Quill$import2) {
	_inherits(BoldBlot, _Quill$import2);

	function BoldBlot() {
		_classCallCheck(this, BoldBlot);

		return _possibleConstructorReturn(this, (BoldBlot.__proto__ || Object.getPrototypeOf(BoldBlot)).apply(this, arguments));
	}

	_createClass(BoldBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(BoldBlot.__proto__ || Object.getPrototypeOf(BoldBlot), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-fBold");
			return node;
		}
	}]);

	return BoldBlot;
}(Quill.import("formats/bold"));

BoldBlot.blotName = "bold";
BoldBlot.tagName = ["strong"];

Quill.register(BoldBlot, true);

// Italic

var ItalicBlot = function (_Quill$import3) {
	_inherits(ItalicBlot, _Quill$import3);

	function ItalicBlot() {
		_classCallCheck(this, ItalicBlot);

		return _possibleConstructorReturn(this, (ItalicBlot.__proto__ || Object.getPrototypeOf(ItalicBlot)).apply(this, arguments));
	}

	_createClass(ItalicBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(ItalicBlot.__proto__ || Object.getPrototypeOf(ItalicBlot), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-fItalic");
			return node;
		}
	}]);

	return ItalicBlot;
}(Quill.import("formats/italic"));

ItalicBlot.blotName = "italic";
ItalicBlot.tagName = ["em"];

Quill.register(ItalicBlot, true);

// Super & Sub

var SuperSubBlot = function (_Quill$import4) {
	_inherits(SuperSubBlot, _Quill$import4);

	function SuperSubBlot() {
		_classCallCheck(this, SuperSubBlot);

		return _possibleConstructorReturn(this, (SuperSubBlot.__proto__ || Object.getPrototypeOf(SuperSubBlot)).apply(this, arguments));
	}

	_createClass(SuperSubBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(SuperSubBlot.__proto__ || Object.getPrototypeOf(SuperSubBlot), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-f" + value);

			return node;
		}
	}, {
		key: "formats",
		value: function formats(domNode) {
			return domNode.tagName.charAt(0).toUpperCase() + domNode.tagName.slice(1).toLowerCase();
		}
	}]);

	return SuperSubBlot;
}(Quill.import("blots/inline"));

SuperSubBlot.tagName = ["sub", "sup"];
SuperSubBlot.blotName = "subsuper";

Quill.register(SuperSubBlot, true);

// Blockquote

var BlockquoteBlot = function (_Quill$import5) {
	_inherits(BlockquoteBlot, _Quill$import5);

	function BlockquoteBlot() {
		_classCallCheck(this, BlockquoteBlot);

		return _possibleConstructorReturn(this, (BlockquoteBlot.__proto__ || Object.getPrototypeOf(BlockquoteBlot)).apply(this, arguments));
	}

	_createClass(BlockquoteBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(BlockquoteBlot.__proto__ || Object.getPrototypeOf(BlockquoteBlot), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-tQuote");
			return node;
		}
	}]);

	return BlockquoteBlot;
}(Quill.import("formats/blockquote"));

Quill.register(BlockquoteBlot, true);

// Header

var HeaderBlot = function (_Quill$import6) {
	_inherits(HeaderBlot, _Quill$import6);

	function HeaderBlot() {
		_classCallCheck(this, HeaderBlot);

		return _possibleConstructorReturn(this, (HeaderBlot.__proto__ || Object.getPrototypeOf(HeaderBlot)).apply(this, arguments));
	}

	_createClass(HeaderBlot, null, [{
		key: "create",
		value: function create(value) {
			var cl = {
				1: "title",
				2: "large",
				3: "medium",
				4: "small"
			};

			var node = _get(HeaderBlot.__proto__ || Object.getPrototypeOf(HeaderBlot), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-tHeading vitxt-tHeading-" + cl[value]);
			return node;
		}
	}]);

	return HeaderBlot;
}(Quill.import("formats/header"));

HeaderBlot.blotName = "header";
HeaderBlot.tagName = ["h1", "h2", "h3", "h4"];
Quill.register(HeaderBlot, true);

// Align
var alignOptions = { scope: Parchment.Scope.BLOCK, whitelist: ["Left", "Right", "Center", "Justify"] };
var AlignClass = new Parchment.Attributor.Class("align", "vitxt-a", alignOptions);
Quill.register({ "attributors/class/align": AlignClass,
	"formats/align": AlignClass }, true);

// List

var ListBlot = function (_Quill$import7) {
	_inherits(ListBlot, _Quill$import7);

	function ListBlot() {
		_classCallCheck(this, ListBlot);

		return _possibleConstructorReturn(this, (ListBlot.__proto__ || Object.getPrototypeOf(ListBlot)).apply(this, arguments));
	}

	_createClass(ListBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(ListBlot.__proto__ || Object.getPrototypeOf(ListBlot), "create", this).call(this, value);
			if (value == "ordered") {
				node.setAttribute("class", "vitxt-list vitxt-listOrder");
			} else if (value == "bullet") {
				node.setAttribute("class", "vitxt-list vitxt-listUnorder");
			}

			return node;
		}
	}]);

	return ListBlot;
}(Quill.import("formats/list"));

Quill.register(ListBlot, true);

// List Item

var ListItemBlot = function (_Quill$import8) {
	_inherits(ListItemBlot, _Quill$import8);

	function ListItemBlot() {
		_classCallCheck(this, ListItemBlot);

		return _possibleConstructorReturn(this, (ListItemBlot.__proto__ || Object.getPrototypeOf(ListItemBlot)).apply(this, arguments));
	}

	_createClass(ListItemBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(ListItemBlot.__proto__ || Object.getPrototypeOf(ListItemBlot), "create", this).call(this, value);
			node.setAttribute("class", "vitxt-listItem");

			return node;
		}
	}]);

	return ListItemBlot;
}(Quill.import("formats/list/item"));

Quill.register(ListItemBlot, true);

var indentAttributor = new Parchment.Attributor.Attribute('indent', 'data-indent', {
	scope: Parchment.Scope.BLOCK
});
Quill.register(indentAttributor);

// Link

var LinkBlot = function (_Quill$import9) {
	_inherits(LinkBlot, _Quill$import9);

	function LinkBlot() {
		_classCallCheck(this, LinkBlot);

		return _possibleConstructorReturn(this, (LinkBlot.__proto__ || Object.getPrototypeOf(LinkBlot)).apply(this, arguments));
	}

	_createClass(LinkBlot, null, [{
		key: "create",
		value: function create(value) {
			console.log(value);

			var node = _get(LinkBlot.__proto__ || Object.getPrototypeOf(LinkBlot), "create", this).call(this, value.href);

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

			if (value.isDownload || (" " + node.className + " ").replace(/[\n\t]/g, " ").indexOf(" vitxt-download ") > -1) {
				node.setAttribute('class', "vitxt-download");
			} else {
				node.setAttribute('class', "vitxt-link");
			}
			return node;
		}
	}, {
		key: "format",
		value: function format(name, value) {
			if (!value) return;

			_get(LinkBlot.__proto__ || Object.getPrototypeOf(LinkBlot), "format", this).call(this, name, value.href); // use value.href here because the super class doesnt support objects

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
	}, {
		key: "formats",
		value: function formats(node) {
			return {
				href: node.getAttribute('href'),
				target: node.getAttribute('target'),
				title: node.getAttribute('title')
			};
		}
	}]);

	return LinkBlot;
}(Quill.import("formats/link"));

LinkBlot.blotName = 'link';
LinkBlot.tagName = 'A';

Quill.register(LinkBlot, true);

// Image

var ImageBlot = function (_Quill$import10) {
	_inherits(ImageBlot, _Quill$import10);

	function ImageBlot() {
		_classCallCheck(this, ImageBlot);

		return _possibleConstructorReturn(this, (ImageBlot.__proto__ || Object.getPrototypeOf(ImageBlot)).apply(this, arguments));
	}

	_createClass(ImageBlot, null, [{
		key: "create",
		value: function create(value) {
			console.log(value);
			var node = _get(ImageBlot.__proto__ || Object.getPrototypeOf(ImageBlot), "create", this).call(this);
			node.setAttribute('class', "vitxt-image");
			node.setAttribute('alt', value.alt);
			node.setAttribute('src', value.url);
			return node;
		}
	}, {
		key: "value",
		value: function value(node) {
			return {
				alt: node.getAttribute('alt'),
				url: node.getAttribute('src')
			};
		}
	}]);

	return ImageBlot;
}(Quill.import('blots/embed'));

ImageBlot.blotName = 'image';
ImageBlot.tagName = 'img';

Quill.register(ImageBlot, true);

// Hr

var DividerBlot = function (_Quill$import11) {
	_inherits(DividerBlot, _Quill$import11);

	function DividerBlot() {
		_classCallCheck(this, DividerBlot);

		return _possibleConstructorReturn(this, (DividerBlot.__proto__ || Object.getPrototypeOf(DividerBlot)).apply(this, arguments));
	}

	_createClass(DividerBlot, null, [{
		key: "create",
		value: function create(value) {
			var node = _get(DividerBlot.__proto__ || Object.getPrototypeOf(DividerBlot), "create", this).call(this);
			node.setAttribute('class', "vitxt-rule");
			return node;
		}
	}]);

	return DividerBlot;
}(Quill.import('blots/embed'));

DividerBlot.blotName = 'divider';
DividerBlot.tagName = 'hr';
Quill.register(DividerBlot, true);
