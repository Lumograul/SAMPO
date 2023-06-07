from uuid import uuid4

from fixtures import *
from sampo.scheduler.heft.base import HEFTScheduler
from sampo.utilities.validation import validate_schedule
from sampo.schemas.resources import Worker


def test_convert_schedule_to_chromosome(setup_toolbox, setup_wg, setup_contractors):
    tb, _ = setup_toolbox

    schedule = HEFTScheduler().schedule(setup_wg, setup_contractors, validate=True)

    chromosome = tb.schedule_to_chromosome(schedule=schedule)
    assert tb.validate(chromosome)


def test_convert_chromosome_to_schedule(setup_toolbox, setup_contractors, setup_wg):
    tb, _ = setup_toolbox

    chromosome = tb.generate_chromosome()
    schedule, _, _, _ = tb.chromosome_to_schedule(chromosome)
    schedule = Schedule.from_scheduled_works(schedule.values(), setup_wg)

    validate_schedule(schedule, setup_wg, setup_contractors)


def test_converter_with_borders_contractor_accounting(setup_toolbox, setup_contractors, setup_wg):
    tb, _ = setup_toolbox

    chromosome = tb.generate_chromosome()

    for contractor_index in range(len(chromosome[2])):
        for resource_index in range(len(chromosome[2][contractor_index])):
            chromosome[1][:, resource_index] = chromosome[1][:, resource_index] / 2
            chromosome[2][contractor_index, resource_index] = max(chromosome[1][:, resource_index])

    schedule, _, _, _ = tb.chromosome_to_schedule(chromosome)
    workers = list(setup_contractors[0].workers.keys())

    contractors = []
    for i in range(len(chromosome[2])):
        contractors.append(Contractor(id=setup_contractors[i].id,
                                      name=setup_contractors[i].name,
                                      workers={name: Worker(str(uuid4()), name, count, contractor_id=setup_contractors[i].id)
                                               for name, count in zip(workers, chromosome[2][i])},
                                      equipments={}))

    schedule = Schedule.from_scheduled_works(schedule.values(), setup_wg)

    validate_schedule(schedule, setup_wg, contractors)
