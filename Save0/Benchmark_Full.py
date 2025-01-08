def benchmark_all(benchGoal):
    grass_benchmark(benchGoal)
    wood_benchmark(benchGoal)
    pumpkin_benchmark(benchGoal)
    maze_benchmark(benchGoal)
    carrot_benchmark(benchGoal)
    polyculture_benchmark(benchGoal)
    sunflower_benchmark(benchGoal)
    cactus_benchmark(benchGoal)
    #dinosaur_benchmark(benchGoal)
    #map_benchmark(benchGoal)

clear()
benchmark_all(1000)