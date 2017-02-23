var counter = 1;

function comment(){

	if(counter>10){
    alert("Only 10 comments allowed");
    return false;
	}

	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", 'TextBoxDiv' + counter);

	newTextBoxDiv.after().html('<span id="draggable'+ counter+'">*' +
	      '<input type="text" name="textbox' + counter +
	      '" id="resizable' + counter +
        '" class="ui-state-active">'+'</span>');

	newTextBoxDiv.appendTo("#TextBoxesGroup");

	$("#resizable"+counter).resizable();
	$("#draggable"+counter).draggable();

	counter++;
}
