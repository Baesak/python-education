from data_structures import Queue


def test_dequeue_enqueue(values_list):

    queue = Queue(5, {}, [])
    queue.enqueue("sa")
    queue.enqueue(())

    result = [value for value in queue]

    assert result == values_list
    assert len(queue) == 0
