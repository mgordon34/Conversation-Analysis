var tags = null;
var pointIndex = null;
var myPlot = null;
var data = null;
var layout = null;
var graph = null;
$.ajax({
  url: '/tags',
  type: 'GET',
  async: false,
  success: function(data) {
    tags = data.tags;
    console.log(tags);
  }
});

// var myPlot = document.getElementById('graph'),
//   x1 = [1, 2, 3, 4, 5],
//   y1 = [1, 2, 4, 8, 16],
//   outData = [{x: x1, y: y1, text: tags, hoverinfo: 'text'}],
//   layout = {
//     hovermode:'closest',
//     title: 'Results Data'
//   };
window.onload = function() {
    myPlot = document.getElementById('graph');
//    bPlot = document.getElementById('barg')
//    var bData = JSON.parse($("#bInfo"))
    var midData = JSON.parse($("#info").text());
    var mid = [];
    var lines = [];
    for (i in midData.y) {
        mid[i] = midData.y[i];
        lines[i] = midData.name + ': ' + midData.lines[i]
    }
    tags = lines;
    data = [{x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'}];
    //var outData = JSON.parse(data);
    // console.log(outData);
//    var bData = JSON.parse(document.getElementById("bInfo").value);
//    var b2 = []
//    for (i in bData.y) {
//        b2[i] = bData.y[i];
//    }
//    bTags = b2
//    b = [{x: b2.x, y: b2.y,type: 'bar'}];
    layout = {
        "showlegend": true,
        "yaxis": {
            "title": "<b>Trust<\/b>"
        },
        "xaxis": {
            "title": "<b>Line Number<\/b>"
        },
        hovermode: 'closest',
        title: 'Results Data'
    };
    graph = Plotly.newPlot(myPlot, data, layout);
//    graphB = Plotly.newPlot(bPlot, b);

    myPlot.on('plotly_click', function (data) {
        var index = data.points[0].pointNumber;
        pointIndex = index;
        $('#modalInput').val(tags[index]);
        $('#tagModal').modal('show');
    });

    $('button#modalSubmit').click(function () {
        var text = $('#modalInput').val();
        tags[pointIndex] = text;
        $('#tagModal').modal('hide');
        Plotly.redraw(myPlot);
    });
}
