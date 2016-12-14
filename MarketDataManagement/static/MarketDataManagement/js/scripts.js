/**
 * 
 */

function updateDatabaseTables() {
	var selectedDataSource = $('select[name=data_source]').val() + '-option';
	$("#related_databasetables option").attr('disabled','disabled');
	
	var selectedOptions = document.querySelectorAll('option.' + selectedDataSource);
    i = 0;
    len = selectedOptions.length;

	for (; i < len; i++) {
		selectedOptions[i].disabled = false;
	}
}

function setFieldParametersOptions(){
	var selectedType = $('select[name=fieldtype]').val();
	console.log(selectedType);
	
	document.getElementById('field-parameters-div').innerHTML = "";
	switch(selectedType) {
		case "DecimalField":		
			var max_digits = document.createElement("input");
			max_digits.type = "number";
			max_digits.name = "max_digits";
			max_digits.step = 1;
			
			var max_digits_label = document.createElement("Label");
			max_digits_label.appendChild(document.createTextNode("Max digits: "));
			max_digits_label.setAttribute("for", max_digits);
			
			document.getElementById('field-parameters-div').appendChild(max_digits_label);
			document.getElementById('field-parameters-div').appendChild(max_digits);
			
			document.getElementById('field-parameters-div').appendChild(document.createElement("br"));
			document.getElementById('field-parameters-div').appendChild(document.createElement("br"));
			
			var decimal_places = document.createElement("input");
			decimal_places.type = "number";
			decimal_places.name = "decimal_places";
			decimal_places.step = 1;
			
			var decimal_places_label = document.createElement("Label");
			decimal_places_label.appendChild(document.createTextNode("Decimal places: "));
			decimal_places_label.setAttribute("for", decimal_places);
			
			document.getElementById('field-parameters-div').appendChild(decimal_places_label);
			document.getElementById('field-parameters-div').appendChild(decimal_places);
			break;
		case "CharField":
			var max_length = document.createElement("input");
			max_length.type = "number";
			max_length.name = "max_length";
			max_length.step = 1;
			
			var max_length_label = document.createElement("Label");
			max_length_label.appendChild(document.createTextNode("Max length: "));
			max_length_label.setAttribute("for", max_length);
			
			document.getElementById('field-parameters-div').appendChild(max_length_label);
			document.getElementById('field-parameters-div').appendChild(max_length);
			break;
		default:
			document.getElementById('field-parameters-div').innerHTML = "";
			break;
	}
}

function overlayClick(overlayID) {
	el = document.getElementById(overlayID);
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}


ajaxPost = function (currentInstrumentIndex) {
	if (currentInstrumentIndex < instrumentList.length) {
		return $.ajax({
			type : "POST",
			url : "/MarketDataManagement/updateData/",
			data : {
				currentInstrument : instrumentList[currentInstrumentIndex].code_c,
				source : source,
				fullData : fullData,
				csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]')
						.val(),
			},
			success : function() {
				$("#automaticLoading").val("1");
				$("#currentInstrument").html(
						"<h4>" + instrumentList[currentInstrumentIndex].instrument__name_c
								+ "</h4>");
				$("#progressbar").css(
						{
							"width" : Math.round(100 * (currentInstrumentIndex+1)
									/ instrumentList.length)
									+ "%",
							"color" : "black",
							"background-color" : "red",
							"border-radius" : "4px"
						});
				$("#progresspercentage").html(
						Math.round(100 * (currentInstrumentIndex+1)
								/ instrumentList.length)
								+ "%");
			}
		});
	}
}