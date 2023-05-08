import matplotlib.pyplot as plt

# draw a graph of fitness over generations where the axis are labelled
def draw_graph(fitness):
    plt.plot(fitness)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness over generations')
    plt.show()
