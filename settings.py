probability_ageing = 0.0125                     # happens on average every 40 steps - a whale becomes old if it is over 40
juvenile_survival = 0.964                       # chance a juvenile survives the year
adult_survival = 0.981                          # chance an adult survives the year
initial_chance_of_birth = 0.06
basic_chance_of_birth = 0.05

young_chance_of_birth = 0.03                    # used when mate choice is implemented; chance of a young whale reproducing
old_chance_of_birth = 0.07                      # used when mate choice is implemented; chance of a old whale reproducing

initial_probability_nonreproductive = 0.01
inherited_probability_nonreproductive = 0.05
steps = 10000

# Survival benefits of older females
# Values represent an x-fold increase in chance of survival
survival_benefit_of_mother_daughter = 5.4
survival_benefit_of_mother_son = 8.7
survival_benefit_of_granny_grandaughter = 1.5
survival_benefit_of_granny_grandson = 1.1

# Reproductive benefits of older females
# Values represent an x-fold increase in chance of reproduction
reproductive_benefit_of_mother_daughter = 1
reproductive_benefit_of_mother_son = 1
reproductive_benefit_of_granny_grandaughter = 1
reproductive_benefit_of_granny_grandson = 1