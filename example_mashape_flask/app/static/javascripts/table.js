String.prototype.format = function () {
  var i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] != 'undefined' ? args[i++] : '';
  });
};

function createTable() {
    //init data
    var json = (function () {
        var json = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': "../static/javascripts/statistics.json",
            'dataType': "json",
            'success': function (data) {
                json = data;
            }
        });
        return json;
    })();
    //end
    var i = 1;
    // FIXME: добавить href и сделать красиво!
    for (var region in json) { // область
        table_row = '<td>'+region+'</td>'
        for (var regionType in json[region]) { // тип город/регион
            table_row_regionType = table_row;
            table_row += '<td>'+regionType+'</td>'
            for (var regionСode in json[region][regionType]) { // код города или обасли
                table_row_regionСode = table_row;
                table_row += '<td>'+regionСode+'</td>'
                for (var customerNumber in json[region][regionType][regionСode]) { //  рег. номер заказчика
                    table_row_customerNumber = table_row;
                    table_row += '<td>'+customerNumber+'</td>'
                    for (var contract in json[region][regionType][regionСode][customerNumber]) { //  контракты заказчика
                        table_row_tmp = table_row
                        table_row_tmp = '<tr><td>'+i+'</td>' +
                            table_row + '<td>'+contract+'</td>'+ '</td><td>' +
                            json[region][regionType][regionСode][customerNumber][contract]["title"] +
                            '</td><td>'+json[region][regionType][regionСode][customerNumber][contract]["budget_level_name"] +
                            '</td><td>'+json[region][regionType][regionСode][customerNumber][contract]["sign_date"] +
                            '</td></tr>'
                        $('#statisticsTable').append(table_row_tmp);
                        i +=1;
                    }
                    table_row = table_row_customerNumber;
                }
                table_row = table_row_regionСode;
            }
            table_row = table_row_regionType;
        }
    }

}
