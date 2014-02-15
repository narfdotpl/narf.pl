#--------
#  Typo
#--------

lineHeight = 28
capHeight = lineHeight / 1.4
ascenderHeight = lineHeight / 20  # o rly?
descenderHeight = lineHeight - capHeight


#-------------
#  Data type
#-------------

valuesToFloat = (d) ->
    for level in [1..countLevels(d)]
        key = "v#{level}"
        d[key] = parseFloat(d[key], 10)

    d


#----------------
#  Data helpers
#----------------

countLevels = (d) ->
    level = 1
    while true
        nextLevel = level + 1
        key = "v#{nextLevel}"
        break if key not of d
        level = nextLevel

    level


# d.v1 + d.v2 + ...
sumValues = (d) ->
    sum = 0

    for level in [1..countLevels(d)]
        key = "v#{level}"
        sum += d[key]

    sum


sumValuesBelowLevel = (d, maxLevel) ->
    sum = 0

    for level in [1...maxLevel]
        key = "v#{level}"
        sum += d[key]

    sum


isoDateToTimeStamp = (isoDate) ->
    new Date(isoDate).getTime()


#----------------
#  Actual chart
#----------------

window.addChart = ({csv, title, subtitle, legend}) ->
    # make space for legend
    if legend
        numberOfLegendLines = 1 + Math.ceil(legend.length / 2)
    else
        numberOfLegendLines = 0

    chartWidth  = 1024
    chartHeight = (14 + numberOfLegendLines) * lineHeight

    # compute dimensions
    numberOfBars = 50
    barWidth = 18
    leftMargin = 50
    margins =
        top:    3 * lineHeight
        right:  chartWidth - leftMargin - numberOfBars * barWidth
        left:   leftMargin
        bottom: (1 + numberOfLegendLines) * lineHeight

    width  = chartWidth  - margins.left - margins.right
    height = chartHeight - margins.top  - margins.bottom - descenderHeight

    # create SVG chart
    chart = d3.select('.entry-content').append('svg')
        .attr('class', 'chart')
        .attr('width',  chartWidth)
        .attr('height', chartHeight)
      .append('g')
        .attr('transform', "translate(#{margins.left}, #{margins.top})")

    # get data
    d3.csv "../data/chart-csv/#{csv}.csv", valuesToFloat, (data) ->
        # add title
        titleY = -margins.top + capHeight + ascenderHeight
        if title
            chart.append('text')
                .attr('class', 'title')
                .attr('x', width / 2)
                .attr('y', titleY)
                .text(title)

        # add subtitle
        if subtitle
            chart.append('text')
                .attr('class', 'subtitle')
                .attr('x', width / 2)
                .attr('y', titleY + lineHeight)
                .text(subtitle)

        # set x scale
        xScale = d3.scale.ordinal()
            .rangeRoundBands([0, width])
            .domain(data.map((d) -> d.date))

        # set x time scale
        firstTimeStamp = isoDateToTimeStamp(data[0].date)
        lastTimeStamp = isoDateToTimeStamp(data[data.length - 1].date)
        secondLastTimeStamp = isoDateToTimeStamp(data[data.length - 2].date)
        rightBorderTimeStamp = \
            lastTimeStamp + lastTimeStamp - secondLastTimeStamp
        xTimeScale = d3.time.scale()
            .range([0, width])
            .domain([firstTimeStamp, rightBorderTimeStamp])

        # set x axis
        xAxis = d3.svg.axis()
            .scale(xTimeScale)
            .orient('bottom')
            .innerTickSize(8)
            .outerTickSize(0)

        # set y scale
        yScale = d3.scale.linear()
            .range([height, 0])
            .domain([0, d3.max(data, sumValues)])

        # set y axis
        yAxis = d3.svg.axis()
            .scale(yScale)
            .orient('left')
            .ticks(5)
            .tickFormat((x) -> x)
            .outerTickSize(0)

        # get colors
        colors = colorbrewer['GnBu'][9].slice().reverse()
        colors[1] = colors[3]

        # create bars
        bar = chart.selectAll('.bar')
            .data(data)
          .enter().append('g')
            .attr('class', 'bar')
            .attr('transform', (d) -> "translate(#{xScale(d.date)}, 0)")

        # add all bar levels
        for level in [1..countLevels(data[0])]
            key = "v#{level}"

            dx = 1
            dy = if level == 2 then dx else 0

            # ceil height and floor y position to get rid of distorted borders
            # (fraction of a pixel less accurate but more readable)
            bar.append('rect')
                .attr('width', xScale.rangeBand() - dx)
                .attr('height', (d) -> height - yScale(d[key]) - dy)
                .attr('y', (d) ->
                    yScale(d[key] + sumValuesBelowLevel(d, level)))
                .attr('fill', colors[level - 1])

        # add green spotify line below the x axis
        spotifyTimeStamp = isoDateToTimeStamp('2013-02-12')
        spotifyX = Math.floor(xTimeScale(spotifyTimeStamp))
        chart.append('rect')
            .attr('class', 'spotify')
            .attr('x', spotifyX)
            .attr('y', height)
            .attr('width', xTimeScale(rightBorderTimeStamp) - spotifyX)
            .attr('height', 8)

        # add "Spotify" text next to the line
        chart.append('text')
            .attr('class', 'spotify')
            .attr('x', width + 5)
            .attr('y', height + 8)
            .text('Spotify')

        # add x axis to chart
        chart.append('g')
            .attr('class', 'x axis')
            .attr('transform', "translate(0, #{height})")
            .call(xAxis)
          .selectAll('text')
            .attr('y', ascenderHeight + lineHeight)
            .attr('dy', 0)
            # add "year" class to January 1st ticks
            .attr 'class', (date) ->
                if date.getMonth() == 0 and date.getDate() == 1
                    'year'

        # add y axis to chart
        chart.append('g')
            .attr('class', 'y axis')
            .call(yAxis)

        # add legend
        if legend
            legendRectSize =
                width: capHeight * 2
                height: capHeight

            legendG = chart.append('g')
                .attr('class', 'legend')
                .attr('transform', "translate(
                    #{-margins.left + (1024 - 640) / 2},
                    #{height + Math.round(ascenderHeight + descenderHeight) +
                      2 * lineHeight})")

            for i in [0...legend?.length]
                text = legend[i]
                color = colors[i]

                legendEntry = legendG.append('g')
                    .attr('transform', "translate(
                        #{(i % 2) * 640 / 2},
                        #{Math.floor(i / 2) * lineHeight})")

                legendEntry.append('rect')
                    .attr('width', legendRectSize.width)
                    .attr('height', legendRectSize.height)
                    .attr('y', descenderHeight / 2)
                    .attr('fill', color)

                legendEntry.append('text')
                    .attr('x', legendRectSize.width + 8)
                    .attr('y', capHeight)
                    .text(text)
