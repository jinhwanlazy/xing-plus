from xing.xaquery import Query as _Query
from xing.logger import Logger
from xing.tr import TR
from xing import tr
log = Logger(__name__)


def _keep_requester_unique(cls):
    instances = {}

    def getinstance(query):
        if query in tr.trname2code:
            query = tr.trname2code[query]
        if query not in tr.queries:
            log.critical("request not defined", query)
            raise KeyError()
        if query not in instances:
            instances[query] = cls(query)
        return instances[query]
    return getinstance


@_keep_requester_unique
class Query:
    def __init__(self, trcode):
        self.query = _Query(trcode)
        self.tr = TR(trcode)

    def help(self):
        print("Inputs:")
        print(self.tr.input_dataframe())

    def send(self, **args):
        return self.query.request(self.tr.in_blocks(**args), self.tr.out_blocks())
