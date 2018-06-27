let Parchment = Quill.import("parchment");

// ViUR-customized link
let Link = Quill.import("formats/link");

class LinkBlot extends Link {
	static create(value)
		{
			console.log("LinkBlot.create, value = ", value);

			let node = super.create(value.href);

			if(value.target)
				node.setAttribute("target", value.target);
			else
				node.removeAttribute("target");

			if(value.title)
				node.setAttribute("title", value.title);
			else
				node.removeAttribute("title");

			console.log("LinkBlot.create, node = ", node);
			return node;
		}

	format(name, value)
		{
			console.log("LinkBlot.format", name, value);

			if( !value )
				return;

			super.format(name, value.href); // use value.href here because the super class doesnt support objects

			this.domNode.setAttribute("href", value.href);

			if(value.target)
				this.domNode.setAttribute("target", value.target);
			else
				this.domNode.removeAttribute("target");

			if(value.title)
				this.domNode.setAttribute("title", value.title);
			else
				this.domNode.removeAttribute("title");
		}

	static formats(node)
		{
			if( !node )
				return {};

			return {
				href: node.getAttribute("href"),
				target: node.getAttribute("target"),
				title: node.getAttribute("title")
			}
		}

}

LinkBlot.blotName = "link";
LinkBlot.tagName = "A";

Quill.register(LinkBlot, true);

//Viur Theme

let BaseTheme = Quill.import("themes/snow");
let icons = Quill.import("ui/icons");

const TOOLBAR_CONFIG = [
  [{ header: ['1', '2', '3', false] }],
  ['bold', 'italic', 'underline', 'link'],
  [{ list: 'ordered' }, { list: 'bullet' }],
  ['clean']
];

class ViurTheme extends BaseTheme {
  constructor(quill, options) {
    if (options.modules.toolbar != null && options.modules.toolbar.container == null) {
      options.modules.toolbar.container = TOOLBAR_CONFIG;
    }
    super(quill, options);
    this.quill.container.classList.add('ql-viur');
  }

  extendToolbar(toolbar) {
    toolbar.container.classList.add('ql-viur');
    this.buildButtons([].slice.call(toolbar.container.querySelectorAll('button')), icons);
    this.buildPickers([].slice.call(toolbar.container.querySelectorAll('select')), icons);
  }
}

Quill.register("themes/viur", ViurTheme);
