from checkout import *
from deploy import ssh_checkout, upload_files


class TestPositive:

    def test_step0(self, start_time):
        res = []
        upload_files(HOST, USER, PASSWD, "p7zip-full.deb", f'/home/{USER}/p7zip-full.deb')
        res.append(
            ssh_checkout(HOST, USER, PASSWD, f'echo "{PASSWD}" | sudo -S dpkg -i /home/{USER}/p7zip-full.deb',
                         "Setting up"))
        res.append(ssh_checkout(HOST, USER, PASSWD, f'echo "{PASSWD}" | sudo -S dpkg -s p7zip-full',
                                "Status: install ok installed"))
        save_log(start_time, f'{self.__class__.__name__}')
        assert all(res), "test0 FAIL"

    def test_step1(self, make_folder, clean_folder, make_files, start_time):
        # test1
        res1 = ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx2', TEXT_OK)
        res2 = ssh_checkout(HOST, USER, PASSWD, f'ls {OUT_FOLDER};', f'arx2.{ARC_TYPE}')
        save_log(start_time, f'{self.__class__.__name__}')
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clean_folder, make_files, start_time):
        # test2
        res = []
        res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx2', TEXT_OK))
        res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {OUT_FOLDER}; 7z e arx2.{ARC_TYPE} -o{FOLDER_FOLDER} -y', TEXT_OK))
        for i in make_files:
            res.append(ssh_checkout(HOST, USER, PASSWD, f'ls {FOLDER_FOLDER}', i))
        save_log(start_time, f'{self.__class__.__name__}')
        assert all(res), "test2 FAIL"

    def test_step3(self, start_time):
        # test3
        res = ssh_checkout(HOST, USER, PASSWD, f'cd {OUT_FOLDER}; 7z t arx2.{ARC_TYPE}', TEXT_OK)
        save_log(start_time, f'{self.__class__.__name__}')
        assert res, "test3 FAIL"

    def test_step4(self, start_time):
        # test4
        res = ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z u arx2.{ARC_TYPE}', TEXT_OK)
        save_log(start_time, f'{self.__class__.__name__}')
        assert res, "test4 FAIL"

    def test_step5(self, clean_folder, make_files, start_time):
        # test5
        res = []
        res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx2', TEXT_OK))
        for i in make_files:
            res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {OUT_FOLDER}; 7z l arx2.{ARC_TYPE}', i))
        save_log(start_time, f'{self.__class__.__name__}')
        assert all(res), "test5 FAIL"

    def test_step6(self, clean_folder, make_files, make_subfolder, start_time):
        # test6
        res = []
        res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z a -t{ARC_TYPE} {OUT_FOLDER}/arx', TEXT_OK))
        res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {OUT_FOLDER}; 7z x arx.{ARC_TYPE} -o{FOLDER_FOLDER} -y', TEXT_OK))
        for i in make_files:
            res.append(ssh_checkout(HOST, USER, PASSWD, f'ls {FOLDER_FOLDER}', i))
        res.append(ssh_checkout(HOST, USER, PASSWD, f'ls {FOLDER_FOLDER}', make_subfolder[0]))
        res.append(ssh_checkout(HOST, USER, PASSWD, f'ls {FOLDER_FOLDER}/{make_subfolder[0]}', make_subfolder[1]))
        save_log(start_time, f'{self.__class__.__name__}')
        assert all(res), "test6 FAIL"

    def test_step7(self, start_time):
        # test7
        res = ssh_checkout(HOST, USER, PASSWD, f'cd {OUT_FOLDER}; 7z d arx.{ARC_TYPE}', TEXT_OK)
        save_log(start_time, f'{self.__class__.__name__}')
        assert res, "test7 FAIL"

    def test_step8(self, clean_folder, make_files, start_time):
        # test8
        res = []
        for i in make_files:
            res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z h {i}', TEXT_OK))
            hash = getout(f'cd {TST_FOLDER}; crc32 {i}').upper()
            res.append(ssh_checkout(HOST, USER, PASSWD, f'cd {TST_FOLDER}; 7z h {i}', hash))
        save_log(start_time, f'{self.__class__.__name__}')
        assert all(res), "test8 FAIL"
