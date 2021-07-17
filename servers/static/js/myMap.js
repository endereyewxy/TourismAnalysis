(function () {
    var mapName = 'china';

    var geoCoordMap = {};

    /*获取地图数据*/
    var myChart = echarts.init(document.querySelector(".map .chart"));
    myChart.showLoading();
    var mapFeatures = echarts.getMap(mapName).geoJson.features;
    myChart.hideLoading();
    mapFeatures.forEach(function (v) {
        // 地区名称
        var name = v.properties.name;
        // 地区经纬度
        geoCoordMap[name] = v.properties.cp;

    });

    // for (var key in geoCoordMap) {
    //     console.log(key);
    //     mapData[0].push({
    //         "year": '2019',
    //         "name": key,
    //         "value": randomNum(0, 200)
    //     });
    //     mapData[1].push({
    //         "year": '2020',
    //         "name": key,
    //         "value": randomNum(0, 200)
    //     });
    //     mapData[2].push({
    //         "year": '2021',
    //         "name": key,
    //         "value": randomNum(0, 200)
    //     });
    // }

    $.getJSON('/api/prov_hot', function (scatterdata) {
        var year = ["2019", "2020", "2021"];
        var mapData = [
            [],
            [],
            [],
        ];
        for (var key in geoCoordMap) {
            for (var pn in scatterdata.data[0].prov) {
                if (key == scatterdata.data[0].prov[pn].name) {
                    mapData[0].push({
                        "year": '2019',
                        "name": key,
                        "value": scatterdata.data[0].prov[pn].hot
                    });
                }
            }
            for (var pn in scatterdata.data[1].prov) {
                if (key == scatterdata.data[1].prov[pn].name) {
                    mapData[1].push({
                        "year": '2020',
                        "name": key,
                        "value": scatterdata.data[1].prov[pn].hot
                    });
                }
            }
            for (var pn in scatterdata.data[2].prov) {
                if (key == scatterdata.data[2].prov[pn].name) {
                    mapData[2].push({
                        "year": '2021',
                        "name": key,
                        "value": scatterdata.data[2].prov[pn].hot
                    });
                }
            }
        }
        console.log(mapData);
        var convertData = function (data) {
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
                    color: '#04387b',
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
                    "trigger": "item",
                    "confine": true,
                    "formatter": (p) => {
                        // console.log(JSON.stringify(p));
                        let dataCon = p.data,
                            txtCon = `${dataCon.name}</br>热度：${dataCon.value}`
                        return txtCon

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
            options: []
        };
        for (var n = 0; n < year.length; n++) {
            console.log(mapData[n]);
            optionXyMap01.options.push({
                visualMap: {
                    show: true,
                    min: 0,
                    max: scatterdata.data[n].max,
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
                series: [
                    {
                        name: '散点',
                        type: 'scatter',
                        coordinateSystem: 'geo',
                        data: convertData(mapData[n]),
                        symbolSize: function (n) {
                            return function (val) {
                                console.log(n);
                                return val[2] / scatterdata.data[n].max * 30;
                            }
                        }(n),
                        // label: {
                        //     normal: {
                        //         formatter: '{b}',
                        //         position: 'right',
                        //         show: true
                        //     },
                        //     emphasis: {
                        //         show: true
                        //     }
                        // },
                        itemStyle: {
                            normal: {
                                color: '#fff',
                                opacity: 0,
                            },

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
                        data: convertData(mapData[n].sort(function (a, b) {
                            return b.value - a.value;
                        }).slice(0, 5)),
                        symbolSize: function (n) {
                            return function (val) {
                                console.log(n);
                                return val[2] / scatterdata.data[n].max * 20;
                            }
                        }(n),
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
    });

    window.addEventListener("resize", function () {
        myChart.resize();
    });
    myChart.on('click', function (data) {
        if (data.hasOwnProperty('name')) {
            window.location.href = '/hot.html?prov=' + data.name;
        }
    });
})();
