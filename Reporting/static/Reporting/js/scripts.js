/**
 * 
 */
//window.print();

function drawChart_Rendite_Risiko() {
	
	var config = {
            type: 'line',
            data: {
                labels: dateArray,
                datasets: [
//                {
//                    label: "Euribor 3M",
//                    data: [
//                           {x: vola_annualisiert[5], y: performace_Auflage[5]}
//                           ],
//                    fill: false,
//                    backgroundColor: 'rgba(160,0,80,1)',
//                    borderColor: 'rgba(160,0,80,1)',
//                    pointRadius: 5,
//                },
//                {
//                    label: "30:70",
//                    data: [
//                           {x: vola_annualisiert[4], y: performace_Auflage[4]},
//                           ],
//                    fill: false,
//                    backgroundColor: 'rgba(80,0,160,1)',
//                    borderColor: 'rgba(80,0,160,1)',
//                    pointRadius: 5,
//                },
//                {
//                    label: "50:50",
//                    data: [
//                           {x: vola_annualisiert[3], y: performace_Auflage[3]},
//                           ],
//                    fill: false,
//                    backgroundColor: 'rgba(120,0,120,1)',
//                    borderColor: 'rgba(120,0,120,1)',
//                    pointRadius: 5,
//                },
                {
                    label: "Q.ELV",
                    data: [
                           {x: vola_annualisiert[1], y: performace_Auflage[1]},
                           ],
                    fill: false,
                    backgroundColor:  'rgba(255,0,0,1)',
                    borderColor: 'rgba(255,0,0,1)',
                    pointRadius: 5,
                },
//                {
//                    label: "70:30",
//                    data: [
//                           {x: vola_annualisiert[2], y: performace_Auflage[2]},
//                           ],
//                    fill: false,
//                    backgroundColor: 'rgba(200,40,20,1)',
//                    borderColor: 'rgba(200,40,20,1)',
//                    pointRadius: 5,
//                },
                {
                    label: "EuroStoxx 50",
                    data: [
                           {x: vola_annualisiert[0], y: performace_Auflage[0]},
                           ],
                    fill: false,
                    backgroundColor: 'rgba(0,0,255,1)',
                    borderColor: 'rgba(0,0,255,1)',
                    pointRadius: 5,
                },
                ]
            },
            options: {
                responsive: true,
                fontFamily: 'Futura Lt BT',
                title:{
                    display: true,
                    text:'Rendite und Risiko',
                    fontFamily: 'Futura Lt BT',
                    fontColor: 'rgba(0,0,0,1)',
                },
                tooltips: {
                    mode: 'label',
                },
                hover: {
                    mode: 'dataset'
                },
                legend: {
                    display: true,
                    labels: {
                    	fontFamily: 'Futura Lt BT',
                    },
                	position: 'bottom',
                },
                scales: {
                    xAxes: [{
                        type: 'linear',
                        position: 'top',
                        scaleLabel: {
                            display: true,
                            labelString: 'Volatilität %',
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	fontFamily: 'Futura Lt BT',
                        	callback: function(value, index, values) {
                            	return parseFloat(value).toFixed(0) + '%';
                            },
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                    }],
                    yAxes: [{
                        type: 'linear',
                        position: 'left',
                        scaleLabel: {
                            display: true,
                            labelString: 'Rendite(seit Fondsauflage) %',
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	max: parseFloat(Math.max.apply(null,performace_Auflage)).toFixed(0),
                        	min: parseFloat(Math.min.apply(null,performace_Auflage)).toFixed(0)-2,
                        	fontFamily: 'Futura Lt BT',
                        	callback: function(value, index, values) {
                            	return parseFloat(value).toFixed(0) + '%';
                            },
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                    }]
                },                          
            }
        };
	var ctx = document.getElementById("rendite-risiko-chart").getContext("2d");
    window.renditeScatterChart = new Chart(ctx, config);
}

function drawChart_Fondsperformance_YTD() {
	
	var es50_p_normalized = es50_p.slice(endYearIndex);
	var qelv_p_normalized = qelv_p.slice(endYearIndex);
	
	var normalizationFactorES50 = 100 - es50_p_normalized[0];
	var normalizationFactorQELV = 100 - qelv_p_normalized[0];
	
	var minES50 = Math.min.apply(null, es50_p_normalized);
	var minQELV = Math.min.apply(null, qelv_p_normalized);
	
	var maxES50 = Math.min.apply(null, es50_p_normalized);
	var maxQELV = Math.min.apply(null, qelv_p_normalized);
	
	for(var i = 0; i < es50_p_normalized.length; i++) {
		es50_p_normalized[i] = es50_p_normalized[i] + normalizationFactorES50;
		qelv_p_normalized[i] = qelv_p_normalized[i] + normalizationFactorQELV;
	}
	
	var config = {
            type: 'line',
            data: {
                labels: dateArray.slice(endYearIndex, endIndex),
                datasets: [{
                    label: "EuroStoxx 50",
                    data: es50_p_normalized,
                    fill: false,
                    backgroundColor: 'rgba(0,0,255,1)', //black
                    borderColor: 'rgba(0,0,255,1)',
                    pointRadius: 0,
                    borderWidth: 1.5,
                }, {
                    label: "Q.ELV",
                    fill: false,
                    data: qelv_p_normalized,
                    backgroundColor: 'rgba(255,0,0,1)', //blue
                    borderColor: 'rgba(255,0,0,1)',
                    pointRadius: 0,
                    borderWidth: 1.5,
                }]
            },
            options: {
                responsive: true,
                title:{
                    display: false,
                    text:'Fondsperformance YTD',
                    fontFamily: 'Futura Lt BT',
                	fontColor: 'rgba(0,0,0,1)',
                },
                tooltips: {
                    mode: 'label',                    
                },
                hover: {
                    mode: 'dataset'
                },
                legend: {
                    display: true,
                    labels: {
                    	fontFamily: 'Futura Lt BT',
                    	fontColor: 'rgba(0,0,0,1)',
                    },
                	position: 'bottom',
                },
                scales: {
                    xAxes: [{
                        display: true,
                        position: "bottom",
                        type: 'time',
                        scaleLabel: {
                            display: false,
                            fontFamily: 'Futura Lt BT',
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	autoSkip: true,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        	callback: function(value) { 
                        		return new Date(value).toLocaleDateString('de-DE', {month:'short', year:'numeric'}); 
                        	},
                        },
                        time: {
                        	displayFormats: {
                        		quarter: 'MMM YYYY',
                        	},
                        	unitStepSize: 1,
                        	min: dateArray[endYearIndex-10],
                        }
                    }],
                    yAxes: [{
                        display: true,
                        position: "left",
                        id: "y-axis-1",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            suggestedMin: 75,//Math.min(minES50, minQELV) - 10,
                            suggestedMax: Math.max(maxES50, maxQELV) + 20,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        }
                    },{
                        display: true,
                        position: "right",
                        id: "y-axis-2",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	drawBorder: true,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            suggestedMin: Math.min(minES50, minQELV) - 20,
                            suggestedMax: Math.max(maxES50, maxQELV) + 50,
                            fontSize: 0,
                        }
                    },]
                }
            }
        };
				
        var ctx = document.getElementById("fondsperformance-ytd-chart").getContext("2d");
        window.fondsperformanceYTDLineChart = new Chart(ctx, config);
        
        delete es50_p_normalized;
        delete qelv_p_normalized;
}

