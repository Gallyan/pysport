import logging

from . import memory
from .result_checker import ResultChecker


def find_person_by_result(system_id, result):
    assert result, memory.Result
    number = str(result.card_number)
    for person in memory.race().persons:
        if person.card_number == number:
            result.person = person

            return True

    return False


def add_result(system_id, result):
    """
    :type system_id: str
    :type result: memory.Result
    """
    assert result, memory.Result
    if isinstance(result.person, memory.Person):
        result.status = memory.ResultStatus.OK
        if len(result.punches):
            checker = ResultChecker(result.person)
            if not checker.check_result(result):
                result.status = memory.ResultStatus.DISQUALIFIED

        result.person.result = result
        memory.race().results.append(result)

        logging.debug(result.status)
    else:
        res = find_person_by_result(system_id, result)
        if res:
            add_result(system_id, result)
        else:
            memory.race().results.insert(0, result)
