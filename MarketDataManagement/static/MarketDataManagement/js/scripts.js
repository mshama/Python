/**
 * 
 */

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