$(function() {
	var editor = new Quill('#wysiwyg0');

	$( 'button.style' ).click(function() {
		var name = $(this).text();
		var fmt = editor.getFormat();
		var value = !fmt.hasOwnProperty(name);
		
		if (name == "super")				{ name = "subsuper";	value = "Super"; }
		if (name == "sub")					{ name = "subsuper";	value = "Sub"; }
		if (name == "justifyLeft")			{ name = "align";		value = "Left"; }
		if (name == "justifyCenter")		{ name = "align";		value = "Center"; }
		if (name == "justifyRight")			{ name = "align";		value = "Right"; }
		if (name == "justifyBlock")			{ name = "align";		value = "Justify"; }
		if (name == "H1")					{ name = "header";		value = 1; }
		if (name == "H2")					{ name = "header";		value = 2; }
		if (name == "H3")					{ name = "header";		value = 3; }
		if (name == "H4")					{ name = "header";		value = 4; }
		if (name == "insertOrderedList")	{ name = "list";		value = "ordered"; }
		if (name == "insertUnorderedList")	{ name = "list";		value = "bullet"; }

		if(name == "removeformat") {
			var r = editor.getSelection();
			if (r.length > 0) {
				editor.removeFormat(r.index, r.length, "user")
			}
			return;
		}
		if(name == "undo") {
			return editor.history.undo();
		}
		if(name == "redo") {
			return editor.history.redo();
		}
		
		editor.format(name, value, "user");
	});

	editor.on('editor-change', function(range, oldRange, source) {
		if (range) {
			var fmt = editor.getFormat();
			console.log(fmt);

			$( '.button' ).removeClass('is-active');
			$.each( fmt, function( key, value ) {
				$( '.button[data-group="' + key + '"][data-value="' + value + '"]').addClass('is-active');
			});
		}
	});

});