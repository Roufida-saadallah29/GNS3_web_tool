function draw_network(url) {
    const scale = d3.scaleOrdinal(d3.schemeCategory10)
    const color = d => scale(d.name[0])

    let height = 400
    let width = 400

    axios.get(url)
        .then(response => {

            let data = response.data

            chart = ForceGraph(data, {
                nodeId: d => d.node_id,
                nodeGroup: d => d.status,
                nodeTitle: d => `${d.name}`,
                width: 1250,
                height: 680,
            })

            $("#network_drawing").append(chart)
        });

}

function ForceGraph({
    nodes,
    links
}, {
    nodeId = d => d.node_id,
    nodeImage = d => d.symbol,
    nodeGroup,
    nodeGroups,
    nodeTitle,
    nodeFill = "currentColor",
    nodeStroke = "#fff",
    nodeStrokeWidth = 1.5,
    nodeStrokeOpacity = 0.5,
    nodeRadius = 25,
    nodeStrength,
    linkSource = ({ source }) => source,
    linkTarget = ({ target }) => target,
    linkStroke = "#999",
    linkStrokeOpacity = 0.6,
    linkStrokeWidth = 2.5,
    linkStrokeLinecap = "round",
    linkStrength,
    colors = d3.schemeTableau10,
    width = 640,
    height = 400,
    invalidation
} = {}) {
    const N = d3.map(nodes, nodeId).map(intern);
    const IMG = d3.map(nodes, nodeImage).map(intern);
    const LS = d3.map(links, linkSource).map(intern);
    const LT = d3.map(links, linkTarget).map(intern);
    if (nodeTitle === undefined) nodeTitle = (_, i) => N[i];
    const T = nodeTitle == null ? null : d3.map(nodes, nodeTitle);
    const G = nodeGroup == null ? null : d3.map(nodes, nodeGroup).map(intern);
    const W = typeof linkStrokeWidth !== "function" ? null : d3.map(links, linkStrokeWidth);


    nodes = d3.map(nodes, (_, i) => ({ id: N[i], symbol: IMG[i] }));
    links = d3.map(links, (_, i) => ({ source: LS[i], target: LT[i] }));


    if (G && nodeGroups === undefined) nodeGroups = d3.sort(G);


    const color = nodeGroup == null ? null : d3.scaleOrdinal(nodeGroups, colors);


    const forceNode = d3.forceManyBody().strength(-1250);
    const forceLink = d3.forceLink(links).id(({ index: i }) => N[i]);
    if (nodeStrength !== undefined) forceNode.strength(nodeStrength);
    if (linkStrength !== undefined) forceLink.strength(linkStrength);

    const simulation = d3.forceSimulation(nodes)
        .force("link", forceLink)
        .force("charge", forceNode)
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .on("tick", ticked);

    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    const link = svg.append("g")
        .attr("stroke", linkStroke)
        .attr("stroke-opacity", linkStrokeOpacity)
        .attr("stroke-width", typeof linkStrokeWidth !== "function" ? linkStrokeWidth : null)
        .attr("stroke-linecap", linkStrokeLinecap)
        .selectAll("line")
        .data(links)
        .join("line");

    if (W) link.attr("stroke-width", ({ index: i }) => W[i]);
    var node = svg.append("g")
        .attr("fill", nodeFill)
        .selectAll("circle")
        .data(nodes)
        .join("g")
    var a = node.append("image")
        .attr("r", nodeRadius)
        .attr('width', 45)
        .attr('xlink:href', function (d) {
            return d.symbol;
        })
        .call(drag(simulation));




    const label = node.append("text")
        .attr("x", 8)
        .attr("stroke", "#555")
        .attr("y", "0.31em")
        .attr("font-size", "1em")
        .attr("dy", "-0.5em")
        .attr("text-anchor", "middle")
        .text(({ index: i }) => T[i])
        .call(drag(simulation));
    if (G) a.attr("fill", ({ index: i }) => color(G[i]));



    if (invalidation != null) invalidation.then(() => simulation.stop());

    function intern(value) {
        return value !== null && typeof value === "object" ? value.valueOf() : value;
    }

    function ticked() {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        a
            .attr("x", d => d.x - 17.5)
            .attr("y", d => d.y - 12.5);

        label
            .attr("x", d => d.x + 5)
            .attr("dy", d => d.y + 32.5);
    }

    function drag(simulation) {
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    return Object.assign(svg.node(), { scales: { color } });
}