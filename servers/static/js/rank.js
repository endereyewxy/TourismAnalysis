(function(){
    var years = ['2018','2019','2020','2021'];
var jdData =[
    [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它'],
    [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它'],
   [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它'],
   [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它']]
var data =[
    [14.23,1.31,21.13,10873,94964,2966,129748,59827,8519,38344,18495,3531,1369,544,2005,975,33855,],
    [13.2,1.11,13.6,9284,64138,2237,4779,48877,2371,36224,12956,2499,4778,594,717,534,16487],
    [15.26,1.31,16.68,10331,91580,1909,40469,67490,1765,36982,15371,3643,2871,762,962,757,34414],
    [14.23,1.31,21.13,10873,94964,2966,129748,59827,8519,38344,18495,3531,1369,544,2005,975,33855,],
];
$.getJSON('/api/month_and_people?year1=2019&year2=2020', function(linedata) {

});
option = {
          
    baseOption: {
         timeline: {
        data: years,
        axisType: 'category',
        autoPlay: true,
        playInterval: 2000,
        left: '10%',
        right: '10%',
        bottom: '0%',
        width: '80%',
        //  height: null,
        label: {
            normal: {
                textStyle: {
                    
                    color: '#fff',
                }
            },
            emphasis: {
                textStyle: {
                    color: '#fff'
                }
            }
        },
        symbolSize: 10,
        lineStyle: {
            color: '#6699CC'
        },
        checkpointStyle: {
            borderColor: '#6699CC',
            borderWidth: 2
        },
        controlStyle: {
            showNextBtn: true,
            showPrevBtn: true,
            normal: {
                color: '#6699CC',
                borderColor: '#6699CC'
            },
            emphasis: {
                color: '#CCFFFF',
                borderColor: '#CCFFFF'
            }
        },

    },
        title: {
            text: '',
            right: '2%',
            bottom: '12%',
            textStyle: {
                fontSize: 50,
                color: '#CCFFFF'
            }
        },
        tooltip: {
            'trigger': 'axis'
        },
        calculable: true,
        grid: {
            left: '8%',
            right: '2%',
            bottom: '10%',
            top:'0%',
            containLabel: true
        },
        label:{
            normal:{
                textStyle:{
                    color:'#CCFFFF'
                }
            }
        },
        yAxis: [{
              offset: '37',
            'type': 'category',
            data: '',
            nameTextStyle:{
                color:'#CCFFFF'
            },
            axisLabel:{
                //rotate:45,
                textStyle:{
                    fontSize:12,
                    color:'#CCFFFF',
                },
                interval: 0
            },
            axisLine:{

                lineStyle:{
                    color:'#336699'
                },
            },
            splitLine:{
                show:false,
                lineStyle:{
                    color:'#336699'
                }
            },

        }],
        xAxis: [{
            'type': 'value',
            'name': '',
           
            splitNumber:8,
            nameTextStyle:{
                color:'#336699'
            },
            axisLine:{
                lineStyle:{
                    color:'#336699'
                }
            },
            axisLabel: {
                formatter: '{value} '
            },
            splitLine:{
                show:true,
                lineStyle:{
                    color:'#336699'
                }
            },
        }],
        series: [{
            'name': '',
            'type': 'bar',
            markLine : {
                label:{
                    normal:{
                        show:false
                    }
                },
                lineStyle:{
                    normal:{
                        color:'red',
                        width:3
                    }
                },
            },
            barWidth:'50%',
            label: {
                normal: {
                    show: true,
                    position: 'inside',
                    formatter: '{c}'
                }
            },
            itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                            '#bcd3bb', '#e88f70', '#9dc5c8', '#e1e8c8',
                            '#7b7c68', '#e5b5b5', '#f0b489', '#928ea8',
                            '#bda29a', '#376956', '#c3bed4', '#495a80',
                            '#9966cc', '#bdb76a', '#eee8ab', '#a35015',
                            '#04dd98', '#d9b3e6', '#b6c3fc','#315dbc',
                        ];
                        return colorList[params.dataIndex]
                    },

                }
            },
        }],
        animationDurationUpdate: 2000,
        animationEasingUpdate: 'quinticInOut'
    },
    options: []
};
for (var n = 0; n < years.length; n++) {
    
           var res = [];
//alert(jdData.length);
   for(j=0;j<data[n].length;j++){
        res.push({
        name: jdData[n][j],
        value: data[n][j]
    });
 
}

res.sort(function(a, b) {
return b.value - a.value;
}).slice(0, 6);

res.sort(function(a, b) {
return a.value - b.value;
});
var res1=[];
var res2=[];
//console.log(res);
for(t=0;t<res.length;t++){
  res1[t]=res[t].name;
    res2[t]=res[t].value;
}
console.log(res1);
  console.log(jdData[n]);
    option.options.push({
        title: {
            text: years[n] +'年'
        },
        yAxis:{
            data:res1,
        },
        series: [{
            data: res2
        }]
    });
}
var myChart = echarts.init(document.querySelector(".map .chart"));
myChart.setOption(option);
window.addEventListener("resize", function() {
myChart.resize();
});
})();