from checkers import checkout, getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        res1 = checkout(f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arx -t{data.get("type")}', "Everything is Ok")
        res2 = checkout(f'ls {data.get("folder_out")}', f'arx.{data.get("type")}')
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout(f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arx -t{data.get("type")}', "Everything is Ok"))
        res.append(checkout(f'cd {data.get("folder_out")}; 7z e arx.{data.get("type")} -o{data.get("folder_ext")} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data.get("folder_ext")}', item))
        assert all(res)

    def test_step3(self):
        # test3
        assert checkout(f'cd {data.get("folder_out")}; 7z t arx.{data.get("type")}', "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert checkout(f'cd {data.get("folder_in")}; 7z u arx2.{data.get("type")}', "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(checkout(f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arx -t{data.get("type")}', "Everything is Ok"))
        for i in make_files:
            res.append(checkout(f'cd {data.get("folder_out")}; 7z l arx.{data.get("type")}', i))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout(f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arx -t{data.get("type")}', "Everything is Ok"))
        res.append(checkout(f'cd {data.get("folder_out")}; 7z x arx.{data.get("type")} -o{data.get("folder_ext2")} -y', "Everything is Ok"))
        for i in make_files:
            res.append(checkout(f'ls {data.get("folder_ext2")}', i))
        res.append(checkout(f'ls {data.get("folder_ext2")}', make_subfolder[0]))
        res.append(checkout(f'ls {data.get("folder_ext2")}/{make_subfolder[0]}', make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert checkout(f'cd {data.get("folder_out")}; 7z d arx.{data.get("folder_out")}', "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(checkout(f'cd {data.get("folder_in")}; 7z h {i}', "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data.get("folder_in"), i)).upper()
            res.append(checkout(f'cd {data.get("folder_in")}; 7z h {i}', hash))
        assert all(res), "test8 FAIL"
