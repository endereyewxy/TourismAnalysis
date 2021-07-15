(function(){
    var mapName = 'china'

    var geoCoordMap = {
    };
    var year = ["2019", "2020", "2021"];  
    var mapData = [
        [],
        [],
        [],
       ];

    /*获取地图数据*/
    var myChart = echarts.init(document.querySelector(".map .chart"));
    myChart.showLoading();
    var mapFeatures = echarts.getMap(mapName).geoJson.features;
    myChart.hideLoading();
    mapFeatures.forEach(function(v) {
        // 地区名称
        var name = v.properties.name;
        // 地区经纬度
        geoCoordMap[name] = v.properties.cp;
    
    });
 
    for (var key in geoCoordMap) {
        mapData[0].push({
            "year": '2019',
            "name": key,
            "value": randomNum(0, 200)
        });
        mapData[1].push({
            "year": '2020',
            "name": key,
            "value": randomNum(0, 200)
        });
        mapData[2].push({
            "year": '2021',
            "name": key,
            "value": randomNum(0, 200)
        });
    }

    //console.log(data)
    var max = 480,
        min = 9; // todo 
    var maxSize4Pin = 100,
        minSize4Pin = 20;

   
    var convertData = function(data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
            var geoCoord = geoCoordMap[data[i].name];
            if (geoCoord) {
                res.push({
                    name: data[i].name,
                    value: geoCoord.concat(data[i].value),
                });
            }
        }
        return res;
    };
    optionXyMap01 = {
        timeline: {
            data: year,
            axisType: 'category',   //离散数据
            autoPlay: false,    //自动播放
            playInterval: 3000,
            left: '10%',
            right: '10%',
            top: '1%',
            width: '80%',
            realtime: true,
            controlPosition: "right",
            //  height: null,
            label: {
                normal: {
                    textStyle: {
                        color: '#ddd'
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
                color: '#467bc0'
            },
            checkpointStyle: {
                borderColor: 'rgb(123,123,132)',
                color:'#04387b',
                borderWidth: 2
            },
            controlStyle: {
                showNextBtn: true,
                showPrevBtn: true,
                normal: {
                    color: '#04387b',
                    borderColor: '#04387b'
                },
                emphasis: {
                    color: '#04387b',
                    borderColor: '#04387b'
                }
            },
        },
      // 鼠标放置显示小窗
        baseOption: {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
            },
             
              //侧边
              visualMap: {
                  show: true,
                  min: 0,
                  max: 200,
                  left: '10%',
                  top: 'bottom',
                  calculable: true,
                  textStyle: {
                    color: '#24CFF4'
                },
                  seriesIndex: [1],
                  inRange: {
                      color: ['#04387b', '#467bc0'] // 蓝绿
                  }
              },
              geo: {
                  show: true,
                  map: mapName,
                  label: {
                      normal: {
                          show: false
                      },
                      emphasis: {
                          show: false,
                      }
                  },
                  roam: false,
                  itemStyle: {
                      normal: {
                          areaColor: '#023677',
                          borderColor: '#1180c7',
                      },
                      emphasis: {
                          areaColor: '#4499d0',
                      }
                  }
              },
        },
        options:[]
    };
    for(var n = 0; n < year.length; n++){
        console.log(mapData[n]);
        optionXyMap01.options.push({
            series: [{
                name: '散点',
                type: 'scatter',
                coordinateSystem: 'geo',
                data: convertData(mapData[n]),
                symbolSize: function(val) {
                    return val[2] / 10;
                },
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'right',
                        show: true
                    },
                    emphasis: {
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#fff'
                    }
                }
            },
            {
                type: 'map',
                map: mapName,
                geoIndex: 0,
                aspectScale: 0.75, //长宽比
                showLegendSymbol: false, // 存在legend时显示
                label: {
                    normal: {
                        show: true
                    },
                    emphasis: {
                        show: false,
                        textStyle: {
                            color: '#fff'
                        }
                    }
                },
                roam: true,
                itemStyle: {
                    normal: {
                        areaColor: '#031525',
                        borderColor: '#3B5077',
                    },
                    emphasis: {
                        areaColor: '#2B91B7'
                    }
                },
                animation: false,
                data: mapData[n]
            },
            {
                name: '点',
                type: 'scatter',
                coordinateSystem: 'geo',
                zlevel: 6,
            },
            {
                name: 'Top 5',
                type: 'effectScatter',
                coordinateSystem: 'geo',
                data: convertData(mapData[n].sort(function(a, b) {
                    return b.value - a.value;
                }).slice(0, 5)),
                symbolSize: function(val) {
                    return val[2] / 10;
                },
                showEffectOn: 'render',
                rippleEffect: {
                    brushType: 'stroke'
                },
                hoverAnimation: true,
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'left',
                        show: false
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'yellow',
                        shadowBlur: 10,
                        shadowColor: 'yellow'
                    }
                },
                zlevel: 1
            },
        ]
        })
    }
    myChart.setOption(optionXyMap01);
    window.addEventListener("resize", function() {
    myChart.resize();
    });
  })();

function randomNum(minNum, maxNum) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * minNum + 1, 10);
            break;
        case 2:
            return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
            break;
        default:
            return 0;
            break;
    }
}