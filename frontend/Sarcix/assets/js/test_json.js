//example provided by https://bl.ocks.org/officeofjane/11b54880abcb6b844637cb1d7a120cd5

var dataset;
  var days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
	times = d3.range(24);
  
  var margin = {top:40, right:50, bottom:70, left:50};
  
  // calculate width and height based on window size
  var w = Math.max(Math.min(window.innerWidth, 1000), 500) - margin.left - margin.right - 20,
  gridSize = Math.floor(w / times.length),
	h = gridSize * (days.length+2);

  //reset the overall font size
	var newFontSize = w * 62.5 / 900;
	d3.select("html").style("font-size", newFontSize + "%");
  
  // svg container
  var svg = d3.select("#heatmap")
  	.append("svg")
  	.attr("width", w + margin.top + margin.bottom)
  	.attr("height", h + margin.left + margin.right)
  	.append("g")
  	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  // linear colour scale
  var colours = d3.scaleLinear()
  	.domain(d3.range(1, 11, 1))
  	.range(["#87cefa", "#86c6ef", "#85bde4", "#83b7d9", "#82afce", "#80a6c2", "#7e9fb8", "#7995aa", "#758b9e", "#708090"]);
  
  var dayLabels = svg.selectAll(".dayLabel")
  	.data(days)
  	.enter()
  	.append("text")
  	.text(function(d) { return d; })
  	.attr("x", 0)
  	.attr("y", function(d, i) { return i * gridSize; })
  	.style("text-anchor", "end")
		.attr("transform", "translate(-6," + gridSize / 1.5 + ")")

  var timeLabels = svg.selectAll(".timeLabel")
    .data(times)
    .enter()
    .append("text")
    .text(function(d) { return d; })
    .attr("x", function(d, i) { return i * gridSize; })
    .attr("y", 0)
    .style("text-anchor", "middle")
    .attr("transform", "translate(" + gridSize / 2 + ", -6)");

  // load data
  d3.json("./static/js/test_data.json", function(error, data) {
    data.forEach(function(d) {
        d.day = +d.day; //+ is numeric operator conversion
        d.hour = +d.hour;
        d.value = +d.value;
    });
    dataset = data;

    //(irrelevant since we don't need to switch maps in one run)
    // group data by location
    var nest = d3.nest()
      .key(function(d) { return d.location; })
      .entries(dataset);

    // array of locations in the data
    var locations = nest.map(function(d) { return d.key; });
    var currentLocationIndex = 0;

    // create location dropdown menu
    var locationMenu = d3.select("#locationDropdown");
    locationMenu
      .append("select")
      .attr("id", "locationMenu")
      .selectAll("option")
        .data(locations)
        .enter()
        .append("option")
        .attr("value", function(d, i) { return i; })
        .text(function(d) { return d; });

    // function to create the initial heatmap
    var drawHeatmap = function(location) {

      // filter the data to return object of location of interest
      var selectLocation = nest.find(function(d) {
        return d.key == location;
      });

      var heatmap = svg.selectAll(".hour")
        .data(selectLocation.values)
        .enter()
        .append("rect")
        .attr("x", function(d) { return (d.hour-1) * gridSize; })
        .attr("y", function(d) { return (d.day-1) * gridSize; })
        .attr("class", "hour bordered")
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("stroke", "white")
        .style("stroke-opacity", 0.6)
        .style("fill", function(d) { return colours(d.value); })
      }
    drawHeatmap(locations[currentLocationIndex]);

    var updateHeatmap = function(location) {
      console.log("currentLocationIndex: " + currentLocationIndex)
      // filter data to return object of location of interest
      var selectLocation = nest.find(function(d) {
        return d.key == location;
      });

      // update the data and redraw heatmap
      var heatmap = svg.selectAll(".hour")
        .data(selectLocation.values)
        .transition()
          .duration(500)
          .style("fill", function(d) { return colours(d.value); })
    }

    // run update function when dropdown selection changes
    locationMenu.on("change", function() {
      // find which location was selected from the dropdown
      var selectedLocation = d3.select(this)
        .select("select")
        .property("value");
      currentLocationIndex = +selectedLocation;
      // run update function with selected location
      updateHeatmap(locations[currentLocationIndex]);
    });    

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
      d3.select("#locationMenu").property("value", currentLocationIndex)
      updateHeatmap(locations[currentLocationIndex]);
    })
  })