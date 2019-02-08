Highcharts.chart('chart', {
    chart: {
      type: 'area',
      animation: Highcharts.svg,
      marginRight: 10,
      events: {
        load: function() {
          const request = window.superagent;
                series = this.series[0];
  
          setInterval(function () {
            request
              .get('/sensor')
              .end(function(err, res){
                let x = (new Date()).getTime(),
                    py = res.body.pressure,
                    ty = res.body.temperature;
                
                if (ty < series.yAxis.oldMin | !series.yAxis.oldMin) {
                    series.yAxis.update({min: ty});
                }
                series.addPoint([x, ty], true, true);
              });
          }, 3000);
        } 
      }
    },
    title: {
      text: 'Temprature'
    },
    xAxis: {
      type: 'datetime'
    },
    yAxis: {
      title: {
        text: '度' 
      }
    },
    series: [{
      name: 'Temprature',
      data: (function () {
        let data = [],
            time = (new Date()).getTime(),
            i;
  
        for (i=-99; i<=0; i+=1) {
          data.push({
            x: time + i * 1000,
            y: undefined
          });
        }
        return data;
      }())
    }]
  });
  