function drawChart_Fondsperformance_seit_auflage() {
	
	var minES50 = Math.min.apply(null, es50_p);
	var minQELV = Math.min.apply(null, qelv_p);
	
	var maxES50 = Math.min.apply(null, es50_p);
	var maxQELV = Math.min.apply(null, qelv_p);
	
	var config = {
            type: 'line',
            data: {
                labels: dateArray.slice(0,endIndex),
                datasets: [{
                    label: "EuroStoxx 50",
                    data: es50_p,
                    fill: false,
                    backgroundColor: 'rgba(0,0,255,1)', //black
                    borderColor: 'rgba(0,0,255,1)',
                    pointRadius: 0,
                    borderWidth: 1.5,
                }, {
                    label: "Q.ELV",
                    fill: false,
                    data: qelv_p,
                    backgroundColor: 'rgba(255,0,0,1)', //blue
                    borderColor: 'rgba(255,0,0,1)',
                    pointRadius: 0,
                    borderWidth: 1.5,
                }]
            },
            options: {
                responsive: true,
                title:{
                    display: true,
                    text:'Fondsperformance seit Auflage',
                    fontFamily: 'Futura Lt BT',
                	fontColor: 'rgba(0,0,0,1)',
                },
                tooltips: {
                    mode: 'label',                    
                },
                hover: {
                    mode: 'dataset'
                },
                legend: {
                    display: true,
                    labels: {
                    	fontFamily: 'Futura Lt BT',
                    	fontColor: 'rgba(0,0,0,1)',
                    },
                	position: 'bottom',
                },
                scales: {
                    xAxes: [{
                        display: true,
                        position: "bottom",
                        type: 'time',
                        scaleLabel: {
                            display: false,
                            fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	autoSkip: true,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        	callback: function(value) { 
                        		return new Date(value).toLocaleDateString('de-DE', {month:'short', year:'numeric'}); 
                        	},
                        },
                        time: {
                        	displayFormats: {
                        		quarter: 'MMM YYYY',
                        	},
                        	unitStepSize: 1,
                        }
                    }],
                    yAxes: [{
                        display: true,
                        position: "left",
                        id: "y-axis-1",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            suggestedMin: 75,//Math.min(minES50, minQELV) - 10,
                            suggestedMax: Math.max(maxES50, maxQELV) + 20,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        }
                    },{
                        display: true,
                        position: "right",
                        id: "y-axis-2",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	drawBorder: true,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            suggestedMin: Math.min(minES50, minQELV) - 20,
                            suggestedMax: Math.max(maxES50, maxQELV) + 50,
                            fontSize: 0,
                        	fontColor: 'rgba(0,0,0,1)',
                        }
                    },]
                }
            }
        };
				
        var ctx = document.getElementById("fondsperformance-seit-auflage-chart").getContext("2d");
        window.fondsperformanceAuflageLineChart = new Chart(ctx, config);
}

