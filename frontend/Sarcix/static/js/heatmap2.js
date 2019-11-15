events = []
coverages = []

function unique(value, index, self) { 
    return self.indexOf(value) === index;
}

d3.json('/get_runs', function(data) {
    data.forEach(function(d){
        events.push(d.event_name) //make unique
        coverages.push(d.coverage_name)

        // d.event_name = +d.event_name;
        // d.coverage_name = +d.coverage_name;
        d.score = +d.score;
    })
    events = events.filter(unique)
    coverages = coverages.filter(unique)

    console.log(events)
    console.log(coverages)
    
    var margin = {top:50, right:50, bottom:70, left:200};
    // calculate width and height based on window size
    var w = Math.max(Math.min(window.innerWidth, 1000), 500) - margin.left - margin.right - 20,
    gridSize = Math.floor(w / 100),//coverages.length),
        h = gridSize * 10;//(events.length+2);

    //reset the overall font size
    var newFontSize = w * 10 / 900;
    d3.select("html").style("font-size", newFontSize + "%");

    // svg container
    var svg = d3.select("#heatmap")
        .append("svg")
        .attr("width", w + margin.top + margin.bottom)
        .attr("height", h + margin.left + margin.right)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // linear colour scale
    var colors = d3.scaleLinear()
        .domain(d3.range(1, 11, 1))
        .range(["#87cefa", "#86c6ef", "#85bde4", "#83b7d9", "#82afce", "#80a6c2", "#7e9fb8", "#7995aa", "#758b9e", "#708090"]);

    var eventLabels = svg.selectAll(".eventLabel")
        .data(events)
        .enter()
        .append("text")
        .text(function(d) { return d; })
        .attr("x", 0)
        .attr("y", function(d, i) { return i * gridSize; })
        .style("text-anchor", "end")
          .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
  
    var coverageLabels = svg.selectAll(".coverageLabel")
      .data(coverages)
      .enter()
      .append("text")
      .text(function(d) { return d; })
      .attr("x", function(d, i) { return i * gridSize; })
      .attr("y", 0)
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + gridSize / 2 + ", -6)");

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
        .attr("x", function(d) { return (events.indexOf(d.event_name)-1) * gridSize; })
        .attr("y", function(d) { return (coverages.indexOf(d.coverage_name)-1) * gridSize; })
        .attr("class", "hour bordered")
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("stroke", "white")
        .style("stroke-opacity", 0.6)
        .style("fill", function(d) { return colors(d.score); })
    }   
    drawHeatmap(locations[0]);


// var updateHeatmap = function(location) {
//     console.log("currentLocationIndex: " + currentLocationIndex)
//     // filter data to return object of location of interest
//     var selectLocation = nest.find(function(d) {
//       return d.key == location;
//     });

//     // update the data and redraw heatmap
//     var heatmap = svg.selectAll(".hour")
//       .data(selectLocation.values)
//       .transition()
//         .duration(500)
//         .style("fill", function(d) { return colours(d.value); })
//   }

//   d3.selectAll(".nav").on("click", function() {
//     if(d3.select(this).classed("left")) {
//       if(currentLocationIndex == 0) {
//         currentLocationIndex = locations.length-1;
//       } else {
//         currentLocationIndex--;  
//       }
//     } else if(d3.select(this).classed("right")) {
//       if(currentLocationIndex == locations.length-1) {
//         currentLocationIndex = 0;
//       } else {
//         currentLocationIndex++;  
//       }
//     }
//     d3.select("#locationMenu").property("score", currentLocationIndex)
//     updateHeatmap(locations[currentLocationIndex]);
//   })
});
