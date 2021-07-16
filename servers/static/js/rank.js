(function(){
//     var years = ['2018','2019','2020','2021'];
// var jdData =[
//     [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它'],
//     [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它'],
//    [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它'],
//    [ '香港同胞','澳门同胞','台湾同胞','日  本','韩  国','蒙  古','印度尼西亚','马来西亚','菲律宾','新加坡','泰  国','印  度','越  南','缅  甸','朝  鲜','巴基斯坦','其  它']]
// var data =[
//     [14.23,1.31,21.13,10873,94964,2966,129748,59827,8519,38344,18495,3531,1369,544,2005,975,33855,],
//     [13.2,1.11,13.6,9284,64138,2237,4779,48877,2371,36224,12956,2499,4778,594,717,534,16487],
//     [15.26,1.31,16.68,10331,91580,1909,40469,67490,1765,36982,15371,3643,2871,762,962,757,34414],
//     [14.23,1.31,21.13,10873,94964,2966,129748,59827,8519,38344,18495,3531,1369,544,2005,975,33855,],
// ];
$.getJSON('/api/city_everypeolple_avg_cost', function(bardata) {
    var years = [];
    var data = [[],[],[]];
    var ydata = [[],[],[]];
    bardata.data.sort(function(a, b) {
        return a.year - b.year;
    });
    for( var key in bardata.data){
        years.push(bardata.data[key].year);
        for( var k in bardata.data[key].prov){
            data[key].push({
                "name": bardata.data[key].prov[k].name,
                "value": bardata.data[key].prov[k].avg_cost,
            });
            ydata[key].push(bardata.data[key].prov[k].name);
        }
    }

    console.log(data);
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
                'trigger': 'axis',
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
                        fontSize:20,
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
                            color:'black',
                            width:3
                        }
                    },
                },
                barWidth:'50%',
                label: {
                    normal: {
                        show: true,
                        position: 'inside',
                        fontSize: '25',
                        formatter: '{c}'
                    }
                },
                itemStyle: {
                    normal: {
                        color: function(params) {
                            // build a color map as your need.
                            var colorList = [
                                '#473C8B', '#436EEE', '#27408B', '#0000EE',
                                '#00008B', '#1C86EE', '#104E8B', '#5CACEE',
                                '#36648B', '#00B2EE', '#87CEFF', '#6CA6CD',
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
        
        // var res = [];
        // for(j=0;j<data[n].length;j++){
        //     res.push({
        //     name: jdData[n][j],
        //     value: data[n][j]
        // });
     
        // }
    
        data[n].sort(function(a, b) {
        return a.value - b.value;
        });
        var res = [];
        //console.log(data[n].slice(0,10));
        res = data[n].slice(0,10);
        var res1=[];
        var res2=[];
        //console.log(res);
        for(t=0;t<res.length;t++){
        res1[t]=res[t].name;
            res2[t]=res[t].value;
        }
        console.log(res1);
        console.log("----------------");
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
    myChart.setOption(option);
});

var myChart = echarts.init(document.querySelector(".map .chart"));

window.addEventListener("resize", function() {
myChart.resize();
});
})();