# Python tools for managing MTurk surveys

## `create_hit.py`

Creates a new HIT. Example:

`create_hit.py --html phase_one.html --config hit_configuration_ph1 --number 100 [--sandbox] --title "Brain Phase 1 Survey"`

- `phase_one.html` and `hit_configuration_ph1.yaml` are both in the `templates` directory.
- `--number` are the number of HITs that we want.
- `--sandbox` creates the HIT in the sandbox versus in production.
- `--title` is what the HIT looks like on the MTurk dashboard.

## `get_results.py`

Gets the results from one or more HITs.

`get_results.py --hit_id HIT_ID --output OUTPUT [--sandbox]`

- `--hit_id` is the HIT ID. You can have multiple HIT IDs and it will concatenate the results.
- `--output` is the output .csv file.
- `--sandbox` gets the results from the sandbox as opposed to production.

## `list_hits.py`

Lists the HITs that have been run so far.

`list_hits.py [--sandbox] --output OUTPUT`

- `--output` is the output .csv file.
- `--sandbox` gets the results from the sandbox as opposed to production.

## `list_qualifications.py`

List the qualifications that we've defined so far.

`list_qualifications.py [--output OUTPUT] [--sandbox]`

- `--output` is the output .csv file.
- `--sandbox` gets the results from the sandbox as opposed to production.

## `list_workers_with_qualification.py`

List the workers that fulfill a qualification ID.

`list_workers_with_qualification.py --qualification_id QUALIFICATION_ID --output OUTPUT [--sandbox]`

- `--qualification_id` is the qualification ID.
- `--output` is the output .csv file.
- `--sandbox` gets the results from the sandbox as opposed to production.

# Workflow

- Edit/create a new HTML file in the `templates` directory.
- Edit/create a new configuration file in the `templates` directory.
- Test:
    - Create a new HIT in the sandbox with `create_hit.py` (with `--sandbox`).
    - Test the new HIT in the sandox.
    - Get the new HIT ID using `list_hits.py` (with `--sandbox`).
    - Get the data from the test HIT using `get_results.py` (with `--sandbox`). Make sure it's good.
- Create a new HIT in production with `create_hit.py`. Specify the number of HITs with `--number`.
- Get the HIT ID using `list_hits.py`.
- Get the data from the HIT using `get_results.py`.
- Update worker qualifications (if needed):
    - Use `set_qualifications.py` with the data file to set which workers have completed the survey (if needed)
    - Create a subset of the data file with the HITs that fulfill the requirements for a next phase.
    - Use that subset file with `set_qualifications.py` to set which workers are qualified for a next phase.
- If you need more data, add more instances to the HIT with `create_additional_assignments.py`.