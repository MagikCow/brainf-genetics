import compiler
import random

def generate_random_population(n, chars_of_code):
    valid_symbols = ['+', '-', '>', '<', '.', '[', ']', ' ']
    population = []
    for i in range(n):
        code = ''
        for k in range(chars_of_code):
            code = code + random.choice(valid_symbols)
        population.append(code)

    return population


def rank_population(population, target_output):
    # convert target output to ASCII number
    target_output = [ord(c) for c in target_output]
    scores = []

    for genome in population:
        score = 0
        try:
            result = compiler.compile(genome)  # final output
            result = [ord(c) for c in result]  # ASCII value of result

            # calculate each character in output and subtract from desired output
            # perfect score = 256 for each character
            # currently does not punish too long output - just looks for the target output first

            try:
                for i in range(len(target_output)):
                    score += 256 - abs(result[i] - target_output[i])
                scores.append(score)
            except IndexError:  # output is too short
                scores.append(score)

        except:
            scores.append(0)

    return population, scores


def crossbreed(population, scores):
    new_population = []

    for i in range(int(len(population)/2)):
        top_30 = sorted(scores)[-30:]

        # roulette selection
        total = sum(top_30)

        num1 = random.randint(0,total)
        sum1 = 0

        num2 = random.randint(0,total)
        sum2 = 0

        for item in top_30:
            sum1 += item
            if sum1 >= num1:
                father = population[scores.index(item)]

        for item in top_30:
            sum2 += item
            if sum2 >= num2:
                mother = population[scores.index(item)]


        father = list(father)
        mother = list(mother)

        split = random.randint(1, len(mother))  # character point to split at

        for j in range(split, len(mother)):  # crossbreed mother and father
            mother[j], father[j] = father[j], mother[j]

        mother = ''.join(mother)
        father = ''.join(father)  # list to string

        new_population.append(mother)  # add children to the new population
        new_population.append(father)

    return new_population


# enter chance as a percentage (eg 5 for 5%)
def mutate(population, chance):
    for ix, genome in enumerate(population):  # ix = index in pop, iy = index in genome
        genome = list(genome)

        for iy, char in enumerate(genome):
            num = random.randint(0, 100)  # chance of each character changing

            if num < chance:
                char = random.choice(['+', '-', '>', '<', '.', '[', ']', ' '])
                genome[iy] = char

        genome = ''.join(genome)
        population[ix] = genome

    return population



pop = generate_random_population(500, 50)

for k in range(5000):
    pop = mutate(pop, 10)
    pop, scores = rank_population(pop, 'hi')
    pop = crossbreed(pop, scores)

    if k % 5 == 0:
        print(k)
        print(sorted([x for x in scores if x != 0]))
        print(pop[scores.index(max(scores))])

pop, scores = rank_population(pop, 'hi')
print(pop[scores.index(max(scores))])
print(compiler.compile(pop[scores.index(max(scores))]))
print('--------------- ENDS ---------------')