function drawChart_performancedifferenz() {
	
	var dateLabel = new Array(spread.length);
	for(var i=0; i<spread.length; i++) {
		if(i % 5 == 0) {
			dateLabel[i] = dateArray[i];
		} else {
			dateLabel[i] = "";
		}
	}
	
	var config = {
            type: 'bar',
            data: {
                labels: dateLabel,
                datasets: [{
                    label: "Performancedifferenz",
                    data: spread,
                    backgroundColor: 'rgba(255,0,0,1)', //blue
                    borderColor: 'rgba(255,0,0,1)',
                }]
            },
            options: {
                responsive: true,
                title:{
                    display: true,
                    text:'Performancedifferenz: Q.ELV vs Euro Stoxx 50',
                    fontFamily: 'Futura Lt BT',
                	fontColor: 'rgba(0,0,0,1)',
                },
                elements: {
                	rectangle: {
                		borderWidth: 2,
                	},
                },
                tooltips: {
                    mode: 'label',                    
                },
                hover: {
                    mode: 'dataset'
                },
                legend: {
                    display: false,
                    labels: {
                    	fontFamily: 'Futura Lt BT',
                    	fontColor: 'rgba(0,0,0,1)',
                    },
                	position: 'bottom',
                },
                scales: {
                    xAxes: [{
                        display: true,
                        position: "bottom",
//                        type: 'time',
                        scaleLabel: {
                            display: false,
                            fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	autoSkip: true,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        	maxRotation: 45,
                        	callback: function(value) { 
                        		if(value == "")
                        			return null;
                        		else
                        			return new Date(value).toLocaleDateString('de-DE', {month:'short', year:'numeric'});
                        	},
                        },
//                        time: {
//                        	displayFormats: {
//                        		quarter: 'MMM YYYY',
//                        	},
//                        	unitStepSize: 1,
//                        },
                    }],
                    yAxes: [{
                        display: true,
                        position: "left",
                        id: "y-axis-1",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                    },{
                        display: true,
                        position: "right",
                        id: "y-axis-2",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	drawBorder: true,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            fontSize: 0,
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                    },]
                },
            }
        };
				
        var ctx = document.getElementById("performancedifferenz-chart").getContext("2d");
        window.performancedifferenzBarChart = new Chart(ctx, config);
}

