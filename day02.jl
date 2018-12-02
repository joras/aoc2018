module day2
using Test

function wordsum(word::String)
    hasTwos = false
    hasTrees = false

    bins = Dict{Char, Integer}()
    for letter in word
        count = get!(bins, letter, 0)
        bins[letter] = count + 1
    end

    for bin in bins
        if bin[2] == 2
            hasTwos = true
        end

        if bin[2] == 3
            hasTrees = true
        end

        if hasTwos && hasTrees
            return (true, true)
        end
    end

    (hasTwos, hasTrees)
end

@test wordsum("abcdef") == (false, false)
@test wordsum("bababc") == (true, true)
@test wordsum("abbcde") == (true, false)

function solution1(words)
    sumTwos = 0
    sumTrees = 0
    for word in words
        (hasTwos, hasTrees) = wordsum(word)
        if hasTwos
             sumTwos +=1
         end
        if hasTrees
            sumTrees+=1
        end
    end

    sumTwos * sumTrees
end


function wordDiff(wordA::String, wordB::String)
    numDiffs = 0
    sameChars = ""
    len = max(length(wordA), length(wordB))

    for i in 1:len
        if wordA[i] != wordB[i]
            numDiffs +=1
        else
            sameChars *= wordA[i]
        end
    end

    numDiffs, sameChars
end

@test wordDiff("aaa", "aaa") == (0, "aaa")
@test wordDiff("aaa", "aba") == (1, "aa")
@test wordDiff("bba", "aaa") == (2, "a")

function solution2(words)
    for wordA in words
        for wordB in words
            (count, same) = wordDiff(wordA, wordB)
            if count == 1
                return wordA, wordB, same
            end
        end
    end
end

# use functional style
function solution2v2(words)
    for (wordA, wordB) in Iterators.product(words, words)
        count = Iterators.count(t-> t[1]!=t[2], Iterators.zip(wordA, wordB))
        if count == 1
            return String(
                Iterators.map(p-> p[1],
                    Iterators.filter(p->p[1]==p[2],
                        Iterators.zip(wordA, wordB))))
        end
    end
end


# copied the algorithm of the challenge winner
function solution2v3(words)
    pairs = Set{Pair{String, String}}()

    for word in words
        for i in 1:length(word)-1
            pair = Pair(word[1:i], word[i+2:end] )
            if (pair ∈ pairs)
                return pair.first * pair.second
            end
            push!(pairs, pair)
        end
    end
end

ids = readlines("day02.txt")
println("Solution 1: ", @time solution1(ids))
println("Solution 2: ", @time solution2(ids)[3])
println("Solution 2.2: ", @time solution2v2(ids))
println("Solution 2.3: ", @time solution2v3(ids))
end
