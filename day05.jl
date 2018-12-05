using Test

function react(input)
    chain = collect(input)
    newchain = Char[]

    for curr in input
        if isempty(newchain)
            push!(newchain, curr)
        else
            prev = last(newchain)
            if abs(curr - prev) == 32
                pop!(newchain)
            else
                push!(newchain, curr)
            end
        end
    end

    String(newchain)
end

function solution2(input)
    lengths = []

    for char in 'a':'z'
        filtered = filter(x->x!=char && x!=char-32, input)
        push!(lengths, length(solution1(filtered)) )
    end

    minimum(lengths)
end

@test react("dabAcCaCcCaABAcCcaDA") == "dabCBAcaDA"#

data = readline("day05.txt")
println("Solution1: ", @time length(react(data)))
println("Solution1: ", @time solution2(data))
