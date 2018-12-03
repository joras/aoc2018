using Test


function solution(lines)
    tiles = Dict()
    pureclaims = BitSet()

    for line in lines
        id,x,y,h,w = map(x->parse(Int64, x.match), eachmatch(r"\d+", line))
        push!(pureclaims, id)

        for xi in x:x+h-1
            for yi in y:y+w-1
                pos = Pair(xi, yi)

                if haskey(tiles, pos)
                    delete!(pureclaims, id)
                    tile = tiles[pos]

                    if tile != "X"
                        delete!(pureclaims, tile)
                        tiles[pos] = "X"
                    end
                else
                    tiles[pos] = id
                end
            end
        end
    end

    @assert length(pureclaims) == 1
    count(x->x=="X", values(tiles)), first(pureclaims)
end


function solutionArr(lines)
    tiles = Array{Union{Int16, Nothing}}(nothing, 1000, 1000)
    pureclaims = BitSet()

    for line in lines
        id,x,y,h,w = map(x->parse(Int16, x.match), eachmatch(r"\d+", line))
        push!(pureclaims, id)

        for xi in x:x+h-1
            for yi in y:y+w-1
                tile = tiles[xi+1, yi+1]

                if tile != nothing
                    delete!(pureclaims, id)

                    if tile != -1
                        delete!(pureclaims, tile)
                        tiles[xi+1, yi+1] = -1
                    end
                else
                    tiles[xi+1, yi+1] = id
                end
            end
        end
    end

    @assert length(pureclaims) == 1
    count(x->x== -1, values(tiles)), first(pureclaims)
end

@test solution(["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]) == (4, 3)
@test solutionArr(["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]) == (4, 3)


println("Solution ", @time solution(readlines("day03.txt")))
println("Solution with arrays: ", @time solutionArr(readlines("day03.txt")))
