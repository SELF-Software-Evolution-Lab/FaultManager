function paintGraphPieFaultTypes(data) {
    var graphPieFaultTypes = Highcharts.chart('graphPieFaultTypes', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Fault Types'
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
            data: JSON.parse(data) 
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
            text: 'Device Types with Faults'
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
            data: JSON.parse(data) 
        }]
    });
}

function paintGraphBarFaultTypesPerDevice(data) {
    var dataGrap = JSON.parse(data) 
	var graphBarFaultTypesPerDevice = Highcharts.chart('graphBarFaultTypesPerDevice', {
		chart: {
			type: 'bar'
		},
		title: {
			text: 'Fault Types Per Device'
		},
		xAxis: {
			categories: dataGrap.categories
		},
		yAxis: {
			title: {
				text: 'Faults'
			}
		},
		series: dataGrap.series
	});
}



function paintGraphLineDeviceFaults(data) {
    var dataGrap = JSON.parse(data) 
    var graphLineDeviceFaults = Highcharts.chart('graphLineDeviceFaults', {
        
        chart: {
            type: 'line'
        },

        title: {
            text: 'Device Faults'
        },
    
        xAxis: {
                categories: dataGrap.categories
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
                dataLabels: {
                    enabled: true
                }
            }
        },
    
        series: dataGrap.series,
    
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

