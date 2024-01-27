from models.aoc_2018 import PlantAutomaton


def test_plant_automaton_keeps_track_of_which_plants_are_alive():
    plant_automaton = PlantAutomaton(
        rules={
            (1, 1, 0, 1, 1): 1,
            (0, 0, 0, 1, 1): 1,
        },
        initial_state={0, 1, 2, 4, 5},
    )
    assert plant_automaton.plants_alive(generation=0) == {0, 1, 2, 4, 5}
    assert plant_automaton.plants_alive(generation=1) == {-1, 3}
    assert plant_automaton.plants_alive(generation=2) == set()
