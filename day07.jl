rules = []
allsteps = Set()

# in case you randomly find this code
# this is really ugly, dont look at it, nothing to learn here

for line in readlines("day07.txt")
    m = match(r"Step (.) must be finished before step (.) can begin.", line)
    push!(rules, (string(m[1]), string(m[2])))
    push!(allsteps, m[1])
    push!(allsteps, m[2])
end

function solve1(allsteps, rules)
    orderedsteps = []
    remainingsteps = Set(allsteps)

    while true
        nextsteps = filter(s->findfirst(x->x[2]==s && x[1] ∉ orderedsteps, rules) == nothing, remainingsteps)

        if !isempty(nextsteps)
            s = first(sort(collect(nextsteps)))
            push!(orderedsteps, s)
            delete!(remainingsteps, s )
        else
            break
        end
    end

    reduce(*, orderedsteps )
end

struct Work
    item:: String
    endtime:: Int32
end

function solve2(allsteps, rules)
    workingelves = Set()
    donesteps = Set()
    remainingsteps = Set(allsteps)

    ELVES = 5
    itemweight(item) = (60 + item[1]-'A'+1)
    #itemweight(item) = (item[1]-'A'+1)

    time = 0
    while true
        donework = filter(w->w.endtime == time, workingelves)
        for work in donework
            delete!(workingelves, work)
            push!(donesteps, work.item)
            delete!(remainingsteps, work.item )
        end

        function canWorkOn(step)
            hasRule = findfirst(x->x[2] == step && x[1] ∉ donesteps, rules) == nothing
            isWorking = findfirst(w->step==w.item, collect(workingelves)) != nothing
            hasRule && !isWorking
        end

        nextsteps = sort(collect(filter(canWorkOn, remainingsteps)))


        if !isempty(nextsteps)
            # assign work
            for i in 1: ELVES - length(workingelves)
                if !isempty(nextsteps)
                    nextitem = popfirst!(nextsteps)
                    newitem = Work(nextitem, time + itemweight(nextitem))
                    push!(workingelves, newitem)
                end
            end
        else
            if isempty(workingelves)
                break
            end
        end

        time+=1
    end

    time
end


println("Solution1: ", solve1(allsteps, rules))
println("Solution2: ", solve2(allsteps, rules))
