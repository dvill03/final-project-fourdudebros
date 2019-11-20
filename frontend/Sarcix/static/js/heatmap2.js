events = []
coverages = []

function unique(value, index, self) { 
    return self.indexOf(value) === index;
}

d3.json('/get_runs', function(data) {
  data.forEach(function(d){
      events.push(d.event_name)
      coverages.push(d.coverage_name)
      d.score = +d.score;
  })
  events = events.filter(unique)
  coverages = coverages.filter(unique)
  
  var margin = {top:50, right:50, bottom:50, left:50};
  // calculate width and height based on window size
  xwindow = window.innerWidth - margin.left - margin.right
  ywindow = window.innerHeight - margin.top - margin.bottom
  xgrid = Math.max(1, Math.floor(xwindow / coverages.length))
  ygrid = Math.max(3, Math.floor(ywindow / events.length))
  ywindow = ygrid * events.length + margin.bottom
  console.log(xgrid)
  console.log(ygrid)

  // svg container
  var svg = d3.select("#heatmap")
      .append("svg")
      .attr("width", xwindow)
      .attr("height", ywindow)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // linear colour scale
  var colors = d3.scaleLinear()
      .domain(d3.range(0, 1, 0.1))
      .range(["#040082", "#0026ff", "#ffffff", "#ff8585", "#ff4242", "#de0000", "#a10000", "#a10000", "#a10000", "#a10000"]);

  // var eventLabels = svg.selectAll(".eventLabel")
  //     .data(events)
  //     .enter()
  //     .append("text")
  //     .text(function(d) { return d; })
  //     .attr("x", 0)
  //     .attr("y", function(d, i) { return i * gridSize; })
  //     .style("text-anchor", "end")
  //       .attr("transform", "translate(-6," + gridSize / 1.5 + ")")

  // var coverageLabels = svg.selectAll(".coverageLabel")
  //   .data(coverages)
  //   .enter()
  //   .append("text")
  //   .text(function(d) { return d; })
  //   .attr("x", function(d, i) { return i * gridSize; })
  //   .attr("y", 0)
  //   .style("text-anchor", "middle")
  //   .attr("transform", "translate(" + gridSize / 2 + ", -6)");

  // group data by location
  var nest = d3.nest()
      .key(function(d) { return d.location; })
      .entries(data);

  // array of locations in the data
  var locations = nest.map(function(d) { return d.key; });
  var currentLocationIndex = 0;

  // function to create the initial heatmap
  var drawHeatmap = function(location) {

      // filter the data to return object of location of interest
      var selectLocation = nest.find(function(d) {
          return d.key == location;
      });
      var heatmap = svg.selectAll(".score")
      .data(selectLocation.values)
      .enter()
      .append("rect")
      .attr("x", function(d) { return (coverages.indexOf(d.coverage_name)-1) * xgrid; })
      .attr("y", function(d) { return (events.indexOf(d.event_name)-1) * ygrid; })
      .attr("class", "hour bordered")
      .attr("width", xgrid)
      .attr("height", ygrid)
      .style("stroke", "white")
      .style("stroke-opacity", 0.6)
      .style("fill", function(d) { return colors(d.score); })
  }   
  drawHeatmap(locations[0]);

  d3.selectAll(".nav").on("click", function() {
    if(d3.select(this).classed("left")) {
      if(currentLocationIndex == 0) {
        currentLocationIndex = locations.length-1;
      } else {
        currentLocationIndex--;  
      }
    } else if(d3.select(this).classed("right")) {
      if(currentLocationIndex == locations.length-1) {
        currentLocationIndex = 0;
      } else {
        currentLocationIndex++;  
      }
    }
    d3.select("#locationMenu").property("score", currentLocationIndex)
    updateHeatmap(locations[currentLocationIndex]);
  })
});
