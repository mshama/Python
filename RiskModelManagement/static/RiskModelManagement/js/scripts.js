/**
 * 
 */

function overlayClick(overlayID) {
	el = document.getElementById(overlayID);
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function deleteRowEditTable(rowid) {
	
	var count = $('#riskfactor-composition-table-edit tr').length;
	if(count > 2) {
		var row = document.getElementById(rowid);
		var table = row.parentNode;
		while ( table && table.tagName != 'TABLE' )
			table = table.parentNode;
		if ( !table )
			return;
		table.deleteRow(row.rowIndex);
	}
	else if(count == 2) {
		$('select[name="riskfactor[]"]').val('');
		$('input[name="weight[]"]').val('');
	}
}

function addRowEditTable(){
	var table = document.getElementById("riskfactor-composition-table-edit");
	
	var tbody = table.children[0];
	
	tbody.insertBefore(table.rows[0].cloneNode(true), table.rows[0]);
	
}

function addRow(){
	var table = document.getElementById("riskfactor-composition-table");
	
	var tbody = table.children[0];
	
	tbody.insertBefore(table.rows[1].cloneNode(true), table.rows[1]);
	
}

function sortRiskfactors() {
	
	var riskfactorListSelect = document.getElementById("riskfactorList");
	
	var tmpAry = new Array();
	
	for (var i = 0; i < riskfactorListSelect.options.length; i++) {
		tmpAry[i] = new Array();		
		if(document.getElementById("sortBy").selectedIndex == 1){
			tmpAry[i][0] = riskfactorListSelect.options[i].text;
			tmpAry[i][1] = Number(riskfactorListSelect.options[i].value);
		} else {			
			tmpAry[i][0] = Number(riskfactorListSelect.options[i].value);
			tmpAry[i][1] = riskfactorListSelect.options[i].text;
		}
	}
	if(document.getElementById("sortBy").selectedIndex == 1){
		tmpAry.sort();
	} else {
		tmpAry.sort(sortNumber);
	}

	while (riskfactorListSelect.options.length > 0) {
		riskfactorListSelect.options[0] = null;
	}
	
	for (var i = 0; i < tmpAry.length; i++) {
		if(document.getElementById("sortBy").selectedIndex == 1){
			var op = new Option(tmpAry[i][0], tmpAry[i][1]);
		} else {
			var op = new Option(tmpAry[i][1], tmpAry[i][0]);
		}
		riskfactorListSelect.options[i] = op;
	}

	return;
}