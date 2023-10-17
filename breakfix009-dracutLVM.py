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
            steps.run_command(
                label="Configuring " + _servera,
                hosts=[_servera],
                command='''
                pvcreate /dev/vdb;
                vgcreate vg01 /dev/vdb;
                lvcreate -L 800M -n lv01 vg01;
                mkfs.xfs /dev/vg01/lv01;
                mkdir /mnt/data;
                mount /dev/vg01/lv01 /mnt/data;
                echo '/dev/vg01/lv01 /mnt/data  xfs  defaults 0 0' | sudo  tee -a /etc/fstab;
                sed  -i '130i      filter=["r|.*/|"]' /etc/lvm/lvm.conf;
                dracut -f  &>> /dev/null;
                touch /var/tmp/.kc1;
                ''',
                shell=True,
            ),
        ]
        userinterface.Console(items).run_items(action="Starting")

    def fix(self):
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
            steps.run_command(
                label="Configuring " + _servera,
                hosts=[_servera],
                command='''
                umount /mnt/data;
                rm -rf /mnt/data;
                egrep -v -e 'filter=\["r\|.*/|"\]' /etc/lvm/lvm.conf > /tmp/lvm.conf && mv -f /tmp/lvm.conf /etc/lvm/lvm.conf;
                dracut -fv /boot/initramfs-3.10.0-957.el7.x86_64.img 3.10.0-957.el7.x86_64;
                lvremove -f /dev/vg01/lv01;
                vgremove vg01;
                pvremove /dev/vdb;
                sed -i "$d" /etc/fstab;
                ''',
                shell=True,
            ),
        ]
        userinterface.Console(items).run_items(action="Un-done")
        
    def grade(self):
        """
        Perform evaluation steps on the system
        """
        items = [
            {
                "label": "Checking lab systems",
                "task": labtools.check_host_reachable,
                "hosts": _targets,
                "fatal": True,
            },
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command="[ ! -z $(systemctl list-units --type target --state active | grep -o $(systemctl get-default)) ]",
                returns="0",
                shell=True,
            ),
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command="[ ! -z $(lsinitrd | grep ^lvm) ]",
                returns="0",
                shell=True,
            ),
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command='''dracut -fv /tmp/test.img $(awk '/^menuentry.*{/,/^}/' /boot/grub2/grub.cfg | awk -vRS="\n}\n" -vDEFAULT="$((default+1))" 'NR==DEFAULT' | grep -o '/vmlinuz-.*' | awk '{print $1}' | cut -c 10-) &> /tmp/test.dracut ; [ ! -z $(grep -o "Including module: lvm" /tmp/test.dracut | sort -u | awk '{print $3}') ]''',
                returns="0",
                shell=True,
            ),
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command='''[ -z $(lvs 2>&1 | grep -o rejected | sort -u) ]''',
                returns="0",
                shell=True,
            ),
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command='''[ -z $(grep -Ev "^[[:space:]]*#|^$|^[[:space:]]*;" /etc/lvm/lvm.conf | grep -o volume_list) ] || [ ! -z $(grep -Ev "^[[:space:]]*#|^$|^[[:space:]]*;" /etc/lvm/lvm.conf | grep volume_list | grep -o $(lvs | awk '$1~"root"{print $2}')) ]''',
                returns="0",
                shell=True,
            ),
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command='''[ $(awk '/^menuentry.*{/,/^}/' /boot/grub2/grub.cfg | awk -vRS="\n}\n" -vDEFAULT="$((default+1))" 'NR==DEFAULT' | grep -o '/vmlinuz-.*' | awk '{print $1}' | cut -c 10-) == $(uname -a | awk '{print $3}') ]''',
                returns="0",
                shell=True,
            ),
            steps.run_command(
                label="Verifying lab system " + _servera,
                hosts=[_servera],
                command='''grep "filter = [ "r|.*/|" ]" /etc/lvm/lvm.conf &>> /dev/null''',
                returns="0",
                shell=True,
            ),
        ]
        ui = userinterface.Console(items)
        ui.run_items(action="Grading")
        ui.report_grade()

    def finish(self):
        items = []
        userinterface.Console(items).run_items(action="Finishing")
