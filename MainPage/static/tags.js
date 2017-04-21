var tags = null;
var pointIndex = null;
var speaker = null;
var myPlot = null;
var data = [];
var layout = null;
var graph = null;
var graphB = null;
var bPlot = null;
var layoutB = null;
var emotion = 'Anger';
$.ajax({
  url: '/tags',
  type: 'GET',
  async: false,
  success: function(data) {
    tags = data.tags;
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

    /*
    * Here we begin to set up the bar graph that shows the most common words spoken by everyone in the conversation.
    */
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

    /*
    * This responds to the button on the tag edit pop up and saves their edited data
    */
    $('button#modalSubmit').click(function () {
        var text = $('#modalInput').val();
        tags[emotion][speaker][pointIndex] = text;
        $('#tagModal').modal('hide');
        updateGraph();
    });

    /*
    * Here we begin to set up functionality for the dropdown menu where users can change what emotion they are currently
    * looking at for the conversation.
    */
    $("#drpdwn0").click(function(e){
        emotion = 'Anger';
        updateGraph();
    });

    $("#drpdwn1").click(function(e){
        emotion = 'Anticipation';
        updateGraph();
    });

    $("#drpdwn2").click(function(e){
        emotion = 'Disgust'; 
        updateGraph();
    });

    $("#drpdwn3").click(function(e){
        emotion = 'Fear'; 
        updateGraph();
    });

    $("#drpdwn4").click(function(e){
        emotion = 'Joy'; 
        updateGraph();
    });

    $("#drpdwn5").click(function(e){
        emotion = 'Sadness'; 
        updateGraph();
    });

    $("#drpdwn6").click(function(e){
        emotion = 'Trust'; 
        updateGraph();
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

    /*
    * This code sets up the Inspect Dropdown to look at each speaker's personal profiles.
    */
    var form = $("#personform");
    var people = JSON.parse($("#pInfo").text());
    for (i in people) {
      var element = $(document.createElement('option'));
      element.val(JSON.stringify(people[i])).text(i);
      $("#personform").append(element);
    }
};
