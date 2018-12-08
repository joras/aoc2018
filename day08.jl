using Test

data = map(x->parse(Int16, x), split(readline("day08.txt"), " "))

struct Node
    metadata::Array{Int16}
    children::Array{Node}
    length::Int32
end

function parseNode(data)
    childno = data[1]
    metalen = data[2]

    rdata = data[3: end]

    childlen = 0
    children = []

    for i in 1:childno
        child = parseNode(rdata[childlen+1:end])
        push!(children, child)
        childlen += child.length
    end

    metadata = rdata[childlen+1: childlen+metalen]
    return Node(metadata, children, metalen+childlen+2)
end


function solution1(node)
    res = 0

    for child in node.children
        res+= solution1(child)
    end

    res+=sum(node.metadata)
end


function solution2(node)
    res = 0

    if isempty(node.children)
        res+= sum(node.metadata)
    else
        for childIdx in node.metadata
            if childIdx in 1:length(node.children)
                res+= solution2(node.children[childIdx])
            else
                res+=0
            end
        end
    end

    res
end


@test solution1(parseNode([2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2])) == 138
@test solution2(parseNode([2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2])) == 66

nodeTree = parseNode(data)

println("solution 1 ", @time solution1(nodeTree))
println("solution 2 ", @time solution2(nodeTree))
