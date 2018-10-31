function paintGraphPieFaultTypes(data) {
    var graphPieFaultTypes = Highcharts.chart('graphPieFaultTypes', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
		title: {
			text: ''
		},
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    connectorColor: 'silver'
                }
            }
        },
        series: [{
            name: 'Share',
            data: data 
        }]
    });
}

function paintGraphPieDeviceTypes(data) {
    var graphPieDeviceTypes = Highcharts.chart('graphPieDeviceTypes', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
		title: {
			text: ''
		},
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    connectorColor: 'silver'
                }
            }
        },
        series: [{
            name: 'Share',
            data: data 
        }]
    });
}

function paintGraphBarFaultTypesPerDevice(data) {
	var graphBarFaultTypesPerDevice = Highcharts.chart('graphBarFaultTypesPerDevice', {
		chart: {
			type: 'bar'
		},
		title: {
			text: ''
		},
		xAxis: {
			categories: data.categories
		},
		yAxis: {
			title: {
				text: 'Faults'
			}
		},
		series: data.series
	});
}



function paintGraphLineUrlFaults(data) {
    var graphLineUrlFaults = Highcharts.chart('graphLineUrlFaults', {
        
        chart: {
            type: 'line'
        },
		title: {
			text: ''
		},
        xAxis: {
            categories: data.categories
        },
        yAxis: {
            title: {
                text: 'Number of Faults'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
    
        plotOptions: {
            line: {
                animation: false,
                dataLabels: {
                    enabled: true
                }
            }
        },
    
        series: data.series,
    
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }
    
    });
}