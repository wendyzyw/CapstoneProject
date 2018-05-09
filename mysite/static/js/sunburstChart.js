
function drawSunburst(plotDiv,bcDiv,data){
	initializeBreadcrumbTrail();
	// Breadcrumb dimensions: width, height, spacing, width of tip/tail.
	var b = {
		w: 170, h: 40, s: 5, t: 12
	};
	// responsive svg
	var svg = d3.select(plotDiv).append("svg")
	  .attr("width", w)
	  .attr("height", h)
	  .append("g")
	  .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

	var arc = d3.svg.arc()
	  .startAngle(function(d) {
		return Math.max(0, Math.min(2 * Math.PI, x(d.x)));
	  })
	  .endAngle(function(d) {
		return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx)));
	  })
	  .innerRadius(function(d) {
		var a = Math.max(0, y(d.y));
		if (a == 0){
			return 0;
		} else if (a == 70){
			return 6;
		} else if (a == 140){
			return 108;
		} else {
			return a;
		}
	  })
	  .outerRadius(function(d) {
		var a = Math.max(0, y(d.y + d.dy));
		if (a == 70){
			return 6;
		} else if (a == 140){
			return 108;
		} else if (a == 210){
			return 210;
		} else {
			return a;
		}
	  });
	  
	function getcrumbpath(a) {
		for (var temp = [], c = a; c.parent;) temp.unshift(c), c = c.parent;
		return temp;
	}
	// Given a node in a partition layout, return an array of all of its ancestor
	// nodes, highest first, but excluding the root.
	function getAncestors(node) {
	  var path = [];
	  var current = node;
	  while (current.parent) {
		path.unshift(current);
		current = current.parent;
	  }
	  return path;
	}

	function initializeBreadcrumbTrail() {
	  // Add the svg area.
	  var trail = d3.select(bcDiv).append("svg:svg")
		  .attr("width", 400)
		  .attr("height", 50)
		  .attr("id", "trail");
	  // Add the label at the end, for the percentage.
	  trail.append("svg:text")
		.attr("id", "endlabel")
		.style("fill", "#000");
	}

	// Generate a string that describes the points of a breadcrumb polygon.
	function breadcrumbPoints(d, i) {
	  var points = [];
	  points.push("0,0");
	  points.push(b.w + ",0");
	  points.push(b.w + b.t + "," + (b.h / 2));
	  points.push(b.w + "," + b.h);
	  points.push("0," + b.h);
	  if (i > 0) { // Leftmost breadcrumb; don't include 6th vertex.
		points.push(b.t + "," + (b.h / 2));
	  }
	  return points.join(" ");
	}

	// Update the breadcrumb trail to show the current sequence and percentage.
	function updateBreadcrumbs(nodeArray) {

	  // Data join; key function combines name and depth (= position in sequence).
	  var g = d3.select("#trail")
		  .selectAll("g")
		  .data(nodeArray, function(d) { return d.name + d.depth; });

	  // Add breadcrumb and label for entering nodes.
	  var entering = g.enter().append("svg:g");

	  entering.append("svg:polygon")
		  .attr("points", breadcrumbPoints)
		  .style("fill", function(d) { return color(d.x); });

	  entering.append("svg:text")
		  .attr("x", (b.w + b.t) / 2)
		  .attr("y", b.h / 2)
		  .attr("dy", "0.35em")
		  .attr("text-anchor", "middle")
		  .style("stroke", "white")
		  .style("fill", "white")
		  .text(function(d) { return d.name; });

	  // Set position for entering and updating nodes.
	  g.attr("transform", function(d, i) {
		return "translate(" + i * (b.w + b.s) + ", 0)";
	  });

	  // Remove exiting nodes.
	  g.exit().remove();

	  <!-- // Now move and update the percentage at the end. -->
	  <!-- d3.select("#trail").select("#endlabel") -->
		  <!-- .attr("x", (nodeArray.length + 0.5) * (b.w + b.s)) -->
		  <!-- .attr("y", b.h / 2) -->
		  <!-- .attr("dy", "0.35em") -->
		  <!-- .attr("text-anchor", "middle") -->
		  <!-- .text(percentageString); -->

	  // Make the breadcrumb trail visible, if it's hidden.
	  d3.select("#trail")
		  .style("visibility", "");

	}
	
	function mouseover(data) {
		<!-- chart.refreshChart(data); -->
		d3.select(this).style("cursor", "pointer");
		var c = getcrumbpath(data);
		var sequenceArray = getAncestors(data);
		updateBreadcrumbs(sequenceArray);
		d3
			.selectAll(plotDiv+" path")
			.style("opacity", .3), svg
			.selectAll("path")
			.filter(function (a) { return c.indexOf(a) >= 0 })
			.style("opacity", 1);
	}
	function mouseleave() {
		d3
			.selectAll("path")
			.on("mouseover", null);
		d3
			.selectAll("path")
			.transition()
			.duration(1e3)
			.style("opacity", 1)
			.each("end", function () { d3.select(this).on("mouseover", mouseover) });
	}

	  var g = svg.selectAll("path")
		.data(partition.nodes(data))
		.enter().append("g");

	  var path = g.append("path")
		.attr("d", arc)
		.style("fill", function(d) {
		  return d.parent ? color(d.x) : "white";
		})
		.style("stroke", "white")
		.style("stroke-width", "1px")
		.on("click", click)
		<!-- .on("mouseover", function(d, i) { -->
		  <!-- d3.select(this).style("cursor", "pointer") -->
		  <!-- var totalSize = path.node().__data__.value; -->
		  <!-- <!-- var percentage = Math.round(((100 * d.value / totalSize) * 100) / percentBase); --> -->
		  <!-- var percentage = d.percent*100; -->
		  <!-- var percentageString = percentage + "%"; -->
		  <!-- if (d.name == "Sources") return null; -->
		  <!-- tooltip.text(d.name + " " + percentageString) -->
			<!-- .style("opacity", 0.8) -->
			<!-- .style("left", (d3.event.pageX) + 0 + "px") -->
			<!-- .style("top", (d3.event.pageY) - 0 + "px"); -->
		  <!-- if (d.name == "Sources") { -->
			<!-- return null; -->
		  <!-- } -->
		<!-- }) -->
		<!-- .on("mouseout", function(d) { -->
		  <!-- d3.select(this).style("cursor", "default") -->
		  <!-- tooltip.style("opacity", 0); -->
		<!-- }); -->
		.on("mouseover", mouseover)
		.on("mouseout", function(d){
			d3.select(this).style("cursor","default");
			d3.selectAll(plotDiv+" path")
			.style("opacity", 1)
		});


	  var text = g.append("text")
		.attr("transform", function(d) {
		  return "translate(" + arc.centroid(d) + ")rotate(" + computeTextRotation(d) + ")";
		})
		.attr("text-anchor", "middle")
		.attr("dx", "0") // margin
		.attr("dy", ".35em") // vertical-align
		.text(function(d) {
		  return d.name == "Commercial Cooking" ? "Cooking" : d.name == "Natural Gas" ? "Gas" :
			d.name == "Construction Dust" ? "Const Dust" : d.name == "Residual Oil" ? "Res Oil" :
			d.name == "Distillate Oil" ? "Dist Oil" : d.name == "Non-Road" ? "Non Rd" :
			d.name == "Non Road Equipment" ? "Equip" : d.name == "Marine Vessels" ? "Vessels" :
			d.name == "Electric Generation" ? "Elec Gen" : d.name == "Road Dust" ? "Rd Dust" :
			d.name == "Sources" ? null : d.name;
		})
		.style("font-size", "10px")
		.style("stroke","white")
		.on("mouseover", mouseover)
		.on("mouseout", function(d){
			d3.select(this).style("cursor","default");
			d3.selectAll(plotDiv+" path")
			.style("opacity", 1)
		});
	
    function click(d) {
		<!-- percentBase = parseFloat(d.percent.split("%")[0]); -->
		percentBase = d.percent;
		if (d.name == "Sources") percentBase = 100;
		  // fade out all text elements
		text.transition().attr("opacity", 0);

		path.transition()
		  .duration(750)
		  .attrTween("d", arcTween(d))
		  .each("end", function(e, i) {
			// check if the animated element's data e lies within the visible angle span given in d
			if (e.x >= d.x && e.x < (d.x + d.dx)) {
			  // get a selection of the associated text element
			  var arcText = d3.select(this.parentNode).select("text");
			  // fade in the text element and recalculate positions
			  arcText.transition().duration(750)
				.attr("opacity", 1)
				.attr("transform", function(d) {
				  return "translate(" + arc.centroid(d) + ")rotate(" + computeTextRotation(d) + ")";
				})
				.attr("text-anchor", "middle");
			}
		  });
   }
   
   // Interpolate the scales!
	function arcTween(d) {
	  var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
		yd = d3.interpolate(y.domain(), [d.y, 1]),
		yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
	  return function(d, i) {
		return i ? function(t) {
		  return arc(d);
		} : function(t) {
		  x.domain(xd(t));
		  y.domain(yd(t)).range(yr(t));
		  return arc(d);
		};
	  };
	}

	function computeTextRotation(d) {
	  var ang = (x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180;
	  return (ang > 90) ? 180 + ang : ang;
	}
};
