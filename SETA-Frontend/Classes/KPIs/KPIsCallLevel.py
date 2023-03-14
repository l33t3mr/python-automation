from .KPIsReportLevel import KPIsReportLevel


class KPIsCallLevel(KPIsReportLevel):
    def __init__(self, driver, obj):
        self.driver = driver
        self.initialize_attributes()
        self.obj = obj
        if not isinstance(obj, KPIsReportLevel):
            raise TypeError("Object passed must be an instance of KPIsReportLevel")

        # print("Init Sub class {} - Report Name {}, Report ID {}, Call ID {}".format(__class__.__name__,self.report_name, self.report_id, self.call_id))

    def _open(self):
        self.report_name = self.obj.report_name
        self.report_id = self.obj.report_id
        self.open_call_level()
        self._buffer_call_id()
