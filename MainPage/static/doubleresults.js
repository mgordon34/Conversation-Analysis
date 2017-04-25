/**
 * Created by elizabethdudley on 4/21/17.
 */
var tags = null;
var tags1 = null;
var pointIndex = null;
var speaker = null;
var myPlot = null;
var data = [];
var data1 = [];
var data2 = [];
var layout = null;
var graph = null;
var graph1 = null;
var emotion = 'Anger';
$.ajax({
  url: '/tags',
  type: 'GET',
  async: false,
  success: function(data) {
    tags = data.tags;
    tags1 = data.tags;
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
    /*
    * This sets up the Emotion Graph for EVERYONE in the conversation. It also sets up the editable tag array, so the
    * user can edit each individual point in the graph.
    */
    myPlot = document.getElementById('graph');
    var midDataArray = JSON.parse($("#Anger").text());
    for (j in midDataArray) {
        var midData = midDataArray[j];
        var mid = [];
        var lines = [];
        for (i in tags) {
          tags[i][j] = {}
        }
        tags['Anger'][j] = {};
        for (i in midData.y) {
            mid[i] = midData.y[i];
            lines[i] = midData.name + ': ' + midData.lines[i]
            if (typeof tags['Anger'][j][i] != 'undefined') {
              lines[i] += '<br>' + 'tag: ' + tags[emotion][j][i];
            }
        }
        data.push({x: midData.x, y: midData.y, name: midData.name, text: lines, hoverinfo: 'text', type: 'scatter'});
    }

    layout = {
        "showlegend": true,
        "yaxis": {
            "title": "<b>Anger<\/b>"
        },
        "xaxis": {
            "title": "<b>Line Number<\/b>"
        },
        hovermode: 'closest',
        title: 'Conversation One'
    };

    myPlot1 = document.getElementById('graph1');


    graph = Plotly.newPlot(myPlot, data, layout);

    var midDataArray1 = JSON.parse($("#Anger1").text());
    for (j in midDataArray1) {
        var midData1 = midDataArray1[j];
        var mid1 = [];
        var lines1 = [];
        for (i in tags1) {
          tags1[i][j] = {}
        }
        tags1['Anger'][j] = {};
        for (i in midData1.y) {
            mid1[i] = midData1.y[i];
            lines1[i] = midData1.name + ': ' + midData1.lines[i]
            if (typeof tags1['Anger'][j][i] != 'undefined') {
              lines1[i] += '<br>' + 'tag: ' + tags1[emotion][j][i];
            }
        }
        data1.push({x: midData1.x, y: midData1.y, name: midData1.name, text: lines1, hoverinfo: 'text', type: 'scatter'});
    }

    layout1 = {
        "showlegend": true,
        "yaxis": {
            "title": "<b>Anger<\/b>"
        },
        "xaxis": {
            "title": "<b>Line Number<\/b>"
        },
        hovermode: 'closest',
        title: 'Conversation Two'
    };

    graph1 = Plotly.newPlot(myPlot1, data1, layout1);

    var compPlot = document.getElementById('compoundGraph');

    var line1 = JSON.parse($("#compound").text());
    line1.name = "Conversation 1";
    var line2 = JSON.parse($("#compound1").text());
    line2.name = "Conversation 2";
    data2 = [line1, line2];
    console.log(data2);

    var layout2 = {
        "showlegend": true,
        "yaxis": {
            "title": "<b>Anger<\/b>"
        },
        "xaxis": {
            "title": "<b>Line Number<\/b>"
        },
        hovermode: 'closest',
        title: 'Compound Scores of Both Conversations'
    };

    var compGraph = Plotly.newPlot(compPlot, data2, layout2);


    /*
    * This function responds to when the user clicks on a point on the graph, and saves their edited data.
    */
    myPlot.on('plotly_click', function (data) {
        var index = data.points[0].pointNumber;
        speaker = data.points[0].curveNumber;
        pointIndex = index;
        $('#modalInput').val(tags[emotion][speaker][index]);
        $('#tagModal').modal('show');
    });

    myPlot1.on('plotly_click', function (data) {
        var index = data.points[0].pointNumber;
        speaker = data.points[0].curveNumber;
        pointIndex = index;
        $('#modalInput').val(tags1[emotion][speaker][index]);
        $('#tagModal1').modal('show');
    });

    /*
    * This responds to the button on the tag edit pop up and saves their edited data
    */
    $('button#modalSubmit').click(function () {
        var text = $('#modalInput').val();
        tags[emotion][speaker][pointIndex] = text;
        $('#tagModal').modal('hide');
        updateGraph();
    });

    $('button#modalSubmit1').click(function () {
        var text = $('#modalInput').val();
        tags1[emotion][speaker][pointIndex] = text;
        $('#tagModal1').modal('hide');
        updateGraph1();
    });

    /*
    * Here we begin to set up functionality for the dropdown menu where users can change what emotion they are currently
    * looking at for the conversation.
    */
    $("#drpdwn0").click(function(e){
        emotion = 'Anger';
        updateGraph();
        updateGraph1();
    });

    $("#drpdwn1").click(function(e){
        emotion = 'Anticipation';
        updateGraph();
        updateGraph1();
    });

    $("#drpdwn2").click(function(e){
        emotion = 'Disgust';
        updateGraph();
        updateGraph1();
    });

    $("#drpdwn3").click(function(e){
        emotion = 'Fear';
        updateGraph();
        updateGraph1();
    });

    $("#drpdwn4").click(function(e){
        emotion = 'Joy';
        updateGraph();
        updateGraph1();
    });

    $("#drpdwn5").click(function(e){
        emotion = 'Sadness';
        updateGraph();
        updateGraph1();
    });

    $("#drpdwn6").click(function(e){
        emotion = 'Trust';
        updateGraph();
        updateGraph1();
    });

    /*
    * The update graph method swaps the data out from the previous emotion for the new emotion the user selected and
    * refreshes the graph.
    */
    function updateGraph() {
        var midDataArray = JSON.parse($("#" + emotion).text());
        data =[];
        for (j in midDataArray) {
            var midData = midDataArray[j];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i];
                if (typeof tags[emotion][j][i] != 'undefined') {
                  lines[i] += '<br>' + 'tag: ' + tags[emotion][j][i];
                }
            }
            data.push({x: midData.x, y: midData.y, name: midData.name, text: lines, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot.layout.yaxis.title = "<b>" + emotion + "<\/b>";
        myPlot.data = data;
        Plotly.redraw(myPlot);
    };

    function updateGraph1() {
        var midDataArray = JSON.parse($("#" + emotion + "1").text());
        data1 =[];
        for (j in midDataArray) {
            var midData = midDataArray[j];
            var mid = [];
            var lines = [];
            for (i in midData.y) {
                mid[i] = midData.y[i];
                lines[i] = midData.name + ': ' + midData.lines[i];
                if (typeof tags1[emotion][j][i] != 'undefined') {
                  lines[i] += '<br>' + 'tag: ' + tags1[emotion][j][i];
                }
            }
            data1.push({x: midData.x, y: midData.y, name: midData.name, text: lines, hoverinfo: 'text', type: 'scatter'});
        }
        myPlot1.layout.yaxis.title = "<b>" + emotion + "<\/b>";
        myPlot1.data = data1;
        Plotly.redraw(myPlot1);
    }
};
