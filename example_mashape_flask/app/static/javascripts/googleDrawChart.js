function drawVisualization(json) {
    // Create and populate the data table.
//    var data = new google.visualization.arrayToDataTable();
    var tableData = [];
    tableData.push(['Месяц', 'Единственный поставщик', 'Открытый аукцион', 'Открытый конкурс','Открытый аукцион в электронной форме', 'Результаты рассмотрения и оценки котировочных заявок', 'Запрос котировок' ]);
    jQuery.each(json, function() {
        console.log(json);
    });

    jQuery.each(json, function () {
        var tmpData = [];
        for (var i = 1; i <= 12; i++) {
            tmpData.push(i)
            for (var j = 1; j <= 6; j++) {
                try {
                    if (this[j][i] != undefined) {
                        tmpData.push(this[j][i]);
                    }
                    else tmpData.push(0);
                } catch (e) {
                    tmpData.push(0);
                }
            }
            tableData.push(tmpData)
            var tmpData = [];
        }
    });
    var data = google.visualization.arrayToDataTable(tableData);
//  var data = google.visualization.arrayToDataTable([
//    ['Месяц', '1', '2', '3', '4', '5' , '6'], месяц и тип
//    ['1', 1336060, 400361, 1001582, 997974, 997974, 997974 ],
//    ['2', 1336060, 400361,           1001582,         997974,            997974,           997974          ],
//    ['3',      1336060,           400361,           1001582,         997974,            997974,           997974          ],
//    ['4',      1336060,           400361,           1001582,         997974,            997974,           997974          ],
//    ['5',      1336060,           400361,           1001582,         997974,            997974,           997974          ],
//
//  ]);

    // Create and draw the visualization.
    new google.visualization.BarChart(document.getElementById('visualization')).
        draw(data,
        {title: "Сумма бюджета по категориям",
            width: 900, height: 900,
            vAxis: {title: "Месяц", minValue:1 ,maxValue: 12 ,gridlines:{count:12}},
            hAxis: {title: "Средства, рубли"}}
    );
}