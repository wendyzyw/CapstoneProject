function drawForceGraph(data, htmlElem){
	var svg = d3.select(htmlElem),
		width = +svg.attr("width"),
		height = +svg.attr("height");

	// var color = d3.scaleOrdinal(d3.schemeCategory20);
	var color_palettes = ['#4abdac', '#fc4a1a', '#f7b733', '#f03b20', '#feb24c', '#ffeda0', '#007849', '#0375b4', '#ffce00', '#373737', '#dcd0c0', '#c0b283', '#e37222', '#07889b', '#eeaa7b', '#062f4f', '#813772', '#b82601', '#565656', '#76323f', '#c09f80'];
	
	var color = d3.scaleOrdinal(color_palettes);

	var simulation = d3.forceSimulation()
		.force("link", d3.forceLink().id(function(d) { return d.id; }))
		.force("charge", d3.forceManyBody().strength(-1500))
		.force("center", d3.forceCenter(width / 2, height / 2));
		
	var defs = svg.append('svg:defs');
	
	var config = {
		"avatar_size" : 60
	}

	defs.append("svg:pattern")
		.attr("id", "twitter")
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("patternUnits", "patternContentUnits")
		.append("svg:image")
		.attr("xlink:href", '../static/img/tw.png')
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("x", 0)
		.attr("y", 0);
	
	defs.append("svg:pattern")
		.attr("id", "facebook")
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("patternUnits", "patternContentUnits")
		.append("svg:image")
		.attr("xlink:href", '../static/img/fb.png')
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("x", 0)
		.attr("y", 0);
		
	defs.append("svg:pattern")
		.attr("id", "tumblr")
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("patternUnits", "patternContentUnits")
		.append("svg:image")
		.attr("xlink:href", '../static/img/tu.png')
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("x", 0)
		.attr("y", 0);
	
	defs.append("svg:pattern")
		.attr("id", "reddit")
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("patternUnits", "patternContentUnits")
		.append("svg:image")
		.attr("xlink:href", '../static/img/re.png')
		.attr("width", config.avatar_size)
		.attr("height", config.avatar_size)
		.attr("x", 0)
		.attr("y", 0);
		
	var link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(data.links)
		.enter().append("line")
		  .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

	var node = svg.append("g")
		.attr("class", "nodes")
		.selectAll("circle")
		.data(data.nodes)
		.enter().append("circle")
		.attr("r", function(d){
			if (d.id == 'twitter' || d.id == 'facebook' || d.id == 'tumblr' || d.id == 'reddit'){
				return 30;
			} else {
				return 15;
			}
		})
		.attr("fill", function(d) {
				if (d.id == 'twitter'){
					return "url(#twitter)";
				} else if (d.id == 'facebook'){
					return "url(#facebook)";
				} else if (d.id == 'tumblr'){
					return "url(#tumblr)";
				} else if (d.id == 'reddit'){
					return "url(#reddit)";
				} else {
					return color(d.group); 
				}
			})
		.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended));
	  var text_dx = -25;
	  var text_dy = 40;
	  var nodes_text = svg.selectAll(".nodetext")
									.data(data.nodes)
									.enter()
									.append("text")
									.attr("class","nodetext")
									.style("font-family", "azo-sans-web")
									.style("stroke", "white")
									.attr("dx",text_dx)
									.attr("dy",text_dy)
									.text(function(d){
										return d.id;
									});

	  node.append("title")
		  .text(function(d) { return d.id; });

	  simulation
		  .nodes(data.nodes)
		  .on("tick", ticked);

	  simulation.force("link")
		  .links(data.links);

	  function ticked() {
		link
			.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });

		node
			.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });
		nodes_text
			.attr("x",function(d){ return d.x })
			.attr("y",function(d){ return d.y });
	  }

	function dragstarted(d) {
	  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
	  d.fx = d.x;
	  d.fy = d.y;
	}

	function dragged(d) {
	  d.fx = d3.event.x;
	  d.fy = d3.event.y;
	}

	function dragended(d) {
	  if (!d3.event.active) simulation.alphaTarget(0);
	  d.fx = null;
	  d.fy = null;
	}
}