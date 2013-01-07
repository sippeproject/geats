import re

class SysStat(object):
    RE_MEMINFO = re.compile("(.*?):\s+(.*?)( kB)?$")
    RE_STAT = re.compile("(.*?)\s(.+)")
    RE_CPUINFO = re.compile("(.*?)\s*:\s*(.*)")

    def __init__(self):
        self.meminfo = meminfo = {}
        for line in open("/proc/meminfo"):
            m = SysStat.RE_MEMINFO.match(line)
            if m:
                meminfo[m.group(1)] = m.group(2)

        self.vmstat = vmstat = {}
        for line in open("/proc/vmstat"):
            m = SysStat.RE_STAT.match(line)
            if m:
                vmstat[m.group(1)] = m.group(2)

        self.stat = stat = {}
        for line in open("/proc/stat"):
            m = SysStat.RE_STAT.match(line)
            if m:
                stat[m.group(1)] = m.group(2)

        cpuflags = {}
        cpucount = 0
        cpuinfo = {}
        for line in open("/proc/cpuinfo"):
            m = SysStat.RE_CPUINFO.match(line)
            if m:
                cpuinfo[m.group(1)] = m.group(2)
            elif line.strip() == "":
                break
        self.cpuinfo = {
            "flags": cpuinfo.get("flags", "").split(" "),
            "cores": cpuinfo.get("cpu cores", 0),
            "siblings": cpuinfo.get("siblings", 0),
            "vendor_id": cpuinfo.get("vendor_id", 0),
            "model name": cpuinfo.get("model name", ""),
            "cache size": cpuinfo.get("cache size", ""),
        }

    @property
    def swaptotal(self):
        return int(self.meminfo['SwapTotal'])

    @property
    def swapfree(self):
        return int(self.meminfo['SwapFree'])

    @property
    def swapused(self):
        return self.swaptotal - self.swapfree

    @property
    def memtotal(self):
        return int(self.meminfo['MemTotal'])

    @property
    def memfree(self):
        return int(self.meminfo['MemFree'])

    @property
    def memused(self):
        return self.memtotal - self.memfree

    @property
    def membuffers(self):
        return int(self.meminfo['Buffers'])

    @property
    def memcached(self):
        return int(self.meminfo['Cached'])

if __name__ == "__main__":
    import pprint
    ss = SysStat()
    pprint.pprint({
        "cpuinfo": ss.cpuinfo,
        "meminfo": ss.meminfo,
        "stat": ss.stat,
        "vmstat": ss.vmstat,
    })
