using Test

function loadFile(fileName::String)
    numbers = Array{Integer, 1}()
    open(fileName) do file
        for line in eachline(file)
            push!(numbers, parse(Int64, line))
        end
    end

    numbers
end

function solution2(data:: Array{Integer, 1})
    curSum = 0;
    prevSums = BitSet([0])

    while true
        for currInt in data
            curSum += currInt;

            if (curSum ∈ prevSums)
                return curSum
            end

            push!(prevSums, curSum)
        end
    end
end

@test solution2([+1, -1] ) == 0
@test solution2([+3, +3, +4, -2, -4]) == 10
@test solution2([-6, +3, +8, +5, -6 ]) == 5
@test solution2([+7, +7, -2, -7, -4]) == 14

integers = loadFile("day01.txt")
solution1 = sum

println("Solution 1: ", @time solution1(integers))
println("Solution 2: ", @time solution2(integers))