function drawChart_qelv_marketexposure() {
	
	var monatsultimo = (marketexposureData[marketexposureData.length-1] * 100) + 50;
	
	var dateLabel = new Array(marketexposureData.length);
	
	for(var i=0; i<marketexposureData.length; i++) {
		marketexposureData[i] = marketexposureData[i] * 100;
		if(i % 2 == 0) {
			dateLabel[i] = marketexposureDates[i];
		} else {
			dateLabel[i] = "";
		}
	}
	var config = {
            type: 'bar',
            data: {
                labels: dateLabel,
                datasets: [{
                    label: "Market Exposure History",
                    data: marketexposureData,
                    backgroundColor: 'rgba(255,0,0,1)', //blue
                    borderColor: 'rgba(255,0,0,1)',
                }]
            },
            options: {
                responsive: true,
                title:{
                    display: true,
                    text:'Q.ELV Marktexposure (neutrale = 50%), wirtschaftliche Aktienquote Monatsultimo: ' + monatsultimo + '%',
                    fontFamily: 'Futura Lt BT',
                    fontColor: 'rgba(0,0,0,1)',
                },
                elements: {
                	rectangle: {
                		borderWidth: 2,
                	},
                },
                tooltips: {
                    mode: 'label',                    
                },
                hover: {
                    mode: 'dataset'
                },
                legend: {
                    display: false,
                    labels: {
                    	fontFamily: 'Futura Lt BT',
                    },
                	position: 'bottom',
                },
                scales: {
                    xAxes: [{
                        display: true,
                        position: "bottom",
//                        type: 'time',
                        scaleLabel: {
                            display: false,
                            fontFamily: 'Futura Lt BT',
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                        	autoSkip: true,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                        	callback: function(value) {
                        		if(value == "")
                        			return null;
                        		else
                        			return new Date(value).toLocaleDateString('de-DE', {month:'short', year:'numeric'});
                        	},
                        },
                        labels: {
                            
                        },
//                        time: {
//                        	displayFormats: {
//                        		quarter: 'MMM YYYY',
//                        	},
//                        	unitStepSize: 1,
//                        	min: marketexposureDates[0],
//                        	unit: 'month',
//                        },
                    }],
                    yAxes: [{
                        display: true,
                        position: "left",
                        id: "y-axis-1",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            suggestedMin: -50,
                            suggestedMax: 50,
                        	fontFamily: 'Futura Lt BT',
                        	callback: function(value, index, values) {
                            	return (value + 50) + '%';
                            },
                        	fontColor: 'rgba(0,0,0,1)',
                        },
                    },{
                        display: true,
                        position: "right",
                        id: "y-axis-2",
                        scaleLabel: {
                            display: false,
                        },
                        gridLines: {
                        	drawTicks: true,
                        	drawOnChartArea: false,
                        	drawBorder: true,
                        	color: 'rgba(0,0,0,1)',
                        },
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: 100,
                        	fontFamily: 'Futura Lt BT',
                        	fontColor: 'rgba(0,0,0,1)',
                            fontSize: 0,
                        },
                    },]
                },
            }
        };
				
        var ctx = document.getElementById("qelv-marketexposure-chart").getContext("2d");
        window.marketexposureBarChart = new Chart(ctx, config);
}

