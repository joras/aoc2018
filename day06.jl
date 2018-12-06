struct Point
    x::Int16
    y::Int16
end

points = Set()
for line in readlines("day06.txt")
    m = match(r"(\d+), (\d+)", line)
    push!(points, Point(parse(Int16, m[1]), parse(Int16, m[2])))
end

function solve(points)
    x_sorted_points = sort(collect(points), by= p-> p.x)
    y_sorted_points = sort(collect(points), by= p-> p.y)

    x_min = first(x_sorted_points).x
    x_max = last(x_sorted_points).x
    y_min = first(y_sorted_points).y
    y_max = last(y_sorted_points).y

    x_range = x_max - x_min
    y_range = y_max - y_min

    areas = Dict()
    edge_areas = Set()
    search_area_size = 0

    for x in x_min:x_max
        for y in y_min:y_max

            #list of points with their distances
            points_dist = map(p->(p, abs(p.x-x) + abs(p.y-y)), collect(points))
            sortedpoints = sort(points_dist, by = x->x[2])

            if (sortedpoints[1][2] != sortedpoints[2][2])
                closest = sortedpoints[1][1]

                area = get(areas, closest, 0)
                areas[closest] = area + 1

                # if area touches the edge, mark it as such
                if x == x_min || x == x_max || y == y_min || y == y_max
                    push!(edge_areas, closest)
                end
            end

            # for part 2
            totaldist = sum(x->x[2], points_dist)
            if totaldist < 10000
                search_area_size=search_area_size+1
            end
        end
    end

    internal = filter(x-> x.first ∉ edge_areas, areas)
    sortedAreas  = sort(collect(internal), by=x->x.second)
    sortedAreas, search_area_size
end

sortedAreas, search_area_size = @time solve(points)

println("Solution 1: ", last(sortedAreas).second)
println("Solution 2: ", search_area_size)
