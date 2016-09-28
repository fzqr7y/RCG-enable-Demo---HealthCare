            /* updating chart */
            if ($('#updating-chart').length) {

                var initialRun = true;
                var $on = false;
                var ajaxComplete = false;
                var updateInterval = 1000;
                var plotDuration = 1800 * updateInterval; // total time shown
                var queryOffset = 300 * updateInterval;   // offset from current time
                var dataOffset = 600 * updateInterval;     // start data this far back from query
                // var plotDuration = 180 * updateInterval; // total time shown
                // var queryOffset = 60 * updateInterval;   // offset from current time
                // var dataOffset = 10 * updateInterval;     // start data this far back from query
                // var member_id = {{ member.id }};
                var member_id = $member_id;

                var plotMax, plotMin;
                var queryMax, queryMin, dataMax;
                var plotData = [];
                var queryData = [];
                var plotOptions;
                var plot;

                var randomAdditive = 0;
                var randomAdditive2 = 0;
                var randomMax = 10;
                var randomMin = -5;
                var randomMax2 = 5;
                var randomMin2 = -1;

                // setup plot
                function getOptions() {
                    var options = {
                        yaxis : {
                            min : 50, max : 100
                        },
                        xaxis: {
                            min: plotMin, max: plotMax,
                            mode: "time", timezone: "browser"
                        },
                        colors : [$chrt_fourth],
                        series : {
                            lines : {
                                lineWidth : 1,
                                fill : true,
                                fillColor : {
                                    colors : [{
                                        opacity : 0.4 }, { opacity : 0 }]
                                },
                                steps : false
                            }
                        }
                    };
                    return options;
                };

var queryCount = 0;

                function getFitbitData() {
                    // var jdata = []
                    var t, val, qmin;
                    var rndval, nv, rndval2;
                    qdatamax = (queryData.length>0) ? queryData[queryData.length-1][0] : queryMin;
// console.log(qdatamax)
                    queryCount++;
// console.log(queryCount);
                    if (queryCount > 10) {
                        ajaxComplete = true;
                    }
                    $.getJSON("/cloudera/heartrate/get", {
                            member_id: member_id,
                            // from: (new Date(queryMin)).toISOString(),
                            from: (new Date(qdatamax)).toISOString(),
                            to: (new Date(queryMax)).toISOString() },
                        function(json){
console.log("qdatamax: " + qdatamax + " from: " + (new Date(queryMin)).toISOString() + " to: " + (new Date(queryMax)).toISOString());
                            $.each(json, function (index, value) {
// console.log(value)
                                t = (new Date(value[0])).getTime();
                                val = value[1];
// console.log("qdatamax: " + qdatamax + " t: " + t + " val: " + val);
                                // jdata.push([t, val]);
                                rndval = Math.random() * 0.8 - 0.4;
                                if (randomAdditive > randomMax && rndval > 0)
                                    rndval = -rndval;
                                if (randomAdditive < randomMin && rndval < 0)
                                    rndval = -rndval;
                                rndval2 = Math.random() * 0.4 - 0.2;
                                if (randomAdditive2 > randomMax2 && rndval > 0)
                                    rndval2 = 0;
                                if (randomAdditive2 < randomMin2 && rndval < 0)
                                    rndval2 = 0;
                                randomAdditive += rndval;
                                randomAdditive2 += rndval2;
                                // if (valadd < -10)
                                //     valadd = -10;
                                // if (valadd > 100)
                                //     valadd = 100;
                                // nv = val + Math.round(randomAdditive) + Math.round(randomAdditive2)
                                nv = val + Math.round(randomAdditive) + Math.round(randomAdditive2)
// console.log(" val: " + val + " randomAdditive: " + randomAdditive + " randomAdditive2: " + randomAdditive2 + " new: " + nv);
                                val = nv;

                                if (t > qdatamax) {
                                    queryData.push([t, val]);
                                }
                            });
                            // queryData = jdata;
                            ajaxComplete = true;
                            queryCount = 0;
                            // console.log("queryMin: " + (new Date(queryMin)).toLocaleTimeString() + " queryMax: " + (new Date(queryMax)).toLocaleTimeString() + " queryData.length: " + queryData.length);
                            // console.log("queryData: queryData.length: " + queryData.length + " queryDataMin: " + (new Date(queryData[0][0])).toLocaleTimeString() + " queryDataMax: " + (new Date(queryData[queryData.length-1][0])).toLocaleTimeString());
                            // console.log("queryData: queryData.length: " + queryData.length + " queryDataMin: " + queryData[0][0] + " queryDataMax: " + queryData[queryData.length-1][0]);
                            // if (plotData.length > 0) {
                                // console.log("plotData: plotData.length: " + plotData.length + " plotDataMin: " + plotData[0][0] + " plotDataMax: " + plotData[plotData.length-1][0]);
                            // }
                    // console.log("p: " + plotData);
                    // console.log("q: " + queryData);
                            $('.heartrate-status').html('');
                    });
                    // asynchronous call so no data at this point
                    return;
                };

                function setupChart() {
                    // update the query max time
                    plotMax = (new Date($.now())).getTime();
                    plotMin = plotMax - plotDuration;
                    queryMax = plotMax - queryOffset;
                    queryMin = (plotData.length > 0) ? plotData[plotData.length - 1][0] : plotMin;
                    dataMax = queryMax - dataOffset;

                    plotOptions = getOptions();
                    // console.log("axis: " + plotOptions.xaxis.min + " " + plotOptions.xaxis.max);
                    // console.log("axis: " + (new Date(plotOptions.xaxis.min)).toLocaleTimeString() + " " + (new Date(plotOptions.xaxis.max)).toLocaleTimeString());
                    plot = $.plot($("#updating-chart"), [plotData], plotOptions);
                    plot.draw();
                    return;
                }

                function getPlotData() {
                    // var maxp = 0;
                    // if (plotData.length > 0) {
                    //  maxp = plotData[plotData.length-1][0]
                    //  console.log("maxp: " + maxp)
                    // }
                    // while (queryData.length > 0 && queryData[0][0] <= maxp) {
                    //  console.log("q: " + queryData[0][0])
                    //  queryData = queryData.slice(1);
                    // }
                    while (queryData.length > 0 && queryData[0][0] < dataMax) {
                        plotData.push(queryData[0])
                        queryData = queryData.slice(1);
                    }
                    if (queryData.length > 0) {
                        // console.log("plotData: " + plotData.length + " " + queryData.length + " dataMax: " + dataMax + " queryData[0][0]: " + queryData[0][0]);
                    }
                    // if (plotData.length > 0) {
                    //  console.log("Query plotData: plotData.length: " + plotData.length + " plotDataMin: " + (new Date(plotData[0][0])).toLocaleTimeString() + " plotDataMax: " + (new Date(plotData[plotData.length-1][0])).toLocaleTimeString());
                    // }
                    while (plotData.length > 0 && plotData[0][0] < plotMin - updateInterval) {
                        plotData = plotData.slice(1);
                    }
                    // console.log(plotData);
           //          if (plotData.length > 0) {
                    //  console.log("PlotData: plotData.length: " + plotData.length + " plotDataMax: " + (new Date(plotData[0][0])).toLocaleTimeString() + " plotDataMax: " + (new Date(plotData[plotData.length-1][0])).toLocaleTimeString());
                    // }
                    if (queryData.length <= 4) {
                        // console.log("requerying fitbit");
                        $('.heartrate-status').html('Querying FitBit');
                        setupChart();
                        getFitbitData();
                    }
                }

                /* live switch */
                $('input[type="checkbox"]#start_interval').click(function() {
                    if ($(this).prop('checked')) {
                        $on = true;
                        // plotData = [];
                        queryData = [];
                        update();
                    } else {
                        clearInterval(updateInterval);
                        $on = false;
                    }
                });

                // var updateCount = 0;
                function update() {
                    // updateCount++;
                    // console.log("update start: " + updateCount);
                    if ($on == true) {
                        dataMax += updateInterval;
                        getPlotData();
                        plot.setData([plotData]);
                        // console.log("update plotted: " + plotData.length + " " + initialRun + " " + ajaxComplete)
                        // console.log("up axis: " + (new Date(plotOptions.xaxis.min)).toLocaleTimeString() + " " + (new Date(plotOptions.xaxis.max)).toLocaleTimeString());
                        // if (plotData.length > 0) {
                        //  console.log("Update: plotData.length: " + plotData.length + " queryData.length: " + queryData.length + " plotDataMin: " + (new Date(plotData[0][0])).toLocaleTimeString() + " plotDataMax: " + (new Date(plotData[plotData.length-1][0])).toLocaleTimeString());
                        // }
                        if (plotData.length > 0 && initialRun) {
                            $on = false;
                            initialRun = false;
                        }
                        if (plotData.length == 0 && ajaxComplete) {
                            $on = false;
                            console.log("Query returned no data. user_id:" + member_id + " from: " + (new Date(queryMin)).toLocaleTimeString() + " to: " + (new Date(queryMax)).toLocaleTimeString());
                            alert("Query returned no data. user_id:" + member_id + " from: " + (new Date(queryMin)).toLocaleTimeString() + " to: " + (new Date(queryMax)).toLocaleTimeString());
                            $('.heartrate-status').html('');
                        }
                        plot.draw();
                        setTimeout(update, updateInterval);
                    } else {
                        clearInterval(updateInterval)
                    }
                }

                if (initialRun) {
                    $on = true
                    update();
                }
            }
            /*end updating chart*/