function fill_month_performance() {
	// create leading months' cells in previous year
	for(var i=0; i<new Date(dateArray[monatsrenditen[0]]).getMonth(); i++){
		document.getElementById("fonds-previous-year").innerHTML += "<td ></td>";
		document.getElementById("index-previous-year").innerHTML += "<td ></td>";
	}
	
	for(var i = 0; i < monatsrenditen.length; i+=3) {							
		var fondValue = monatsrenditen[i+2];
		var fondsCellFontColor = "#000000";
		if(fondValue < 0){
			fondsCellFontColor = "#FF0000"
		}
		
		
		var alphaValue = monatsrenditen[i+1];
		var alphaCellFontColor = "#000000";
		if(alphaValue < 0){
			alphaCellFontColor = "#FF0000"
		}
		rowDate = new Date(dateArray[monatsrenditen[i]]);
		if(rowDate.getFullYear() == currentYear) {
			document.getElementById("fonds-current-year").innerHTML += "<td style='color:"+fondsCellFontColor+"'>"+fondValue.toLocaleString()+"%</td>";
			document.getElementById("index-current-year").innerHTML += "<td style='color:"+alphaCellFontColor+"'>"+alphaValue.toLocaleString()+"%</td>";
		} else {
			document.getElementById("fonds-previous-year").innerHTML += "<td style='color:"+fondsCellFontColor+"'>"+fondValue.toLocaleString()+"%</td>";
			document.getElementById("index-previous-year").innerHTML += "<td style='color:"+alphaCellFontColor+"'>"+alphaValue.toLocaleString()+"%</td>";
		}
		delete rowDate;
	}
	
	// create following months' cells in current year
	for(var i=new Date(dateArray[monatsrenditen[monatsrenditen.length-3]]).getMonth()+1; i<12; i++){
		document.getElementById("fonds-current-year").innerHTML += "<td ></td>";
		document.getElementById("index-current-year").innerHTML += "<td ></td>";
	}
	
	// create YTD values
	var index_ytd_previous_year = (es50_p[endYearIndex] / es50_p[0] - 1) * 100; // es50_p[1]: index "1" needs to be replaced with something like startPYearIndex
	index_ytd_previous_year = Math.round(index_ytd_previous_year * 10) / 10;
	
	var fond_ytd_previous_year = (qelv_p[endYearIndex] / qelv_p[0] - 1) * 100;
	fond_ytd_previous_year = Math.round(fond_ytd_previous_year * 10) / 10;
	
	document.getElementById("fonds-previous-year").innerHTML += "<td >"+fond_ytd_previous_year.toLocaleString()+"%</td>";
	document.getElementById("index-previous-year").innerHTML += "<td >"+(fond_ytd_previous_year - index_ytd_previous_year).toLocaleString()+"%</td>";
	
	var index_ytd_current_year = (es50_p[endIndex] / es50_p[endYearIndex] - 1) * 100; // es50_p[1]: index "1" needs to be replaced with something like startPYearIndex
	index_ytd_current_year = Math.round(index_ytd_current_year * 10) / 10;
	
	var fond_ytd_current_year = (qelv_p[endIndex+1] / qelv_p[endYearIndex+1] - 1) * 100;
	fond_ytd_current_year = Math.round(fond_ytd_current_year * 10) / 10;
	
	document.getElementById("fonds-current-year").innerHTML += "<td >"+fond_ytd_current_year.toLocaleString()+"%</td>";
	document.getElementById("index-current-year").innerHTML += "<td >"+(Math.round((fond_ytd_current_year - index_ytd_current_year) * 10) / 10).toLocaleString()+"%</td>";
}

function init() {
	drawChart_Rendite_Risiko();
	drawChart_Fondsperformance_YTD();
	drawChart_performancedifferenz();
	drawChart_qelv_marketexposure();
	drawChart_Fondsperformance_seit_auflage();
}