from data_structures import Graph
import pytest


@pytest.fixture
def filled_graph(values_list):

    graph = Graph()

    graph.insert(values_list[0])
    graph.insert(values_list[1], graph.lookup(values_list[0]))
    graph.insert(values_list[2], graph.lookup(values_list[1]))

    return graph


def test_insert(filled_graph):

    result = [value for value in filled_graph]
    expected_peaks_data = [5, {}, []]
    expected_peaks_connections = [[{}], [5, []], [{}]]
    peaks = [node.data for node in filled_graph]
    connections = [peak.connections for peak in peaks]

    for peak, value, in zip(peaks, expected_peaks_data):
        assert peak == value

    # Check values of every peak in each peak connections list.
    for linked_list, lst in zip(connections, expected_peaks_connections):
        for node, value in zip(linked_list, lst):
            assert node.data.data == value


def test_lookup(filled_graph):

    peak = filled_graph.peaks_linked_list[1].data
    assert peak == filled_graph.lookup({})


def test_insert_wrong_data(filled_graph):

    with pytest.raises(ValueError):
        filled_graph.insert(2)
        filled_graph.insert("asf")
        filled_graph.insert({})
        filled_graph.insert(1, Graph.Peak(2))


def test_delete(filled_graph):

    delete_peak = filled_graph.lookup({})
    filled_graph.delete(delete_peak)
    peaks = [node.data for node in filled_graph.peaks_linked_list]

    with pytest.raises(ValueError):
        filled_graph.lookup(delete_peak)

    for peak in peaks:
        with pytest.raises(ValueError):
            peak.connections.lookup(delete_peak)




