var tags = null;
var pointIndex = null;
var myPlot = null;
var data = [];
var layout = null;
var graph = null;
var graphB = null;
var bPlot = null;
var layoutB = null;
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
    var midDataArray = JSON.parse($("#Anger").text());
    for (i in midDataArray) {
        var midData = midDataArray[i];
        var mid = [];
        var lines = [];
        for (i in midData.y) {
            mid[i] = midData.y[i];
            lines[i] = midData.name + ': ' + midData.lines[i]
        }
        tags = lines;
        data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
    }
    bPlot = document.getElementById('barg');
    //var bData = JSON.parse($("#bInfo"));
    var midB = JSON.parse($("#bInfo").text());
    console.log(midB);
    layout = {
        "showlegend": true,
        "yaxis": {
            "title": "<b>Anger<\/b>"
        },
        "xaxis": {
            "title": "<b>Line Number<\/b>"
        },
        hovermode: 'closest',
        title: 'Results Data'
    };

    layoutB = {
        "yaxis": {
            "title": "<b>Word Count<\/b>"
        },
        "xaxis": {
            "title": "<b>Most Common Words<\/b>"
        }
    };
    graph = Plotly.newPlot(myPlot, data, layout);
    graphB = Plotly.newPlot(bPlot,[midB], layoutB);

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

    $("#drpdwn0").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Anger").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>Anger<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
        e.preventDefault();
    });

    $("#drpdwn1").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Anticipation").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>Anticipation<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
        e.preventDefault();
    });

    $("#drpdwn2").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Disgust").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>Disgust<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
    });

    $("#drpdwn3").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Fear").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>Fear<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
    });

    $("#drpdwn4").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Joy").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.data = data;
        Plotly.redraw(myPlot);
    });

    $("#drpdwn5").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Sadness").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>Sadness<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
    });

    $("#drpdwn6").click(function(e){
    //console.log($("#info").text());
        var midDataArray = JSON.parse($("#Trust").text());
        data =[];
        for (i in midDataArray) {
            var midData = midDataArray[i];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i]
            }
            tags = lines;
            data.push({x: midData.x, y: midData.y, name: midData.name, text: tags, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>Trust<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
    });

    var form = $("#personform");
    var people = JSON.parse($("#pInfo").text());
    for (i in people) {
      var element = $(document.createElement('option'));
      element.val(JSON.stringify(people[i])).text(i);
      $("#personform").append(element);
      console.log(people[i]);
    }
};
