from checkout import *
from deploy import ssh_checkout


class TestNegative:

    def test_step1(self, make_folder, clean_folder, make_files, make_bad_archive, start_time):
        res = ssh_checkout(HOST, USER, PASSWD, f'cd {OUT_FOLDER}; 7z e bad.{ARC_TYPE} -o{FOLDER_FOLDER} -y', TEXT_FAIL)
        save_log(start_time, f'{self.__class__.__name__}')
        assert res, "test1 FAIL"
