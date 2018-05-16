function CurveGen(e, t) {
	<!-- var p = t ? 1e3 : 0; -->
	
	function formatNumber(e) {
		return String(e).replace(/(\d)(?=(\d{3})+$)/g, "$1,")
	}
	function a(t, a, n) {
		var o = void 0 != a ? e[a].Id : n;
		$("path.path_padding:not([data-brand-id='" + o + "'])").hide();
		var r = d3.selectAll("path.curve:not([data-brand-id='" + o + "'])");
		if (r.transition().duration(function (e, t) { return 200 }).style("opacity", w.opacity.dim), 
			r.transition().delay(200).duration(function (e, t) { return 10 * t }).attr("d", O), 
			d3.select("path[data-brand-id='" + o + "']").style({ "stroke-width": 3.5 * w.strokeWidth }), 
			void 0 == a && (a = parseInt($("path[data-brand-id='" + o + "']").attr("id").replace("curve", ""))), 
			<!-- "loved" != _mostLovedOrTalkedAbout ? $("#tool_tip .tt_score").addClass("talkedabout") : $("#tool_tip .tt_score").removeClass("talkedabout"),  -->
			$("#tool_tip .tt_score span").html(function () {
				var t = e[a][l];
				return t = "+" + Math.round(t) /* : formatNumber(Math.round(t)) */
			}), 
			$("#tool_tip .tt_brand").html(function () {
				return e[a].DisplayName
			}), 
			$(".tt_stats").show(), 
			$("#tool_tip").finish().fadeIn(500), n) 
			{
				$("#tool_tip .flip").removeClass("flip");
					var i = {
						top: $("path.path_padding[data-brand-id='" + n + "']").offset().top - 5 - V + "px",
						left: $("#main_graph").offset().left + $("#main_graph").width() / 2 + 2 + "px"
					};
					$("#tool_tip").animate({
						top: i.top,
						left: i.left
					}, 300)
			}
	}
	function n(t, a, n) {
		var o = void 0 != a ? e[a].Id : n;
		d3.select("path[data-brand-id='" + o + "']").style({
			"stroke-width": w.strokeWidth
		}),
		d3.selectAll("path.curve:not([data-brand-id='" + o + "'])").transition().duration(function (e, t) {
			return 10 * t
		}).ease("back-out").attr("d", R).style({
			opacity: w.opacity.on
		}),
		$("path.path_padding").show(),
		($("#tool_tip").finish().fadeOut(200), setTimeout(function () {}, 20))
	}
	function o(e, t) {
		$("#tool_tip").css({
			top: function () {
				return d3.event.pageY - 23 + "px"
			},
			left: function () {
				return d3.event.pageX + 20 + 1.1 * $("#tool_tip").width() > window.innerWidth ? 
				($("#tool_tip .tt_score").addClass("flip"), 
				$("#tool_tip .tt_stats").addClass("flip"), 
				$("#tool_tip .tt_brand").addClass("flip"), 
				d3.event.pageX - 20 - $("#tool_tip").width() + "px") : ($("#tool_tip .flip").removeClass("flip"), d3.event.pageX + 20 + "px")
			}
		})
	}
	function r(t, a, n) {
		n && (a = parseInt($("path[data-brand-id='" + n + "']").attr("id").replace("curve", ""))),
		$("#tool_tip").fadeOut(500),
		d3.selectAll(".curve").transition().duration(750).attr("d", A),
		setTimeout(function () {
			$("#graph").fadeOut(500)
			<!-- curveClick(e[a]) -->
		}, 750)
	}
	function i(e) {
		return e /= 2,
		d3.range(0, 6.5, .25).map(function (t) {
			return 6.25 == t ? 0 : -e * Math.cos(t) + e
		})
	}

	function s() {
		var e = d3.max(p, function (e) {
				return d3.max(e)
			});
		return e *= 1.1,
		Math.ceil(e)
	}
	function d() {
		y = !0,
		d3.selectAll("#main_graph path.curve").transition().duration(function (e, t) {
			return 1e3
		}).ease("circle-in-out").attr("d", d3.svg.line().x(function (e, t) {
				return k(t)
			}).y(function (e, t) {
				return C(e * Math.random())
			}).interpolate("cardinal"))
	}
	function c() {
		clearInterval(G),
		d3.selectAll("#main_graph path.curve").transition().duration(1e3).ease("elastic-in").attr("d", R),
		y = !1
	}

	var l = "IndexScore",
	p = function (t) {
		for (var a = [], n = d3.min(e, function (e) {
					return +e[l]
				}), o = 0; o < t.length; o++)
			a.push(i(t[o][l] - n));
		return a
	}(e),
	u = e,
	h = $(window).innerWidth(),
	f = $(window).innerHeight() - 124,
	v = {
		top: 30,
		right: 150,
		bottom: 30,
		left: 150
	},
	m = h - v.right - v.left - 320,
	g = f - v.top - v.bottom - 400,
	b = !1,
	<!-- y = !(!isMobile.phone && !isMobile.tablet), -->
	w = {
		strokeWidth: 2.5,
		opacity: {
			on: 1,
			dim: .1
		}
	},
	k = d3.scale.linear().domain([0, 25]).range([0, m]),
	C = d3.scale.linear().domain([0, s()]).range([g, 0]),
	x = d3.select("#graph").append("svg").attr({
			viewBox: "0 0 " + (v.left-50) + " " + g,
			preserveAspectRatio: "xMidYMid meet",
			width: (v.left-50),
			height: g
		}),
	S = x.append("svg:defs").append("linearGradient").attr("id", "gradL");
	console.log(m);
	console.log(g);
	
	S.append("stop").attr({
		"stop-color": endcolor.purple,
		"stop-opacity": 0,
		offset: "40%"
	});
	S.append("stop").attr({
		"stop-color": endcolor.purple,
		"stop-opacity": 1,
		offset: "100%"
	}),
	x.append("g").append("line").attr({
		x1: 0,
		y1: g,
		x2: "100%",
		y2: g
	}).style({
		stroke: endcolor.purple,
		"stroke-width": "3px",
		"shape-rendering": "crispEdges"
	});

	var D = d3.select("#graph").append("svg").attr("id", "main_graph").attr({
			viewBox: "0 0 " + m + " " + g,
			preserveAspectRatio: "xMidYMin slice",
			width: m,
			height: g
		});
	D.append("g").append("line").attr({
		x1: 0,
		y1: g,
		x2: m,
		y2: g
	}).style({
		stroke: endcolor.purple,
		"stroke-width": "3px",
		"shape-rendering": "crispEdges"
	});
	var I = d3.select("#graph").append("svg").attr({
			viewBox: "0 0 " + (v.right-50) + " " + g,
			preserveAspectRatio: "xMidYMin slice",
			width: (v.right-50),
			height: g
		}),
	M = I.append("svg:defs").append("linearGradient").attr("id", "gradR");
	M.append("stop").attr({
		"stop-color": endcolor.purple,
		"stop-opacity": 1,
		offset: "0%"
	}),
	M.append("stop").attr({
		"stop-color": endcolor.purple,
		"stop-opacity": 0,
		offset: "60%"
	}),
	I.append("g").append("line").attr({
		x1: 0,
		y1: g,
		x2: "100%",
		y2: g
	}).style({
		stroke: endcolor.purple,
		"stroke-width": "3px",
		"shape-rendering": "crispEdges"
	});
	var B = D.append("defs");
	for (var T in gradients)
		if (gradients.hasOwnProperty(T))
			for (var L in gradients[T])
				if (gradients[T].hasOwnProperty(L)) {
					var N = B.append("linearGradient").attr("id", "gradient_" + T + "_" + L);
					N.append("stop").attr({
						"stop-color": endcolor.purple,
						"stop-opacity": 1,
						offset: "0"
					}),
					N.append("stop").attr({
						"stop-color": gradients[T][L],
						"stop-opacity": 1,
						offset: "0.4"
					}),
					N.append("stop").attr({
						"stop-color": endcolor.purple,
						"stop-opacity": 1,
						offset: "1"
					})
				}
	var A = d3.svg.line().x(function (e, t) {
			return k(+t)
		}).y(function (e, t) {
			return C(0)
		}).interpolate("cardinal"),
	O = d3.svg.line().x(function (e, t) {
			return k(t)
		}).y(function (e, t) {
			return C(.75 * e)
		}).interpolate("cardinal"),
	R = d3.svg.line().x(function (e, t) {
			return k(t)
		}).y(function (e, t) {
			return C(e)
		}).interpolate("cardinal");

	//color_curves
	D.append("g").attr("class", "color_curves").selectAll("path").data(p).enter().append("path").attr("class", "curve").attr("id", function (e, t) {
		return "curve" + t
	}).attr("data-brand-id", function (t, a) {
		return e[a].Id
	}).attr("d", A).style({
		opacity: 0
	}).style({"stroke-width": 3+"px"})
	.transition().duration(function () {
		return t ? 1e3 : 0
	}).delay(function (e, a) {
		return a == p.length - 10 && setTimeout(function () {
			b = !0
		}, 10 * a),
		t ? 10 * a : 0
	}).ease("back-out").attr("d", R).style({
		opacity: 1
	}).attr("class", function (e) {
		return e[13] < 0 ? e[13] > -s() / 10 ? "curve negative_1-10" : e[13] > -s() / 9 ? "curve negative_2-10" : e[13] > -s() / 8 ? "curve negative_3-10" : e[13] > -s() / 7 ? "curve negative_4-10" : e[13] > -s() / 6 ? "curve negative_5-10" : e[13] > -s() / 5 ? "curve negative_6-10" : e[13] > -s() / 4 ? "curve negative_7-10" : e[13] > -s() / 3 ? "curve negative_8-10" : e[13] > -s() / 2 ? "curve negative_9-10" : "curve negative_10-10" : e[13] > s() ? "curve positive_10-10" : e[13] > s() / 2 ? "curve positive_9-10" : e[13] > s() / 3 ? "curve positive_8-10" : e[13] > s() / 4 ? "curve positive_7-10" : e[13] > s() / 5 ? "curve positive_6-10" : e[13] > s() / 6 ? "curve positive_5-10" : e[13] > s() / 7 ? "curve positive_4-10" : e[13] > s() / 8 ? "curve positive_3-10" : e[13] > s() / 9 ? "curve positive_2-10" : "curve positive_1-10"
	}),

	//padding_curves
	D.append("g").attr("class", "padding_curves").selectAll("path").data(p).enter().append("path").attr("class", "path_padding").attr("id", function (e, t) {
		return "curve" + t
	}).attr("data-brand-id", function (t, a) {
		return e[a].Id
	}).attr("d", R).on("mouseover", function (e, t) {
		b && a(e, t)
	}).on("mousemove", function (e, t) {
		b && o(e, t)
	}).on("mouseout", function (e, t) {
		b && n(e, t)
	}).on("mousedown", function (e, t) {
		b && r(e, t)
	});
}