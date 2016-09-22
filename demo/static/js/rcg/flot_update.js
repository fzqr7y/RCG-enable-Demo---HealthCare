            /* updating chart */
            if ($('#updating-chart').length) {

                // For the demo we use generated data, but normally it would be coming from the server
                var data = [], totalPoints = 200;
                function getRandomData() {
                    if (data.length > 0)
                        data = data.slice(1);

                    // do a random walk
                    while (data.length < totalPoints) {
                        var prev = data.length > 0 ? data[data.length - 1] : 50;
                        var y = prev + Math.random() * 10 - 5;
                        if (y < 0)
                            y = 0;
                        if (y > 100)
                            y = 100;
                        data.push(y);
                    }

                    // zip the generated y values with the x values
                    var res = [];
                    for (var i = 0; i < data.length; ++i)
                        res.push([i, data[i]])
                    return res;
                }

                // setup control widget
                var updateInterval = 1000;
                $("#updating-chart").val(updateInterval).change(function() {
                    var v = $(this).val();
                    if (v && !isNaN(+v)) {
                        updateInterval = +v;
                        if (updateInterval < 1)
                            updateInterval = 1;
                        if (updateInterval > 2000)
                            updateInterval = 2000;
                        $(this).val("" + updateInterval);
                    }
                });

                // setup plot
                var options = {
                    yaxis : {
                        min : 0,
                        max : 100
                    },
                    xaxis : {
                        min : 0,
                        max : 100
                    },
                    colors : [$chrt_fourth],
                    series : {
                        lines : {
                            lineWidth : 1,
                            fill : true,
                            fillColor : {
                                colors : [{
                                    opacity : 0.4
                                }, {
                                    opacity : 0
                                }]
                            },
                            steps : false

                        }
                    }
                };
                var plot = $.plot($("#updating-chart"), [getRandomData()], options);

                /* live switch */
                $('input[type="checkbox"]#start_interval').click(function() {
                    if ($(this).prop('checked')) {
                        $on = true;
                        updateInterval = 1500;
                        update();
                    } else {
                        clearInterval(updateInterval);
                        $on = false;
                    }
                });

                function update() {
                    if ($on == true) {
                        plot.setData([getRandomData()]);
                        plot.draw();
                        setTimeout(update, updateInterval);

                    } else {
                        clearInterval(updateInterval)
                    }
                }
                var $on = false;
            }
            /*end updating chart*/

