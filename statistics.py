import parse
from runner.examine import Examiner, latest_log


# define a metric parser for each directory (experiment)
def get_acc(output_dir, experiment, _):
    # Each parser follows the same signature
    # It can read/write to a global cache dict `caches`,
    # and read/write each experiment:
    # collections.namedtuple("Experiment", ["cache", "metric", "param"])
    log = latest_log("test", output_dir)
    if log is None:
      return
    with open(log, 'r') as f:
      content = ''.join(f.readlines())
    results = parse.search("* Acc@1 {acc1:g}", content)
    experiment.metric["Acc@1"] = results['acc1'] if results is not None and 'acc1' in results else None


def _main():
  examiner = Examiner()  # container for parsed results
  # register parser for each directory (experiment)
  examiner.add(get_acc)
  # run all parsers for directories matched by regex
  examiner.exam(output="output", regex=".*")
  # print the tsv table with all (different) params and metrics of each experiment
  examiner.table()

if __name__ == '__main__':
  _main()