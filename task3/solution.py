
def get_events_time(intervals):
    """Получает список всех событий (вход/выход) с указанием типа события.
    """
    events = []
    for i in range(0, len(intervals), 2):
        events.append((intervals[i], 'start'))
        events.append((intervals[i + 1], 'end'))
    return events


def calculate_overlap(lesson: list[int, str], pupil: list[int, str], tutor: list[int, str]):
    """Рассчитывает общее время пересечения урока, ученика и учителя
    """
    times = get_events_time(lesson) + get_events_time(pupil) + get_events_time(tutor)
    times.sort()

    lesson_active = pupil_active = tutor_active = 0
    overlap_time = 0
    last_time = 0

    for time, event in times:
        if lesson_active > 0 and pupil_active > 0 and tutor_active > 0:
            overlap_time += time - last_time

        match event:
            case "start":
                if time in lesson:
                    lesson_active += 1
                elif time in pupil:
                    pupil_active += 1
                elif time in tutor:
                    tutor_active += 1
            case "end":
                if time in lesson:
                    lesson_active -= 1
                elif time in pupil:
                    pupil_active -= 1
                elif time in tutor:
                    tutor_active -= 1
            case _:
                return

        last_time = time

    return overlap_time


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']
    return calculate_overlap(lesson, pupil, tutor)


tests = [
    {
        'intervals': {
            'lesson': [
                1594663200,
                1594666800
            ],
            'pupil': [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472
            ],
            'tutor': [
                1594663290,
                1594663430,
                1594663443,
                1594666473
            ]
        },
        'answer': 3117
    },
    {
        'intervals': {
            'lesson': [
                1594702800,
                1594706400
            ],
            'pupil': [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641
            ],
            'tutor': [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463
            ]
        },
        'answer': 3577
    },
    {
        'intervals': {
            'lesson': [
                1594692000,
                1594695600
            ],
            'pupil': [
                1594692033,
                1594696347
            ],
            'tutor': [
                1594692017,
                1594692066,
                1594692068,
                1594696341
            ]
        },
        'answer': 3565
    },
]

def main():
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print("Все тесты пройдены!")


if __name__ == '__main__':
    main()