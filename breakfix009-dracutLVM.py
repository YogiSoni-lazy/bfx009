#
# Copyright (c) 2020 Red Hat Training <training@redhat.com>
#
# All rights reserved.
# No warranty, explicit or implied, provided.

from labs import labconfig
from labs.grading import Default
from labs.common import steps, labtools, userinterface

SKU = labconfig.get_course_sku().upper()

_targets = ["servera"]
_servera = "servera"

class Breakfix009Dracutlvm(Default):
    __LAB__ = "breakfix009-dracutLVM"

    def start(self):
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
        userinterface.Console(items).run_items(action="Starting")

    def grade(self):
        items = []
        ui = userinterface.Console(items)
        ui.run_items(action="Grading")
        ui.report_grade()

    def finish(self):
        items = []
        userinterface.Console(items).run_items(action="Finishing")
