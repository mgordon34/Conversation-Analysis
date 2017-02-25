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
var dat = document.getElementById('info')
console.log(dat)
var outData = JSON.parse(data);
var myPlot = document.getElementById('graph'),
//  data = [{x: x1, y: y1, text: tags, hoverinfo: 'text'}],
  layout = {
    hovermode:'closest',
    title: 'Results Data'
  };
var graph = Plotly.newPlot(myPlot, [outData], layout);
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
