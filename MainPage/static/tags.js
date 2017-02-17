var tags = null;
$.ajax({
  url: '/tags',
  type: 'GET',
  async: false,
  success: function(data) {
    tags = data.tags;
    console.log(tags);
  }
});

var myPlot = document.getElementById('graph'),
  x1 = [1, 2, 3, 4, 5],
  y1 = [1, 2, 4, 8, 16],
  data = [{x: x1, y: y1, text: tags, hoverinfo: 'text'}],
  layout = {
    hovermode:'closest',
    title: 'Results Data'
  };
var graph = Plotly.newPlot(myPlot, data, layout);
var pointIndex;

myPlot.on('plotly_click', function(data) {
  var index = data.points[0].x - 1;
  pointIndex = index;
  $('#modalInput').val(tags[index]);
  $('#tagModal').modal('show');
});

$('button#modalSubmit').click(function(){
  var text = $('#modalInput').val();
  tags[pointIndex] = text;
  $('#tagModal').modal('hide');
  Plotly.redraw(myPlot);
});
