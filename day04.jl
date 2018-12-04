function sleepmap(input)
    sleepminutes = Dict()
    currGuard = nothing
    sleepStart = nothing
    sleepEnd = nothing

    for actionRow in sort(collect(input), by=x->x[1])
        minutes, action = actionRow.second

        if startswith(action, "Guard")
            m = match(r"Guard #(\d+) begins shift", action)

            # fill sleep until the end of the hour of previous guard
            if (currGuard != nothing && sleepStart!= nothing && sleepEnd == nothing)
                for min in sleepStart+1:60
                    sleepStat[min] = sleepStat[min] + 1
                end
            end

            # create empty sleep stats for the guard
            currGuard = parse(Int16, m[1])
            if !haskey(sleepminutes, currGuard)
                sleepminutes[currGuard] = zeros(Int16, 60)
            end

            sleepStart = nothing
            sleepEnd = nothing

        elseif startswith(action, "wakes")
            sleepEnd = minutes
            sleepStat = sleepminutes[currGuard]

            # fill sleep range stats
            for min in sleepStart+1:sleepEnd
                sleepStat[min] = sleepStat[min] + 1
            end
        elseif startswith(action, "falls")
            sleepStart = minutes
            sleepEnd = nothing
        end

    end

    sleepminutes
end


function solution1(sleepmap)
    sleepy = sort(
            map(x->(x.first,
                sum(x.second),
                 findmax(x.second)[2]),
                  collect(sleeps)),
            by=x->x[2],
            rev=true)[1]

    sleepy[1] * (sleepy[3]-1)
end

function solution2(sleepmap)
    sleepy = sort(
            map(x->(x.first,findmax(x.second)), collect(sleeps)),
            by=x->x[2][1],
            rev=true)[1]

    sleepy[1] * (sleepy[2][2] - 1)
end

actions = Dict()
for row in readlines("day04.txt")
    m = match(r"\[((.+) .+:(.+))\] (.+)", row)
    actions[m[1]] = (parse(Int8,m[3]), m[4])
end

sleeps = sleepmap(actions)

println("solution1 ",  @time solution1(sleeps))
println("solution2 ",  @time solution2(sleeps))
