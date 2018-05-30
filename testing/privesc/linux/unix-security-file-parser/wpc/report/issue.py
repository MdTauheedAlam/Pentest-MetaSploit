import wpc.conf
import string

import xml.etree.cElementTree as etree
def stripit(s):
	s = filter(lambda x: x in string.printable, s)
	s = filter(lambda x: ord(x) != 11, s)
	s = filter(lambda x: ord(x) != 12, s)
	return s

class issue:
    def __init__(self, identifier):
        self.id = identifier
        self.sdcount = {}
        self.supporting_data = {}

    def add_supporting_data(self, k, v):
        #print "ADD called"
        if not k in self.supporting_data.keys():
            self.supporting_data[k] = []
            self.sdcount[k] = 0
        self.supporting_data[k].append(v)
        self.sdcount[k] = self.sdcount[k] + 1

    def count_supporting_data(self, k):
        #print "ADD called"
        if not k in self.supporting_data.keys():
            return None
        return self.sdcount[k]

    def get_id(self):
        return self.id

    def render_supporting_data(self, data_name):
        # expect an array of issue.fileAcl type for now
        d = etree.Element('supporting_data')
        if data_name == 'principals_with_service_perm':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                p = data[1]
                etree.SubElement(d, 'data').text = stripit("    %s (%s) which runs as %s has permission granted for: %s\n" % (s.get_description(), s.get_name(), s.get_run_as(), p.get_fq_name()))

        elif data_name == 'text_line':
            for data in self.get_supporting_data(data_name):
                k = data[0]
                l = data[1]
                etree.SubElement(d, 'data').text = stripit("%s\n" % (l))

        elif data_name == 'principals_with_service_ownership':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                p = data[1]
                etree.SubElement(d, 'data').text = stripit("    %s (%s) which runs as %s is owned by %s\n" % (s.get_description(), s.get_name(), s.get_run_as(), p.get_fq_name()))

        elif data_name == 'writable_dirs':
            for data in self.get_supporting_data(data_name):
                f = data[0]
                a = data[1]
                etree.SubElement(d, 'data').text = stripit("    File %s has weak permissions: %s\n" % (f.get_name(), a.as_text()))

        elif data_name == 'writable_progs':
            for data in self.get_supporting_data(data_name):
                f = data[0]
                a = data[1]
                etree.SubElement(d, 'data').text = stripit("    File %s has weak permissions: %s\n" % (f.get_name(), a.as_text()))

        elif data_name == 'service_exe_write_perms':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                f = data[1]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs the following program as %s:\n" % (s.get_description(), s.get_name(), s.get_run_as()))
                etree.SubElement(d, 'data').text = stripit("  %s\n" % (f.as_text()))

        elif data_name == 'file_untrusted_ownership':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs %s as %s.  Program owned by %s\n" % (s.get_description(), s.get_name(), s.get_exe_file().get_name(), s.get_run_as(), s.get_exe_file().get_sd().get_owner().get_fq_name()))

        elif data_name == 'service_exe_parent_dir_untrusted_ownership':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                f = data[1]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs %s as %s.  Parent directory %s is owned by %s\n" % (s.get_description(), s.get_name(), s.get_exe_file().get_name(), s.get_run_as(), f.get_name(), f.get_sd().get_owner().get_fq_name()))

        elif data_name == 'service_exe_file_parent_write_perms' or data_name == 'service_exe_parent_grandparent_write_perms':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                f = data[1]
                fp = data[2]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs %s as %s" % (s.get_description(), s.get_name(), s.get_exe_file().get_name(), s.get_run_as()))
                etree.SubElement(d, 'data').text = stripit("  %s\n" % (f.as_text()))
                etree.SubElement(d, 'data').text = stripit("  %s\n" % (fp.as_text()))

        elif data_name == 'service_exe_parent_dir_perms':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                f = data[1]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs %s as %s\n" % (s.get_description(), s.get_name(), s.get_exe_file().get_name(), s.get_run_as()))
                etree.SubElement(d, 'data').text = stripit("  %s\n" % (f.as_text()))

        elif data_name == 'service_exe_regkey_untrusted_ownership':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                r = data[1]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) uses registry key %s, owned by %s" % (s.get_description(), s.get_name(), r.get_name(), r.get_sd().get_owner().get_fq_name()))

        elif data_name == 'regkey_untrusted_ownership':
            for data in self.get_supporting_data(data_name):
                r = data[0]
                etree.SubElement(d, 'data').text = stripit("Registry key %s is owned by %s" % (r.get_name(), r.get_sd().get_owner().get_fq_name()))

        elif data_name == 'service_reg_perms':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                a = data[1]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) uses registry key %s:\n" % (s.get_description(), s.get_name(), a.get_name()))
                etree.SubElement(d, 'data').text = stripit("  %s\n" % (a.as_text()))

        elif data_name == 'regkey_perms':
            for data in self.get_supporting_data(data_name):
                r = data[0]
                a = data[1]
                etree.SubElement(d, 'data').text = stripit("Registry key %s has permissions:\n" % (r.get_name()))
                etree.SubElement(d, 'data').text = stripit("  %s\n" % (a.as_text()))

        elif data_name == 'service_info':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs as %s and has path: %s:\n" % (s.get_description(), s.get_name(), s.get_run_as(), s.get_exe_path()))

        elif data_name == 'service_domain_user':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs as %s\n" % (s.get_description(), s.get_name(), s.get_run_as()))

        elif data_name == 'service_no_exe':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) tries to run '%s' as %s\n" % (s.get_description(), s.get_name(), s.get_exe_path(), s.get_run_as()))

        elif data_name == 'service_dll':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                r = data[1]
                f = data[2]
                etree.SubElement(d, 'data').text = stripit(" Service %s (%s) runs as %s: Regkey %s references %s which has weak file permissions (TODO how so?)\n" % (s.get_description(), s.get_name(), s.get_run_as(), r.get_name(), f.get_name()))

        elif data_name == 'regkey_ref_replacable_file':
            for data in self.get_supporting_data(data_name):
                keytype = data[0]
                name = data[1]
                clsid = data[2]
                f = data[3]
                r = data[4]
                etree.SubElement(d, 'data').text = stripit(" %s \"%s\" uses CLSID %s which references the following file with weak permissions: %s [defined in %s] - TODO how are perms weak?\n" % (type, name, clsid, f.get_name(), r.get_name()))

        elif data_name == 'regkey_ref_file':
            for data in self.get_supporting_data(data_name):
                r = data[0]
                v = data[1]
                f = data[2]
                etree.SubElement(d, 'data').text = stripit(" %s references %s which has weak permissions.  TODO weak how?\n" % (r.get_name() + "\\" + v, f.get_name()))

        elif data_name == 'sectool_services':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s (%s) runs '%s' as %s\n" % (s.get_description(), s.get_name(), s.get_exe_path(), s.get_run_as()))

        elif data_name == 'sectool_files':
            for data in self.get_supporting_data(data_name):
                f = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s\n" % (f.get_name()))

        elif data_name == 'file_read':
            for data in self.get_supporting_data(data_name):
                f = data[0]
                u = data[1]
                etree.SubElement(d, 'data').text = stripit(" %s can be read by %s\n" % (f.get_name(), u.get_fq_name()))

        elif data_name == 'process_exe':
            for data in self.get_supporting_data(data_name):
                p = data[0]
                etree.SubElement(d, 'data').text = stripit(" Process ID %s (%s) as weak permissions.  TODO: Weak how?\n" % (p.get_pid(), p.get_exe().get_name()))

        elif data_name == 'user_powerful_priv':
            for data in self.get_supporting_data(data_name):
                u = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s\n" % (u.get_fq_name()))

        elif data_name == 'group_powerful_priv':
            for data in self.get_supporting_data(data_name):
                u = data[0]
                etree.SubElement(d, 'data').text = stripit(" %s\n" % (u.get_fq_name()))

        elif data_name == 'share_perms':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                u = data[1]
                etree.SubElement(d, 'data').text = stripit(" Share %s (%s) is accessible by %s\n" % (s.get_name(), s.get_description(), u.get_fq_name()))

        elif data_name == 'writable_eventlog_dll' or data_name == 'writable_eventlog_file':
            for data in self.get_supporting_data(data_name):
                s = data[0]
                f = data[1]
                etree.SubElement(d, 'data').text = stripit(" Registry key %s refers to replaceable file %s TODO print file perms?\n" % (s.get_name(), f.get_name()))

        elif data_name == 'drive_and_fs_list':
            for data in self.get_supporting_data(data_name):
                drive = data[0]
                etree.SubElement(d, 'data').text = stripit(" Drive %s has %s filesystem\n" % (drive.get_name(), drive.get_fs()))

        elif data_name == 'dir_add_file':
            for data in self.get_supporting_data(data_name):
                drive = data[0]
                a = data[1]
                etree.SubElement(d, 'data').text = stripit(" Drive %s allows %s to add files\n" % (drive.get_name(), a.get_principal().get_fq_name()))

        elif data_name == 'dir_add_dir':
            for data in self.get_supporting_data(data_name):
                drive = data[0]
                a = data[1]
                etree.SubElement(d, 'data').text = stripit(" Drive %s allows %s to add directories\n" % (drive.get_name(), a.get_principal().get_fq_name()))

        elif data_name == 'process_dll':
            for data in self.get_supporting_data(data_name):
                p = data[0]
                dll = data[1]
                if p.get_exe():
                    exe = p.get_exe().get_name()
                else:
                    exe = "[unknown]"
                etree.SubElement(d, 'data').text = stripit(" Process ID %s (%s) uses DLL %s.  DLL has weak permissions.  TODO: Weak how?\n" % (p.get_pid(), p.get_exe().get_name(), dll.get_name()))

        elif data_name == 'process_perms':
            for data in self.get_supporting_data(data_name):
                p = data[0]
                perms = data[1]
                if p.get_exe():
                    exe = p.get_exe().get_name()
                else:
                    exe = "[unknown]"
                etree.SubElement(d, 'data').text = stripit(" Process ID %s (%s) has weak process-level permissions: %s\n" % (p.get_pid(), exe, perms.as_text()))

        elif data_name == 'writeable_dirs' or data_name == 'files_write_perms':
            for o in self.get_supporting_data(data_name):
                etree.SubElement(d, 'data').text = o.as_text() + "\n"
            #print "RETURNING: " + d
        return d

    def get_supporting_data(self, data_name):
        #print "data_name: " + data_name
        #print "keys: " + " ".join(self.supporting_data.keys())
        if data_name in self.supporting_data.keys():
            return self.supporting_data[data_name]
        else:
            return None

    def get_rendered_supporting_data(self, section):
        d = etree.Element('details')
        for data_name in wpc.conf.issue_template[self.get_id()]['supporting_data'].keys():
            if wpc.conf.issue_template[self.get_id()]['supporting_data'][data_name]['section'] == section:
                if self.get_supporting_data(data_name):
                    etree.SubElement(d, 'preamble').text = wpc.conf.issue_template[self.get_id()]['supporting_data'][data_name]['preamble'] + "\n\n"
                    d.append(self.render_supporting_data(data_name))
        return d

    def as_xml(self):
        r = etree.Element('issue')
        etree.SubElement(r, 'title').text = wpc.conf.issue_template[self.get_id()]['title']
        s = etree.SubElement(r, 'section', type = 'description')
        etree.SubElement(s, 'body').text = wpc.conf.issue_template[self.get_id()]['description']
        s.append(self.get_rendered_supporting_data('description'))
        s = etree.SubElement(r, 'section', type = 'recommendation')
        etree.SubElement(s, 'body').text = wpc.conf.issue_template[self.get_id()]['recommendation']
        s.append(self.get_rendered_supporting_data('recommendation'))
        return r

