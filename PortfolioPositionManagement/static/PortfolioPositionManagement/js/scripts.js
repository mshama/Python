/**
 * 
 */

ajaxPost = function (event) {
	var url = "/PortfolioPositionManagement/viewPortfolios/";
	return $.ajax({
		type : "POST",
		url : url,
		data : { 
			'changes[]' : changedPortfolios, 
			csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
		},
		success : function(responseData, textStatus, jqXHR) {
			window.location.reload(true);
			if( responseData == 1) {
				$('#message').text("Changes were saved successfully");
		    	$('#message').css('color', '#28B463');
			} else {
				$('#message').text(responseData);
		    	$('#message').css('color', 'red');
			}
			
	    	changedPortfolios = [];
	    	$("#save-button").prop("disabled",true);
		}
	});
}

function overlayClick(overlayID) {
	el = document.getElementById(overlayID);
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function updateChangedPortfolios(portfolio_id, checkBox){
	if (checkBox.is(':checked')) {
		changedPortfolios.push([portfolio_id, true]);
	} else {
		changedPortfolios.push([portfolio_id, false]);
	}
	
	if($("#save-button").is(":disabled")) {
		$("#save-button").removeAttr('disabled');
	}
}